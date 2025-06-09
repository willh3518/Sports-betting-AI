import asyncio
import os
import aiohttp
import logging
import pandas as pd
import random
from bs4 import BeautifulSoup
from Data_Extraction.utils import fetch_html, clean_player_name  # Utility functions

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# File Paths
input_csv = "../Prop_Data_CSV/prizepicks_data.csv"
output_csv = "../Prop_Data_CSV/box_scores.csv"
prop_data_csv = "/Users/willhart/Downloads/did_it_hit - Sheet1.csv"  # The file containing props and 'Hit' column

STATMUSE_URL_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-box-score-last-game"

# List of rotating user-agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
]

PROP_TYPE_MAPPING = {
    "Points": "PTS",
    "Rebounds": "REB",
    "Assists": "AST",
    "Steals": "STL",
    "Blocked Shots": "BLK",
    "FG Made": "FGM",
    "FG Attempted": "FGA",
    "3-PT Made": "3PM",
    "3-PT Attempted": "3PA",
    "Free Throws Made": "FTM",
    "Free Throws Attempted": "FTA",
    "Offensive Rebounds": "OREB",
    "Defensive Rebounds": "DREB",
    "Turnovers": "TOV",
    "Pts+Rebs+Asts": ["PTS", "REB", "AST"],
    "Pts+Rebs": ["PTS", "REB"],
    "Pts+Asts": ["PTS", "AST"],
    "Rebs+Asts": ["REB", "AST"],
    "Blks+Stls": ["BLK", "STL"]
}

async def fetch_html_with_retries(url, max_retries=5):
    """Fetches HTML with rotating User-Agents and exponential backoff retries."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    for attempt in range(max_retries):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        return await response.text()
                    elif response.status in [403, 429]:  # Rate-limited or forbidden
                        logging.warning(f"⚠️ Rate-limited ({response.status}) on attempt {attempt + 1}. Retrying...")
                        await asyncio.sleep((2 ** attempt) + random.uniform(0.5, 2.0))
            except Exception as e:
                logging.warning(f"❌ Request failed: {e}. Retrying...")

    logging.error(f"❌ Max retries reached for {url}. Skipping...")
    return None

def extract_box_score(html):
    """Parses HTML and extracts player box score stats."""
    soup = BeautifulSoup(html, "lxml")

    # Locate the table container
    table = soup.select_one("div.relative.overflow-x-auto table")
    if not table:
        logging.error("❌ Could not find the stats table.")
        return {}

    # Select the first row inside the table (which contains stats)
    stat_row = table.select_one("tbody tr")
    if not stat_row:
        logging.error("❌ No stats found for player.")
        return {}

    # Define the exact column indices to extract (skipping unwanted ones)
    column_indices = {
        "PTS": 8, "REB": 9, "AST": 10, "STL": 11, "BLK": 12,
        "FGM": 13, "FGA": 14, "3PM": 16, "3PA": 17, "FTM": 19,
        "FTA": 20, "OREB": 23, "DREB": 24, "TOV": 25
    }

    values = [td.get_text(strip=True) for td in stat_row.select("td")]

    # Ensure we have enough values in the row to extract stats
    if max(column_indices.values()) >= len(values):
        logging.warning("⚠️ Possible mismatch in extracted columns. Some stats might be missing.")

    # Extract only the needed columns using the correct index mapping
    stats = {key: values[idx] for key, idx in column_indices.items() if idx < len(values)}

    return stats

async def scrape_player_box_score(player_name, session):
    """Scrapes last game box score for a single player."""
    url = STATMUSE_URL_TEMPLATE.format(player=player_name.replace(" ", "-").lower())
    html = await fetch_html_with_retries(url)
    stats = extract_box_score(html) if html else {}
    if stats:
        stats["Player"] = player_name  # Add player name
    return stats

async def scrape_all_box_scores():
    """Scrapes last game box scores for all players from input CSV and updates the hit column."""
    if not os.path.exists(input_csv):
        logging.error(f"🚨 Input CSV '{input_csv}' not found!")
        return

    df = pd.read_csv(input_csv)
    unique_players = set(
        name for _, row in df.iterrows()
        if (name := clean_player_name(row["Player"].strip())) is not None
    )

    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_player_box_score(player, session) for player in unique_players]
        responses = await asyncio.gather(*tasks)

    for player, stats in zip(unique_players, responses):
        if stats:
            results.append(stats)

    if not results:
        logging.warning("⚠️ No box scores were successfully scraped.")
        return

    # Convert to DataFrame and save
    df_output = pd.DataFrame(results)
    df_output = df_output[
        ["Player"] + [col for col in df_output.columns if col != "Player"]]  # Ensure Player is first column
    df_output.sort_values(by="Player", inplace=True)
    df_output.to_csv(output_csv, index=False, encoding="utf-8")
    logging.info(f"✅ Box scores saved to '{output_csv}'")

    update_hit_column()

def update_hit_column():
    """Fills out the 'Actual Stat' and 'Hit' columns in processed_data.csv by comparing to box_scores.csv."""
    if not os.path.exists(prop_data_csv) or not os.path.exists(output_csv):
        logging.error("🚨 One of the required CSV files is missing!")
        return

    prop_df = pd.read_csv(prop_data_csv)
    box_scores_df = pd.read_csv(output_csv)

    # ✅ Ensure Player name consistency (clean both prop_df and box_scores_df)
    prop_df["Player"] = prop_df["Player"].apply(clean_player_name)
    box_scores_df["Player"] = box_scores_df["Player"].apply(clean_player_name)

    def get_stat_value(row):
        """Retrieves the correct stat value from the box score based on the prop type."""
        player_name = row["Player"]
        prop_type = row["Prop Type"]

        if player_name not in box_scores_df["Player"].values:
            return -999  # Player not found in box score

        player_stats = box_scores_df.loc[box_scores_df["Player"] == player_name]

        if prop_type in PROP_TYPE_MAPPING:
            mapped_stat = PROP_TYPE_MAPPING[prop_type]

            if isinstance(mapped_stat, list):  # For compound stats
                return player_stats[mapped_stat].sum(axis=1).values[0]

            if mapped_stat in player_stats.columns:
                return player_stats[mapped_stat].values[0]

        return -999  # Stat type not found

    prop_df["Actual Stat"] = prop_df.apply(get_stat_value, axis=1)

    # ✅ Determine if the prop hit (1) or missed (0)
    prop_df["Hit"] = prop_df.apply(
        lambda row: 1 if row["Actual Stat"] >= row["Prop Value"] else 0 if row["Actual Stat"] != -999 else -999, axis=1
    )

    prop_df.to_csv(prop_data_csv, index=False, encoding="utf-8")
    logging.info(f"✅ Updated '{prop_data_csv}' with actual stats and hit values.")

if __name__ == "__main__":
    asyncio.run(scrape_all_box_scores())

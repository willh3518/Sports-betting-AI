import asyncio
import os
import aiohttp
import pandas as pd
import logging
import re
from Data_Extraction.utils import fetch_html, clean_player_name

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

# 📌 Input & Output CSV Paths
csv_folder = "../Prop_Data_CSV"
input_csv = os.path.join(csv_folder, "prizepicks_data.csv")
season_stats_csv = os.path.join(csv_folder, "season_stats.csv")
output_csv = os.path.join(csv_folder, "season_hit_percentage.csv")

# 📌 StatMuse Query Template
STATMUSE_HIT_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-games-with-more-than-{value}-{prop}-this-season"


# 📌 Load Games Played Data from `season_stats.csv`
def load_games_played():
    """Loads Games Played (GP) from `season_stats.csv`."""
    if not os.path.exists(season_stats_csv):
        logging.error(f"🚨 Season stats file '{season_stats_csv}' not found!")
        return {}

    df = pd.read_csv(season_stats_csv)
    df = df[["Player", "GP"]].dropna()
    df["GP"] = df["GP"].astype(str).str.extract(r"(\d+)").fillna("0")  # Extract numeric GP values
    return dict(zip(df["Player"], df["GP"]))

def extract_hit_percentage(html):
    """Extracts games hit count from StatMuse results."""
    if not html:
        return 0

    match = re.search(r"(\d+) games", html)
    return int(match.group(1)) if match else 0

async def scrape_hit_percentage(player_name, prop, value, session):
    """Scrapes season hit percentage for a given player & prop."""
    formatted_player = player_name.replace(" ", "-").lower()
    formatted_prop = prop.replace(" ", "-").lower()
    url = STATMUSE_HIT_TEMPLATE.format(player=formatted_player, value=value, prop=formatted_prop)

    html = await fetch_html(url)
    games_hit = extract_hit_percentage(html)

    return player_name, prop, value, games_hit

async def scrape_all_hit_percentages():
    """Scrapes season hit percentages for all player-prop combinations in the input CSV."""
    if not os.path.exists(input_csv):
        logging.error(f"🚨 Input CSV '{input_csv}' not found!")
        return

    # Load Games Played Data
    games_played_map = load_games_played()

    df = pd.read_csv(input_csv)
    player_props = [
        (clean_player_name(row["Player"].strip()), row["Prop Type"].strip(), str(row["Prop Value"]).strip())
        for _, row in df.iterrows()
        if clean_player_name(row["Player"].strip()) and row["Prop Type"].strip() and str(
            row["Prop Value"]).strip().replace('.', '', 1).isdigit()
    ]

    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_hit_percentage(player, prop, value, session) for player, prop, value in player_props]
        responses = await asyncio.gather(*tasks)

    for player, prop, value, games_hit in responses:
        gp = int(games_played_map.get(player, 0))  # Get GP from season_stats.csv, default 0 if missing
        hit_percentage = round((games_hit / gp) * 100, 1) if gp > 0 else "N/A"

        results.append({
            "Player": player,
            "Prop": f"{prop.capitalize()} {value}",
            "Hit Percentage": f"{hit_percentage}%"
        })

    # ✅ Convert to DataFrame and Save
    df_output = pd.DataFrame(results)
    df_output.fillna("N/A", inplace=True)
    df_output.sort_values(by="Player", inplace=True)
    df_output.to_csv(output_csv, index=False, encoding="utf-8")

    logging.info(f"✅ Season hit percentages saved to '{output_csv}'")

if __name__ == "__main__":
    asyncio.run(scrape_all_hit_percentages())

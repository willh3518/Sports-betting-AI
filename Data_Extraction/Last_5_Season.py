import asyncio
import os
import aiohttp
import pandas as pd
import logging
import re
from bs4 import BeautifulSoup
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
output_csv = os.path.join(csv_folder, "last_5_games_avg.csv")

# 📌 StatMuse Query Template
STATMUSE_LAST_5_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-in-the-last-5-games"

def extract_last_5_avg(html):
    """Parses Last 5 games stats, extracts only the 'Average' row."""
    soup = BeautifulSoup(html, "lxml")

    # ✅ Extract Table Data
    table = soup.select_one("table")
    if not table:
        return {"GP": "N/A"}  # Default to N/A if no data is found

    headers = [th.get_text(strip=True) for th in table.select("th")]
    rows = table.select("tr")

    if len(rows) < 2:
        return {"GP": "N/A"}  # Not enough data

    # ✅ Extract **only the average row** (last row in table)
    avg_row = rows[-2].select("td")
    avg_values = [td.get_text(strip=True) for td in avg_row]

    # ✅ Map stats correctly
    stat_mapping = {
        "PTS": "PPG", "REB": "RPG", "AST": "APG", "STL": "SPG", "BLK": "BPG",
        "FGM": "FGM", "FGA": "FGA", "3PM": "3PM", "3PA": "3PA",
        "FTM": "FTM", "FTA": "FTA", "OREB": "OREB", "DREB": "DREB", "TOV": "TPG"
    }

    avg_stats = {stat_mapping.get(headers[i], headers[i]): avg_values[i] for i in range(len(headers)) if headers[i] in stat_mapping}

    # ✅ Force "Games Played" to be 5
    avg_stats["GP"] = "5"

    return avg_stats

async def scrape_last_5_avg(player_name, session):
    """Scrapes last 5 games average stats for a player."""
    formatted_player = player_name.replace(" ", "-").lower()
    url = STATMUSE_LAST_5_TEMPLATE.format(player=formatted_player)

    html = await fetch_html(url)
    return extract_last_5_avg(html) if html else {"GP": "N/A"}  # Handle missing data

async def scrape_all_last_5_avg():
    """Scrapes last 5 games average stats for all players in the input CSV."""
    if not os.path.exists(input_csv):
        logging.error(f"🚨 Input CSV '{input_csv}' not found!")
        return

    df = pd.read_csv(input_csv)
    unique_players = {
        name for _, row in df.iterrows()
        if (name := clean_player_name(row["Player"].strip())) is not None
    }

    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_last_5_avg(player, session) for player in unique_players]
        responses = await asyncio.gather(*tasks)

    for player, avg_stats in zip(unique_players, responses):
        avg_stats["Player"] = player  # Attach player name
        results.append(avg_stats)

    # ✅ Convert to DataFrame and Save
    df_output = pd.DataFrame(results)

    # ✅ Ensure proper column order
    cols = ["Player", "GP"] + [col for col in df_output.columns if col not in ["Player", "GP"]]
    df_output = df_output[cols]

    df_output.fillna("N/A", inplace=True)
    df_output.sort_values(by="Player", inplace=True)
    df_output.to_csv(output_csv, index=False, encoding="utf-8")

    logging.info(f"✅ Last 5 games average stats saved to '{output_csv}'")

if __name__ == "__main__":
    asyncio.run(scrape_all_last_5_avg())

import asyncio
import os
import aiohttp
import pandas as pd
import logging
from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
from Data_Extraction.utils import fetch_html, clean_player_name  # Utility functions

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

input_csv = "../Prop_Data_CSV/prizepicks_data.csv"
output_csv = "../Prop_Data_CSV/season_stats.csv"

STATMUSE_URL_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-2024-25-season-stats"


def extract_stats(html):
    """Parses HTML and extracts player stats from the first table."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("table")
    if not table:
        return {}

    headers = [th.get_text(strip=True) for th in table.select("th")]
    values = [td.get_text(strip=True) for td in table.select("td")]

    valid_stats = ["GP", "PPG", "RPG", "APG", "SPG", "BPG", "FGM", "FGA", "3PM", "3PA", "FTM", "FTA", "OREB", "DREB",
                   "TPG"]

    return {headers[i]: values[i] for i in range(len(headers)) if headers[i] in valid_stats}

async def scrape_player_stats(player_name, session):
    """Scrapes season stats for a single player."""
    url = STATMUSE_URL_TEMPLATE.format(player=player_name.replace(" ", "-").lower())
    html = await fetch_html(url)
    return extract_stats(html) if html else {}

async def scrape_all_season_stats():
    """Scrapes season stats for all players from input CSV."""
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
        tasks = [scrape_player_stats(player, session) for player in unique_players]
        responses = await asyncio.gather(*tasks)

    for player, stats in zip(unique_players, responses):
        stats["Player"] = player  # Add player name
        results.append(stats)

    # Convert to DataFrame and reorder columns
    df_output = pd.DataFrame(results)
    cols = ["Player"] + [col for col in df_output.columns if col != "Player"]
    df_output = df_output[cols]

    df_output.sort_values(by="Player", inplace=True)

    df_output.to_csv(output_csv, index=False, encoding="utf-8")
    logging.info(f"✅ Season stats saved to '{output_csv}'")

if __name__ == "__main__":
    asyncio.run(scrape_all_season_stats())

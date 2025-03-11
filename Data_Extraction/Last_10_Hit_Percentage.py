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
output_csv = os.path.join(csv_folder, "last_10_hit_percentage.csv")

# 📌 StatMuse Query Template
STATMUSE_LAST_10_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-vs-{team}-in-last-10-matchups"

TEAM_NAME_MAPPING = {
    "ATL": "Atlanta", "BOS": "Boston", "BKN": "Brooklyn", "CHA": "Charlotte",
    "CHI": "Chicago", "CLE": "Cleveland", "DAL": "Dallas", "DEN": "Denver",
    "DET": "Detroit", "GSW": "Golden-State", "HOU": "Houston", "IND": "Indiana",
    "LAC": "LA-Clippers", "LAL": "LA-Lakers", "MEM": "Memphis", "MIA": "Miami",
    "MIL": "Milwaukee", "MIN": "Minnesota", "NOP": "New-Orleans", "NYK": "New-York",
    "OKC": "Oklahoma-City", "ORL": "Orlando", "PHI": "Philadelphia", "PHX": "Phoenix",
    "POR": "Portland", "SAC": "Sacramento", "SAS": "San-Antonio", "TOR": "Toronto",
    "UTA": "Utah", "WAS": "Washington"
}

def extract_last_10_logs(html):
    """Extracts last 10 matchup game logs from StatMuse."""
    soup = BeautifulSoup(html, "lxml")
    table = soup.select_one("table")

    if not table:
        return []

    rows = table.select("tr")
    if len(rows) < 2:
        return []

    headers = [th.get_text(strip=True) for th in table.select("th")]

    # ✅ Extract all game logs (excluding the last row, which is the average row)
    stats_list = []
    for row in rows[1:-1]:  # Exclude the last row
        values = [td.get_text(strip=True) for td in row.select("td")]
        stats = {headers[i]: values[i] for i in range(len(headers))}
        stats_list.append(stats)

    return stats_list  # ✅ Return only individual game logs

def calculate_hit_percentage(game_logs, prop_type, threshold):
    """Calculates the percentage of last 10 matchups where the player hit the prop threshold."""
    prop_mapping = {
        "points": "PTS", "assists": "AST", "rebounds": "REB",
        "steals": "STL", "blocks": "BLK", "fg made": "FGM",
        "fg attempted": "FGA", "3-pt made": "3PM", "3-pt attempted": "3PA",
        "turnovers": "TOV", "offensive rebounds": "OREB", "defensive rebounds": "DREB",
        "pts+asts": ["PTS", "AST"], "pts+rebs": ["PTS", "REB"],
        "pts+rebs+asts": ["PTS", "REB", "AST"], "rebs+asts": ["REB", "AST"],
        "blks+stls": ["BLK", "STL"]
    }

    stat_key = prop_mapping.get(prop_type.lower())
    if not stat_key:
        return 0  # Skip unsupported props

    hit_count = 0
    total_games = len(game_logs)

    for game in game_logs:
        if isinstance(stat_key, list):
            stat_value = sum(float(game.get(k, 0)) for k in stat_key)
        else:
            stat_value = float(game.get(stat_key, 0))

        if stat_value >= threshold:
            hit_count += 1

    return round((hit_count / total_games) * 100, 1) if total_games else "N/A"

async def scrape_last_10_stats(player_name, opposing_team, session):
    """Scrapes last 10 matchups for a player vs an opponent."""
    if not opposing_team:
        return []

    formatted_player = player_name.replace(" ", "-").lower()
    formatted_team = TEAM_NAME_MAPPING.get(opposing_team, opposing_team).replace(" ", "-").lower()
    url = STATMUSE_LAST_10_TEMPLATE.format(player=formatted_player, team=formatted_team)

    html = await fetch_html(url)
    return extract_last_10_logs(html) if html else []

async def scrape_all_last_10_hit_percentages():
    """Scrapes last 10 hit percentages for all player-prop combinations."""
    if not os.path.exists(input_csv):
        logging.error(f"🚨 Input CSV '{input_csv}' not found!")
        return

    df = pd.read_csv(input_csv)
    player_props = [
        (clean_player_name(row["Player"].strip()), row["Prop Type"].strip(), str(row["Prop Value"]).strip(),
         row["Opposing Team"].strip())
        for _, row in df.iterrows()
        if clean_player_name(row["Player"].strip()) and row["Prop Type"].strip() and str(
            row["Prop Value"]).strip().replace('.', '', 1).isdigit()
    ]

    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_last_10_stats(player, opponent, session) for player, _, _, opponent in player_props]
        responses = await asyncio.gather(*tasks)

    for (player, prop, value, opponent), game_logs in zip(player_props, responses):
        last_10_hit_percentage = calculate_hit_percentage(game_logs, prop, float(value))

        results.append({
            "Player": player,
            "Prop": f"{prop.capitalize()} {value}",
            "Last 10 Hit Percentage": f"{last_10_hit_percentage}%"
        })

    # ✅ Convert to DataFrame and Save
    df_output = pd.DataFrame(results)
    df_output.fillna("N/A", inplace=True)
    df_output.sort_values(by="Player", inplace=True)
    df_output.to_csv(output_csv, index=False, encoding="utf-8")

    logging.info(f"✅ Last 10 hit percentages saved to '{output_csv}'")

if __name__ == "__main__":
    asyncio.run(scrape_all_last_10_hit_percentages())

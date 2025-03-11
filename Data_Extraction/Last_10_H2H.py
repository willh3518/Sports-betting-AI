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
output_csv = os.path.join(csv_folder, "last_10_h2h.csv")

# 📌 StatMuse Query Template
STATMUSE_LAST_10_TEMPLATE = "https://www.statmuse.com/nba/ask/{player}-vs-{team}-in-last-10-matchups"

# 📌 Team Name Mapping
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

def extract_last_10_stats(html):
    """Extracts last 10 matchups stats for a player vs an opponent."""
    soup = BeautifulSoup(html, "lxml")

    # ✅ Extract games played from header
    header_element = soup.find("h1")
    header_text = header_element.text.strip() if header_element else ""

    games_played_match = re.search(r"in (\d+) games?", header_text)
    games_played = games_played_match.group(1) if games_played_match else "N/A"

    # ✅ Extract opponent name
    opponent_match = re.search(r"vs (.*?) in", header_text, re.IGNORECASE)
    opponent_name = opponent_match.group(1) if opponent_match else "Unknown"

    # ✅ Extract table stats
    table = soup.select_one("table")
    if not table:
        return {"Opponent": opponent_name, "GP": games_played}

    headers = [th.get_text(strip=True) for th in table.select("th")]
    rows = table.select("tr")

    # ✅ Handling multi-game case (Check if an average row exists)
    if len(rows) > 2:
        last_row = rows[-2].select("td")  # ✅ Use second-last row as the average row
    else:
        last_row = rows[1].select("td")  # Otherwise, use the first row

    values = [td.get_text(strip=True) for td in last_row]

    stat_mapping = {
        "PTS": "PPG", "REB": "RPG", "AST": "APG", "STL": "SPG", "BLK": "BPG",
        "FGM": "FGM", "FGA": "FGA", "3PM": "3PM", "3PA": "3PA",
        "FTM": "FTM", "FTA": "FTA", "OREB": "OREB", "DREB": "DREB", "TOV": "TPG"
    }

    stats = {stat_mapping.get(headers[i], headers[i]): values[i] if i < len(values) else "N/A"
             for i in range(len(headers)) if headers[i] in stat_mapping}

    # ✅ Ensure opponent & GP are included
    stats["Opponent"] = opponent_name
    stats["GP"] = games_played

    return stats

async def scrape_last_10_stats(player_name, opposing_team, session):
    """Scrapes last 10 matchups stats for a single player against an opponent."""
    if not opposing_team:
        return {"Player": player_name, "Opponent": "N/A", "GP": "N/A"}

    formatted_player = player_name.replace(" ", "-").lower()
    formatted_team = TEAM_NAME_MAPPING.get(opposing_team, opposing_team).replace(" ", "-").lower()
    url = STATMUSE_LAST_10_TEMPLATE.format(player=formatted_player, team=formatted_team)

    html = await fetch_html(url)
    stats = extract_last_10_stats(html) if html else {}

    stats["Player"] = player_name  # Ensure player name is included
    stats["Opponent"] = opposing_team  # Ensure opponent is included

    return stats

async def scrape_all_last_10():
    """Scrapes last 10 matchups stats for all players in the input CSV."""
    if not os.path.exists(input_csv):
        logging.error(f"🚨 Input CSV '{input_csv}' not found!")
        return

    df = pd.read_csv(input_csv)
    unique_players = {
        name: TEAM_NAME_MAPPING.get(row["Opposing Team"], row["Opposing Team"])
        for _, row in df.iterrows()
        if (name := clean_player_name(row["Player"].strip())) is not None and row["Opposing Team"].strip()
    }

    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_last_10_stats(player, team, session) for player, team in unique_players.items()]
        responses = await asyncio.gather(*tasks)

    for (player, team), stats in zip(unique_players.items(), responses):
        stats["Player"] = player
        stats["Opponent"] = team
        results.append(stats)

    # ✅ Convert to DataFrame and reorder columns
    df_output = pd.DataFrame(results)

    cols = ["Player", "Opponent", "GP"] + [col for col in df_output.columns if col not in ["Player", "Opponent", "GP"]]
    df_output = df_output[cols]

    # ✅ Fill missing values with "N/A"
    df_output.fillna("N/A", inplace=True)

    df_output.sort_values(by="Player", inplace=True)

    # ✅ Save to CSV
    df_output.to_csv(output_csv, index=False, encoding="utf-8")
    logging.info(f"✅ Last 10 matchups stats saved to '{output_csv}'")

if __name__ == "__main__":
    asyncio.run(scrape_all_last_10())

import asyncio
import os
import aiohttp
import pandas as pd
import logging
import re
from bs4 import BeautifulSoup
from Data_Extraction.utils import fetch_html

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# 📌 Input & Output CSV Paths
csv_folder = "../Prop_Data_CSV"
prizepicks_csv = os.path.join(csv_folder, "prizepicks_data.csv")
output_csv = os.path.join(csv_folder, "home_away_status.csv")

# 📌 StatMuse Query for Today's Schedule
STATMUSE_SCHEDULE_URL = "https://www.statmuse.com/nba/ask/nba-schedule-tonight"

# ✅ Extended Team Name Mapping
TEAM_NAME_MAPPING = {
    "Bulls": "CHI", "Magic": "ORL", "76ers": "PHI", "Celtics": "BOS",
    "Warriors": "GSW", "Nets": "BKN", "Pacers": "IND", "Hawks": "ATL",
    "Rockets": "HOU", "Pelicans": "NOP", "Knicks": "NYK", "Heat": "MIA",
    "Cavaliers": "CLE", "Trail Blazers": "POR", "Jazz": "UTA", "Wizards": "WAS",
    "Timberwolves": "MIN", "Hornets": "CHA", "Mavericks": "DAL", "Bucks": "MIL",
    "Kings": "SAC", "Nuggets": "DEN", "Thunder": "OKC", "Grizzlies": "MEM",
    "Pistons": "DET", "Clippers": "LAC", "Lakers": "LAL", "Raptors": "TOR",
    "Suns": "PHX", "Spurs": "SAS"
}

# ✅ Step 1: Fetch Tonight's NBA Schedule
async def fetch_schedule():
    """Fetches today's NBA schedule from StatMuse and extracts team matchups."""
    html = await fetch_html(STATMUSE_SCHEDULE_URL)

    if not html:
        logging.error("🚨 Failed to fetch NBA schedule!")
        return []

    soup = BeautifulSoup(html, "html.parser")
    matchups = []

    # ✅ Select all game blocks
    game_blocks = soup.select("div.border-t.border-gray-6.py-2.flex.flex-col")

    for game_block in game_blocks:
        team_elements = game_block.select("div[class*='flex'][class*='items'][class*='py-2.5'] p")

        if len(team_elements) == 2:
            away_team = team_elements[0].get_text(strip=True)
            home_team = team_elements[1].get_text(strip=True)

            # Normalize team names
            away_team = TEAM_NAME_MAPPING.get(away_team, away_team)
            home_team = TEAM_NAME_MAPPING.get(home_team, home_team)

            matchups.append((away_team, "Away"))
            matchups.append((home_team, "Home"))

    if not matchups:
        logging.error("🚨 No valid matchups found in schedule!")

    return matchups

# ✅ Step 2: Map Players to Home/Away Status
def map_home_away(prizepicks_df, matchups):
    """Maps each player's team to their home/away status based on the schedule."""
    team_status = {team: status for team, status in matchups}  # Convert list to dictionary

    # ✅ Ensure BOTH Home and Away teams are mapped
    prizepicks_df["Home/Away"] = prizepicks_df["Team"].map(team_status).fillna("N/A")

    return prizepicks_df[["Player", "Team", "Home/Away"]].drop_duplicates()

# ✅ Step 3: Process and Save Data
async def main():
    if not os.path.exists(prizepicks_csv):
        logging.error(f"🚨 Input CSV '{prizepicks_csv}' not found!")
        return

    prizepicks_df = pd.read_csv(prizepicks_csv)
    prizepicks_df = prizepicks_df.drop_duplicates(subset=["Player", "Team"])  # Ensure unique players

    matchups = await fetch_schedule()
    if not matchups:
        logging.error("🚨 No games found in schedule!")
        return

    final_df = map_home_away(prizepicks_df, matchups)
    final_df.to_csv(output_csv, index=False)
    logging.info(f"✅ Saved home/away status to {output_csv}")

if __name__ == "__main__":
    asyncio.run(main())

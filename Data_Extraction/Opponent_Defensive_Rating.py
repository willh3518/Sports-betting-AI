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
output_csv = os.path.join(csv_folder, "opponent_defensive_ratings.csv")

# 📌 StatMuse Query Template
STATMUSE_DEF_RATING_TEMPLATE = "https://www.statmuse.com/nba/ask/{team}-defensive-rating"

# 📌 Team Name Mapping for URL Formatting
TEAM_NAME_MAPPING = {
    "ATL": "atlanta", "BOS": "boston", "BKN": "brooklyn", "CHA": "charlotte",
    "CHI": "chicago", "CLE": "cleveland", "DAL": "dallas", "DEN": "denver",
    "DET": "detroit", "GSW": "golden-state", "HOU": "houston", "IND": "indiana",
    "LAC": "la-clippers", "LAL": "la-lakers", "MEM": "memphis", "MIA": "miami",
    "MIL": "milwaukee", "MIN": "minnesota", "NOP": "new-orleans", "NYK": "new-york",
    "OKC": "oklahoma-city", "ORL": "orlando", "PHI": "philadelphia", "PHX": "phoenix",
    "POR": "portland", "SAC": "sacramento", "SAS": "san-antonio", "TOR": "toronto",
    "UTA": "utah", "WAS": "washington"
}

# ✅ Step 1: Extract Unique Opponent Teams (Skipping Combo Teams)
def extract_unique_opponents():
    """Extracts unique opponent teams from PrizePicks data, skipping combo teams."""
    df = pd.read_csv(prizepicks_csv)
    if "Opposing Team" not in df.columns:
        logging.error("🚨 'Opposing Team' column not found in PrizePicks data!")
        return {}

    unique_teams = df["Opposing Team"].dropna().unique()

    # ✅ Skip teams containing '/'
    filtered_teams = {TEAM_NAME_MAPPING.get(team, team).replace(" ", "-").lower(): team
                      for team in unique_teams if "/" not in team}

    return filtered_teams

# ✅ Step 2: Extract Defensive Rating from HTML
def extract_defensive_rating(html):
    """Parses StatMuse HTML to extract defensive rating."""
    soup = BeautifulSoup(html, "lxml")

    # Extract rating from main text (if available)
    header_element = soup.select_one("h1")
    if header_element:
        match = re.search(r"defensive rating of (\d+\.\d+)", header_element.text)
        if match:
            return match.group(1)

    # Extract rating from the stats table
    table = soup.select_one("table")
    if table:
        headers = [th.get_text(strip=True) for th in table.select("th")]
        rows = table.select("tr")
        if len(rows) > 1:
            values = [td.get_text(strip=True) for td in rows[1].select("td")]
            if "DRTG" in headers:
                return values[headers.index("DRTG")]

    return "N/A"

# ✅ Step 3: Fetch Defensive Ratings for Each Team
async def fetch_defensive_rating(session, formatted_team):
    """Fetches the defensive rating for a single team."""
    url = STATMUSE_DEF_RATING_TEMPLATE.format(team=formatted_team)
    html = await fetch_html(url)
    return extract_defensive_rating(html) if html else "N/A"

# ✅ Step 4: Process All Teams
async def process_defensive_ratings():
    """Processes all unique teams and fetches their defensive ratings."""
    teams = extract_unique_opponents()
    if not teams:
        logging.warning("⚠️ No valid opponent teams found.")
        return []

    stats_data = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_defensive_rating(session, formatted_team) for formatted_team in teams.keys()]
        ratings = await asyncio.gather(*tasks)

    for (formatted_team, original_team), rating in zip(teams.items(), ratings):
        stats_data.append({"Team": original_team, "Defensive Rating": rating})

    return stats_data

# ✅ Step 5: Save to CSV
async def main():
    """Main function to scrape and save defensive ratings."""
    stats_data = await process_defensive_ratings()
    df = pd.DataFrame(stats_data, columns=["Team", "Defensive Rating"])
    df.to_csv(output_csv, index=False)
    logging.info(f"✅ Defensive ratings saved to {output_csv}")

if __name__ == "__main__":
    asyncio.run(main())

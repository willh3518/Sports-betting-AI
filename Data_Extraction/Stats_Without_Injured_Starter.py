import asyncio
import os
import aiohttp
import pandas as pd
import logging
import unicodedata
import re
from bs4 import BeautifulSoup
from Data_Extraction.utils import fetch_html, clean_player_name

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# 📌 Input & Output CSV Paths
csv_folder = "../Prop_Data_CSV"
lineup_csv = os.path.join(csv_folder, "Constant_CSV/starting_lineups.csv")
output_csv = os.path.join(csv_folder, "season_stats_without_injured_players.csv")

# 📌 ESPN Injury Report URL
ESPN_INJURY_URL = "https://www.espn.com/nba/injuries"

# 📌 StatMuse Query Template
STATMUSE_NO_INJURY_TEMPLATE = "https://www.statmuse.com/nba/ask?q={player}+in+the+2024-25+season+in+games+without+{injured_player}"

TEAM_NAME_MAPPING = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BKN", "Charlotte Hornets": "CHA",
    "Chicago Bulls": "CHI", "Cleveland Cavaliers": "CLE", "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET", "Golden State Warriors": "GSW", "Houston Rockets": "HOU", "Indiana Pacers": "IND",
    "LA Clippers": "LAC", "Los Angeles Lakers": "LAL", "Memphis Grizzlies": "MEM", "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOP", "New York Knicks": "NYK",
    "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL", "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHX",
    "Portland Trail Blazers": "POR", "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS", "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA", "Washington Wizards": "WAS"
}

# 📌 Headers for CSV Output
HEADERS = [
    "Player", "Playing without Injured Player", "Team",
    "PTS", "REB", "AST", "STL", "BLK", "FGM", "FGA", "3PM", "3PA",
    "FTM", "FTA", "OREB", "DREB", "TOV"
]

# ✅ Step 1: Fetch ESPN Injury Report
async def fetch_injury_data():
    """Fetches the ESPN injury report."""
    html = await fetch_html(ESPN_INJURY_URL)
    if not html:
        logging.error("🚨 Failed to fetch ESPN injury data!")
        return []

    soup = BeautifulSoup(html, "html.parser")

    injuries = []
    teams = soup.select(".Table__Title")
    tables = soup.select("table.Table tbody")

    for team, table in zip(teams, tables):
        team_name = team.get_text(strip=True)
        rows = table.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 4:
                player_name = cells[0].get_text(strip=True)
                status = cells[3].get_text(strip=True)
                injuries.append((player_name, team_name, status))

    return injuries

# ✅ Step 2: Filter Injured Starters (Without Saving to CSV)
def filter_injured_starters(injuries_df):
    """Filters injured starters from the injury report and returns the data without saving to CSV."""
    starting_lineups_df = pd.read_csv(lineup_csv)

    # Ensure proper column formatting
    injuries_df.columns = injuries_df.columns.str.strip()
    starting_lineups_df.columns = starting_lineups_df.columns.str.strip()

    # Flatten starting lineup DataFrame
    starter_players = set(starting_lineups_df.melt(id_vars=["Team"], var_name="Position", value_name="Player")["Player"])

    # Filter injuries to only include players who are starters
    injured_starters_df = injuries_df[injuries_df["Name"].isin(starter_players)]

    logging.info("✅ Injured starters list extracted.")

    return injured_starters_df  # ✅ Returning DataFrame instead of saving it

# ✅ Step 3: Match Healthy Players with Injured Teammates
def get_matched_players(injured_starters_df):
    """Matches healthy players with injured teammates on the same team."""
    # Standardize team names
    injured_starters_df.loc[:, "Team"] = injured_starters_df["Team"].map(TEAM_NAME_MAPPING)

    # Track injured players
    out_players = set(injured_starters_df[injured_starters_df["Status"] == "Out"]["Name"].tolist())
    injured_status_dict = {row["Name"]: row["Status"] for _, row in injured_starters_df.iterrows()}

    # Extract unique players from prizepicks data
    prizepicks_df = pd.read_csv(os.path.join(csv_folder, "prizepicks_data.csv"))
    healthy_players_df = prizepicks_df[['Player', 'Team']].drop_duplicates()

    # Merge healthy players with injured teammates
    merged_df = healthy_players_df.merge(
        injured_starters_df[['Name', 'Team']],
        on="Team", how="left"
    ).rename(columns={"Name": "Injured Player"})

    # Remove players without injured teammates
    merged_df = merged_df.dropna(subset=["Injured Player"])

    # Append (Day-To-Day) if needed
    merged_df["Injured Player"] = merged_df["Injured Player"].apply(
        lambda x: f"{x} (Day-To-Day)" if injured_status_dict.get(x) == "Day-To-Day" else x
    )

    # Remove players who are marked as "Out"
    merged_df = merged_df[~merged_df["Player"].isin(out_players)]

    return merged_df.sort_values(by=["Team", "Player"])

# ✅ Step 4: Fetch Stats from StatMuse
async def fetch_stats(session, player, injured_player):
    """Fetches season stats for a player in games without the injured teammate."""
    injured_player_clean = injured_player.replace(" (Day-To-Day)", "")

    if player == injured_player_clean:
        logging.warning(f"Skipping self-search: {player} without {injured_player}")
        return {}

    url = STATMUSE_NO_INJURY_TEMPLATE.format(
        player=player.replace(" ", "+"),
        injured_player=injured_player_clean.replace(" ", "+")
    )

    html = await fetch_html(url)
    return parse_stats(html) if html else {}

def parse_stats(html):
    """Parses HTML and extracts the average stats row."""
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if not table:
        return {}

    rows = table.find_all("tr")
    if len(rows) < 3:
        return {}

    headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]
    avg_row = rows[-2].find_all("td")  # Extract second-to-last row

    values = [td.get_text(strip=True) for td in avg_row]
    return {headers[i]: values[i] if i < len(values) else "N/A" for i in range(len(headers))}

# ✅ Step 5: Process Players and Fetch Stats
async def process_players(matched_players_df):
    """Processes all players and retrieves their stats."""
    stats_data = []

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_stats(session, row["Player"], row["Injured Player"]) for _, row in matched_players_df.iterrows()]
        results = await asyncio.gather(*tasks)

    for (_, row), stats in zip(matched_players_df.iterrows(), results):
        if stats:
            csv_row = [row["Player"], row["Injured Player"], row["Team"]] + [
                stats.get(stat, "N/A") if stats.get(stat) else "N/A" for stat in HEADERS[3:]
            ]
            stats_data.append(csv_row)

    return stats_data

async def main():
    injuries = await fetch_injury_data()

    # ✅ Store the injury data in memory instead of saving to CSV
    injuries_df = pd.DataFrame(injuries, columns=["Name", "Team", "Status"])

    # ✅ Store the injured starters in memory instead of saving to CSV
    injured_starters_df = filter_injured_starters(injuries_df)

    # ✅ Generate matched players and pass it to process_players()
    matched_players_df = get_matched_players(injured_starters_df)
    stats_data = await process_players(matched_players_df)

    df = pd.DataFrame(stats_data, columns=HEADERS)
    df.fillna("N/A", inplace=True)  # ✅ Fill empty cells with "N/A"
    df.sort_values(by="Player", inplace=True)
    df.to_csv(output_csv, index=False)

    logging.info(f"✅ Saved results to {output_csv}")

if __name__ == "__main__":
    asyncio.run(main())

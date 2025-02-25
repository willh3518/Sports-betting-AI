import aiohttp
import asyncio
import pandas as pd
import csv
import logging
from bs4 import BeautifulSoup

# 📌 File Paths
PRIZEPICKS_DATA_FILE = "prizepicks_data.csv"
INJURED_STARTERS_FILE = "injured_starters.csv"
OUTPUT_CSV_FILE = "Season_Stats_without_Injured_Players.csv"

# 📌 Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("scraper.log"), logging.StreamHandler()]
)

# 📌 Team Name Mapping (Ensures Consistency)
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
    "Player", "Playing without Injured Player", "Team", "Season Stats",
    "PTS", "REB", "AST", "STL", "BLK", "FGM", "FGA", "3PM", "3PA", "FTM", "FTA", "OREB", "DREB", "TOV"
]

# 📌 Step 1: Extract Unique Players from PrizePicks Data
def extract_unique_players():
    df = pd.read_csv(PRIZEPICKS_DATA_FILE)
    unique_players = df[['Player', 'Team']].drop_duplicates()
    return unique_players

# 📌 Step 2: Standardize Team Names & Track Injury Status
def standardize_injured_teams():
    df = pd.read_csv(INJURED_STARTERS_FILE)

    # ✅ Map team names to match PrizePicks data
    df["Team"] = df["Team"].map(TEAM_NAME_MAPPING)

    # ✅ Create dictionaries to track Out & Day-To-Day players
    out_players = set(df[df["Status"] == "Out"]["Name"].tolist())
    injured_status_dict = {row["Name"]: row["Status"] for _, row in df.iterrows()}

    return df[['Name', 'Team']], injured_status_dict, out_players

# 📌 Step 3 & 4: Match Healthy Players with Injured Teammates
def get_matched_players():
    healthy_players_df = extract_unique_players()
    injured_players_df, injured_status_dict, out_players = standardize_injured_teams()

    # Merge healthy players with injured teammates on the same team
    merged_df = healthy_players_df.merge(injured_players_df, on="Team", how="left")

    # Drop rows where "Injured Player" is missing (means no injured teammate)
    merged_df = merged_df.dropna(subset=["Name"]).rename(columns={"Name": "Injured Player"})

    # ✅ Append "(Day-To-Day)" to injured player names if needed
    merged_df["Injured Player"] = merged_df["Injured Player"].apply(
        lambda x: f"{x} (Day-To-Day)" if injured_status_dict.get(x) == "Day-To-Day" else x
    )

    # ✅ Remove players who are marked as "Out" from final output
    merged_df = merged_df[~merged_df["Player"].isin(out_players)]

    return merged_df.sort_values(by=["Team", "Player"])

# 📌 Fetch Stats from StatMuse
async def fetch_stats(session, player, injured_player):
    # ✅ Remove "(Day-To-Day)" from the search query
    injured_player_clean = injured_player.replace(" (Day-To-Day)", "")

    # ✅ Ensure player is not searching for themselves
    if player == injured_player_clean:
        logging.warning(f"Skipping self-search: {player} without {injured_player}")
        return {}

    url = f"https://www.statmuse.com/nba/ask?q={player}+in+the+2024-25+season+in+games+without+{injured_player_clean.replace(' ', '+')}"

    async with session.get(url) as response:
        if response.status == 200:
            html = await response.text()
            return parse_stats(html)
        else:
            logging.warning(f"Failed to fetch stats for {player} without {injured_player_clean}")
            return {}

# 📌 Parse Stats from HTML (Extract Second-to-Last Row for Averages)
def parse_stats(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    if not table:
        return {}

    rows = table.find_all("tr")
    if len(rows) < 3:  # Ensure there's enough data
        return {}

    # Extract headers from the table
    headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]

    # ✅ Extract the **second-to-last row** (which contains the Averages)
    avg_row = rows[-2].find_all("td")
    values = [td.get_text(strip=True) for td in avg_row]

    return {headers[i]: values[i] if i < len(values) else "N/A" for i in range(len(headers))}

# 📌 Process Players and Fetch Stats
async def process_players():
    matched_players_df = get_matched_players()
    stats_data = []

    async with aiohttp.ClientSession() as session:
        tasks = []
        player_queries = []

        for _, row in matched_players_df.iterrows():
            player = row["Player"]
            injured_player = row["Injured Player"]
            team = row["Team"]

            # ✅ Add tasks to fetch stats
            tasks.append(fetch_stats(session, player, injured_player))
            player_queries.append((player, injured_player, team))

        results = await asyncio.gather(*tasks)

        for (player, injured_player, team), stats in zip(player_queries, results):
            if stats:
                csv_row = [player, injured_player, team, "2024-25"]

                # Add stats to row, ensuring it matches the required headers
                for stat in HEADERS[4:]:
                    csv_row.append(stats.get(stat, "N/A"))

                stats_data.append(csv_row)

    return stats_data

# 📌 Save Data to CSV
def save_to_csv(data):
    df = pd.DataFrame(data, columns=HEADERS)
    df = df.sort_values(by=["Team", "Player"])  # ✅ Sort by team & player name
    df.to_csv(OUTPUT_CSV_FILE, index=False)
    logging.info(f"✅ Saved results to {OUTPUT_CSV_FILE}")

# 📌 Main Function
async def main():
    stats_data = await process_players()

    if stats_data:
        save_to_csv(stats_data)
    else:
        logging.info("⚠️ No stats were retrieved.")

# 📌 Run the script
if __name__ == "__main__":
    asyncio.run(main())

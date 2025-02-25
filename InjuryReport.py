import aiohttp
import asyncio
import pandas as pd
from bs4 import BeautifulSoup

# ✅ Fetch injury data and save to CSV
async def fetch_injury_data_aiohttp():
    url = "https://www.espn.com/nba/injuries"
    headers = {"User-Agent": "Mozilla/5.0"}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                print(f"Failed to fetch data. Status code: {response.status}")
                return []
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")

    injuries = []
    teams = soup.select(".Table__Title")  # Select team names
    tables = soup.select("table.Table tbody")  # Select all injury tables

    for team, table in zip(teams, tables):
        team_name = team.get_text(strip=True)
        rows = table.find_all("tr")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) >= 4:  # Ensure the row has enough columns
                player_name = cells[0].get_text(strip=True)
                status = cells[3].get_text(strip=True)
                injuries.append((player_name, team_name, status))

    return injuries

def filter_injured_starters(injury_csv="nba_injuries.csv", lineup_csv="starting_lineups.csv", output_csv="injured_starters.csv"):
    """
    Filters the NBA injury report to only include injured players who are in the starting lineups.

    Args:
    - injury_csv (str): Path to the injuries CSV file.
    - lineup_csv (str): Path to the starting lineups CSV file.
    - output_csv (str): Path where the filtered injured starters CSV will be saved.
    """
    # Load data
    injuries_df = pd.read_csv(injury_csv)
    starting_lineups_df = pd.read_csv(lineup_csv)

    # Ensure column names are properly formatted
    injuries_df.columns = injuries_df.columns.str.strip()
    starting_lineups_df.columns = starting_lineups_df.columns.str.strip()

    # Flatten the starting lineup DataFrame to get a list of all starters
    starter_players = set(starting_lineups_df.melt(id_vars=["Team"], var_name="Position", value_name="Player")["Player"])

    # Filter injuries to only include players who are starters
    injured_starters_df = injuries_df[injuries_df["Name"].isin(starter_players)]

    # Save to CSV
    injured_starters_df.to_csv(output_csv, index=False)
    print(f"✅ Injured starters list saved to {output_csv}")

    return injured_starters_df

# ✅ Save the injury data to CSV
def save_injury_data_to_csv(injuries, filename="nba_injuries.csv"):
    df = pd.DataFrame(injuries, columns=["Name", "Team", "Status"])
    df.to_csv(filename, index=False)
    print(f"✅ Injury data saved to {filename}")

# ✅ Main async function
async def main():
    # Fetch latest injuries
    injuries = await fetch_injury_data_aiohttp()

    # Save injuries to CSV
    injury_csv = "nba_injuries.csv"
    save_injury_data_to_csv(injuries, injury_csv)

    # Path to starting lineups CSV (make sure it exists)
    lineup_csv = "starting_lineups.csv"

    # Filter and save only injured starters
    filter_injured_starters(injury_csv, lineup_csv, "injured_starters.csv")

if __name__ == '__main__':
    asyncio.run(main())


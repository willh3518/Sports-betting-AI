import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import json
import re

COOKIE_FILE = "statmusecookies.json"

# Selenium setup
def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    service = Service("/Users/willhart/Downloads/chromedriver-mac-arm64/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def load_specific_cookie(driver, cookie_file, cookie_name):
    """Load and apply a specific cookie (e.g., 'sm_session')."""
    with open(cookie_file, "r") as file:
        cookies = json.load(file)
        for cookie in cookies:
            if cookie["name"] == cookie_name:
                if "domain" in cookie and cookie["domain"].startswith("."):
                    cookie["domain"] = cookie["domain"].lstrip(".")
                cookie.pop("storeId", None)
                cookie.pop("sameSite", None)
                cookie.pop("session", None)
                driver.add_cookie(cookie)
                break

def parse_stats_text(stats_text):
    """
    Parse stats text to extract points, assists, rebounds, blocks, and games played.
    Handles variations in text formatting, including single-game stats.
    """
    try:
        # Enhanced regex to handle single-game stats or standard stats
        match = re.search(
            r"(?=.*?(\d+\.\d+)\s+points)?(?=.*?(\d+\.\d+)\s+assists)?(?=.*?(\d+\.\d+)\s+rebounds)?(?=.*?(\d+\.\d+)\s+blocks)?.*?in\s+(\d+)\s+game[s]?",
            stats_text,
            re.IGNORECASE
        )

        if match:
            points = float(match.group(1)) if match.group(1) else None
            assists = float(match.group(2)) if match.group(2) else None
            rebounds = float(match.group(3)) if match.group(3) else None
            blocks = float(match.group(4)) if match.group(4) else None
            games = int(match.group(5)) if match.group(5) else None

            return {
                "Points": points,
                "Assists": assists,
                "Rebounds": rebounds,
                "Blocks": blocks,
                "Games Played": games,
            }

        # Log unparsed stats text for debugging
        print(f"Could not parse stats text: {stats_text}")
        return {"Points": None, "Assists": None, "Rebounds": None, "Blocks": None, "Games Played": None}
    except Exception as e:
        print(f"Error parsing stats text: {e}")
        return {"Points": None, "Assists": None, "Rebounds": None, "Blocks": None, "Games Played": None}

def search_player_stats(driver, player_name, team_name, exclude_player):
    """Perform a search on StatMuse for a player's stats on a specific team this season, excluding another player."""
    search_query = f"{player_name} stats this season on the {team_name} without {exclude_player}"
    print(f"Searching: {search_query}")
    try:
        driver.get("https://www.statmuse.com/")
        time.sleep(3)

        # Load the saved cookie to stay logged in
        load_specific_cookie(driver, COOKIE_FILE, "sm_session")
        driver.refresh()
        time.sleep(5)  # Allow session to reload after applying the cookie

        # Find the search bar and enter the query
        search_bar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[placeholder='Search players, stats or odds']"))
        )
        search_bar.clear()
        search_bar.send_keys(search_query + Keys.RETURN)
        time.sleep(5)  # Allow time for results to load

        # Locate the stats
        stats_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span[contains(@class, 'text-pretty')]"))
        )
        stats_text = stats_element.text.strip()
        print(f"Raw stats text: {stats_text}")

        # Parse the stats text
        parsed_stats = parse_stats_text(stats_text)
        if parsed_stats:
            print(f"Parsed Stats: {parsed_stats}")
            return parsed_stats
        else:
            print(f"Could not parse stats for {player_name} this season on the {team_name} without {exclude_player}")
            return {"Points": None, "Assists": None, "Rebounds": None, "Games Played": None}
    except Exception as e:
        print(f"Error fetching stats for {player_name} this season on the {team_name} without {exclude_player}: {e}")
        return {"Points": None, "Assists": None, "Rebounds": None, "Games Played": None}

def fetch_non_injured_players(csv_file):
    """Fetch non-injured players from the combined CSV."""
    df = pd.read_csv(csv_file)
    non_injured_df = df[df['Injury Status'] == 'Healthy']  # Filter non-injured players
    return non_injured_df

def fetch_injured_players(csv_file):
    """Fetch injured players from the combined CSV."""
    df = pd.read_csv(csv_file)
    injured_df = df[df['Injury Status'] == 'Injured']  # Filter injured players
    return injured_df

def search_stats_for_players(non_injured_players, injured_players, output_file):
    """Search for stats for each non-injured player, excluding each injured player individually."""
    driver = setup_driver()
    results = []

    # Iterate through each non-injured player
    for index, row in non_injured_players.iterrows():
        team = row['Team']
        player_name = row['Player']

        # Get all injured players for the same team
        excluded_players = injured_players[injured_players['Team'] == team]['Player'].tolist()

        # Perform a search for each excluded player
        for exclude_player in excluded_players:
            stats = search_player_stats(driver, player_name, team, exclude_player)
            if stats:
                results.append({
                    'Team': team,
                    'Player': player_name,
                    'Excluded Player': exclude_player,
                    'Points': stats['Points'],
                    'Assists': stats['Assists'],
                    'Rebounds': stats['Rebounds'],
                    'Games Played': stats['Games Played']
                })

    # Save results to a CSV file
    driver.quit()
    results_df = pd.DataFrame(results)
    results_df.to_csv(output_file, index=False)
    print(f"Player stats saved to '{output_file}'.")

def main():
    combined_csv_file = "combined_starters.csv"  # Input combined CSV file
    output_stats_file = "player_stats.csv"  # Output stats file

    # Fetch non-injured players and injured players
    non_injured_players = fetch_non_injured_players(combined_csv_file)
    injured_players = fetch_injured_players(combined_csv_file)

    # Perform searches and save stats
    search_stats_for_players(non_injured_players, injured_players, output_stats_file)

if __name__ == '__main__':
    main()

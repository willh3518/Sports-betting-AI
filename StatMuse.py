from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import pandas as pd
import time
import re
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo
from fuzzywuzzy import process

# Selenium setup
chrome_options = Options()
service = Service("/Users/willhart/Downloads/chromedriver-mac-arm64/chromedriver")  # Update with your ChromeDriver path
COOKIE_FILE = "statmusecookies.json"

# Load all NBA players for searching
nba_players = players.get_players()

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

def clean_player_name(name):
    """Clean player names by removing extraneous characters like jersey numbers."""
    return re.sub(r"#\d+|\s+\d+$", "", name).strip()

def search_player_in_nba_api(player_name):
    """Search for a player in the NBA API using fuzzy matching."""
    nba_player_names = [player['full_name'] for player in nba_players]
    match = process.extractOne(player_name, nba_player_names, score_cutoff=80)  # Match with a threshold of 80%
    if match:
        matched_name = match[0]
        player = next(player for player in nba_players if player['full_name'] == matched_name)
        return player  # Return full player object
    return None  # No match found

def get_player_position(player_id, retries=3):
    """Get a player's position using the NBA API's commonplayerinfo endpoint with retry logic."""
    for attempt in range(retries):
        try:
            player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id, timeout=60)
            player_data = player_info.get_data_frames()[0]
            return player_data['POSITION'][0]  # Extract the position
        except Exception as e:
            print(f"Error retrieving position for player ID {player_id} (Attempt {attempt + 1}/{retries}): {e}")
            time.sleep(2)  # Wait 2 seconds before retrying
    return "Unknown"  # Return "Unknown" after all retries fail

def add_positions_to_csv(input_csv, output_csv):
    """Add player positions to the CSV file and sort by position."""
    try:
        # Load the CSV file
        df = pd.read_csv(input_csv)

        # Normalize and clean player names
        df['Player Name'] = (
            df['Player Name']
            .str.strip()
            .apply(clean_player_name)  # Clean jersey numbers and extraneous characters
        )

        # Add a new column for positions
        def fetch_position(name):
            player_info = search_player_in_nba_api(name)
            if player_info:
                time.sleep(1)  # Add a 1-second delay between requests
                return get_player_position(player_info['id'])
            return "Player Not Found"

        # Apply the position fetching logic
        for index, row in df.iterrows():
            df.at[index, 'Position'] = fetch_position(row['Player Name'])

            # Save progress after every row
            if index % 10 == 0:  # Save every 10 rows
                print(f"Saving progress at row {index}...")
                df.to_csv(output_csv, index=False)

        # Sort the DataFrame by the Position column
        df = df.sort_values(by='Position', ascending=True)

        # Save the final sorted DataFrame
        df.to_csv(output_csv, index=False)
        print(f"Updated CSV with player positions saved to '{output_csv}'. Sorted by position.")
    except Exception as e:
        print(f"Error adding positions to CSV: {e}")

def calculate_average_points_by_role_and_position(input_csv, output_csv):
    """
    Calculate the average points by position and role (Starter/Bench) and save to a new CSV.
    """
    try:
        # Load the input CSV
        df = pd.read_csv(input_csv)

        # Ensure numeric type for Points
        df['Points'] = pd.to_numeric(df['Points'], errors='coerce')

        # Group by Position and Role, then calculate average points
        avg_points = (
            df.groupby(['Position', 'Role'], as_index=False)
            .agg({'Points': 'mean'})
            .rename(columns={'Points': 'Average Points'})
        )

        # Round the average points to 2 decimal places
        avg_points['Average Points'] = avg_points['Average Points'].round(2)

        # Save the resulting DataFrame to the output CSV
        avg_points.to_csv(output_csv, index=False)
        print(f"Average points by position and role saved to '{output_csv}'.")
    except Exception as e:
        print(f"Error calculating average points: {e}")

def main():
    # Your existing code here...
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.statmuse.com/")
    time.sleep(3)

    # Load session cookie to stay logged in
    load_specific_cookie(driver, COOKIE_FILE, "sm_session")
    driver.refresh()
    time.sleep(5)

    # Static search query for Thunder games
    search_query = "Thunder box score last 10 games"
    print(f"Performing static search query: {search_query}")

    # Dictionary to store stats for all games
    all_game_stats = {}

    for game_index in range(10):  # Loop through 10 games
        print(f"\nProcessing game {game_index + 1}...")

        # Perform the search again at the start of each iteration
        try:
            search_bar = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "textarea[placeholder='Search players, stats or odds']"))
            )
            search_bar.clear()
            search_bar.send_keys(search_query, Keys.RETURN)
            time.sleep(5)
        except Exception as e:
            print(f"Error performing search: {e}")
            break

        # Locate and click the "Final" button for the current game
        try:
            final_buttons = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(text(), 'Final')]"))
            )
            if game_index < len(final_buttons):
                final_buttons[game_index].click()
                print(f"Successfully clicked the 'Final' button for game {game_index + 1}.")
                time.sleep(5)  # Pause to allow the page to load
            else:
                print("No more 'Final' buttons available. Exiting loop.")
                break
        except Exception as e:
            print(f"Error clicking 'Final' button for game {game_index + 1}: {e}")
            continue

        # Dynamically detect the opposing team name
        try:
            title_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//title"))
            )
            title_text = title_element.get_attribute("innerText")
            print(f"Raw title text: {title_text}")

            # Adjusted regex to handle both formats (Thunder win or lose)
            match = re.search(r"(Thunder) \d+-\d+ (.+?) \(|(.+?) \d+-\d+ Thunder", title_text)
            if match:
                opponent_name = match.group(2) or match.group(3)  # Extract the opponent name
                print(f"Detected opposing team: {opponent_name.strip()}")
                opponent_name = opponent_name.strip()
            else:
                raise ValueError("Unexpected title format. Could not parse team names.")
        except Exception as e:
            print(f"Error detecting opposing team: {e}")
            continue

        # Locate and click the button for the opposing team
        try:
            team_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//label[contains(text(), '{opponent_name}')]")
                )
            )
            team_button.click()
            print(f"Successfully clicked the '{opponent_name}' button.")
            time.sleep(5)  # Allow the stats table to load
        except Exception as e:
            print(f"Error clicking opponent's button: {e}")
            continue

        # Extract player stats and assign hard-coded roles based on order
        try:
            player_rows = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr"))
            )
            print(f"Extracting player stats for game {game_index + 1}...")

            game_stats = {}
            starter_count = 0  # Counter to track starters

            for row in player_rows:
                try:
                    # Extract player name and points
                    name = row.find_element(By.XPATH, ".//td[1]").text.strip()
                    points = row.find_element(By.XPATH, ".//td[3]").text.strip()

                    if name and points:
                        # Assign "Starter" to the first 5 players, then "Bench"
                        role = "Starter" if starter_count < 5 else "Bench"
                        game_stats[name] = {"Points": points, "Role": role}

                        # Increment the starter counter only if the role is "Starter"
                        starter_count += 1
                except Exception as e:
                    print(f"Error parsing row: {e}")

            # Store stats for the current game
            all_game_stats[f"Game {game_index + 1}"] = game_stats
            print(f"Game {game_index + 1} stats: {game_stats}")

        except Exception as e:
            print(f"Error extracting stats for game {game_index + 1}: {e}")
            continue

    # Save all extracted stats to a CSV
    try:
        csv_file = "opponent_stats_last_10_games.csv"
        df = pd.DataFrame.from_dict(all_game_stats, orient="index").transpose()
        df.index.name = "Player Name"  # Add a title for the player names column

        # Convert the dictionary to a DataFrame and reset the index for sorting
        df = pd.DataFrame([
            {"Game": game, "Player Name": player, **stats}
            for game, players in all_game_stats.items()
            for player, stats in players.items()
        ])

        # Ensure sorting is applied
        df = df.sort_values(by=["Role", "Position"], ascending=[True, True])

        # Save the sorted DataFrame to CSV
        df.to_csv(csv_file, index=False)
        print(f"\nAll game stats saved to '{csv_file}' and sorted by role and position.")
    except Exception as e:
        print(f"Error saving stats to CSV: {e}")

    # Add positions to the CSV
    add_positions_to_csv(csv_file, "player_positions_last_10_games.csv")

    # Calculate average points by position and role
    calculate_average_points_by_role_and_position(
        input_csv="player_positions_last_10_games.csv",
        output_csv="average_points_by_position_and_role.csv"
    )

    driver.quit()

if __name__ == "__main__":
    main()

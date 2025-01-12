import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import logging
from nba_api.stats.endpoints import leaguegamelog
from nba_api.stats.static import players

# Setup logging for debugging and error reporting
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

# Fetch all game logs for the season in one batch
def fetch_all_game_logs(season='2023-24'):
    try:
        print("Fetching all game logs...")
        league_logs = leaguegamelog.LeagueGameLog(season=season)
        all_logs = league_logs.get_data_frames()[0]
        print("All game logs fetched successfully.")
        logging.debug(f"all_logs columns: {all_logs.columns}")
        logging.debug(f"Sample rows from all_logs:\n{all_logs.head()}")
        return all_logs
    except Exception as e:
        logging.error(f"Error fetching all game logs: {e}")
        return pd.DataFrame()

# Analyze props for a specific player
def analyze_player_props(player_name, prop_type, prop_value, all_logs):
    try:
        print(f"Analyzing props for {player_name} - {prop_type}")
        logging.debug(f"Analyzing props for {player_name} - {prop_type} - {prop_value}")

        # Fetch player ID and filter logs
        player_data = players.find_players_by_full_name(player_name)
        if not player_data:
            print(f"Player {player_name} not found in NBA API.")
            logging.debug(f"Player {player_name} not found in NBA API.")
            return None, None, None, None
        else:
            player_id = player_data[0]['id']
            print(f"Resolved Player ID for {player_name}: {player_id}")
            logging.debug(f"Resolved Player ID for {player_name}: {player_id}")

        # Inspect the columns of all_logs
        print("Inspecting all_logs columns...")
        logging.debug(f"all_logs columns: {all_logs.columns}")

        # Determine the correct column for PLAYER_ID
        if 'PLAYER_ID' in all_logs.columns:
            id_column = 'PLAYER_ID'
        elif 'Player_ID' in all_logs.columns:
            id_column = 'Player_ID'
        else:
            print("PLAYER_ID column not found in all_logs. Please verify column names.")
            logging.error("PLAYER_ID column not found in all_logs.")
            return None, None, None, None

        # Filter game logs for this player
        player_logs = all_logs[all_logs[id_column] == player_id]
        if player_logs.empty:
            print(f"No game logs found for {player_name} (ID: {player_id})")
            logging.debug(f"No game logs found for {player_name} (ID: {player_id})")
            return None, None, None, None
        else:
            print(f"Game logs found for {player_name} (ID: {player_id}): {len(player_logs)} games")
            logging.debug(f"Game logs for {player_name}:\n{player_logs.head()}")

        # Take the last 15 games
        recent_15_games = player_logs.head(15)

        # Analyze based on prop type
        if 'Points' in prop_type:
            stat_avg = recent_15_games['PTS'].mean()
            over_hits = (recent_15_games['PTS'] > prop_value).sum()
        elif 'Rebounds' in prop_type:
            stat_avg = recent_15_games['REB'].mean()
            over_hits = (recent_15_games['REB'] > prop_value).sum()
        elif 'Assists' in prop_type:
            stat_avg = recent_15_games['AST'].mean()
            over_hits = (recent_15_games['AST'] > prop_value).sum()
        elif 'Turnovers' in prop_type:
            stat_avg = recent_15_games['TOV'].mean()
            over_hits = (recent_15_games['TOV'] > prop_value).sum()
        else:
            print(f"Unsupported prop type: {prop_type}")
            logging.debug(f"Unsupported prop type: {prop_type}")
            return None, None, None, None

        total_games = len(recent_15_games)
        likelihood = round((over_hits / total_games) * 100, 2) if total_games > 0 else 0.0

        return round(stat_avg, 2), over_hits, total_games, likelihood

    except Exception as e:
        logging.error(f"Error analyzing player {player_name}: {e}")
        return None, None, None, None

# Scrape props data from the PrizePicks website
def scrape_props(driver):
    print("Scraping props data...")
    try:
        # Locate all prop filter buttons initially
        filter_buttons = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.stat"))
        )
        print(f"Found {len(filter_buttons)} filter buttons.")

        # Track visited filters
        visited_filters = set()
        all_props = []

        # Loop through each filter button
        for i in range(len(filter_buttons)):
            try:
                # Re-fetch filter buttons dynamically
                filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button.stat")
                button = filter_buttons[i]

                # Get the filter name
                filter_name = button.text.strip()
                if filter_name in visited_filters:
                    continue  # Skip already visited filters
                visited_filters.add(filter_name)

                print(f"Scraping data for: {filter_name}")

                # Scroll the button into view
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
                time.sleep(1)

                # Click using JavaScript
                driver.execute_script("arguments[0].click();", button)
                time.sleep(5)

                # Fetch player containers
                player_containers = WebDriverWait(driver, 60).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='grid'][class*='grid-rows']"))
                )

                # Scrape data for each player
                for container in player_containers:
                    try:
                        # Extract player name
                        player_name_element = container.find_element(By.CSS_SELECTOR, "h3[id='test-player-name']")
                        player_name = player_name_element.text if player_name_element else "N/A"

                        # Extract prop value
                        prop_value_element = container.find_element(By.CSS_SELECTOR, "div[class='heading-md']")
                        prop_value = float(prop_value_element.text) if prop_value_element else 0.0

                        # Extract prop type
                        prop_type_element = container.find_element(By.CSS_SELECTOR, "span[class='break-words']")
                        prop_type = prop_type_element.text if prop_type_element else "N/A"

                        all_props.append({
                            'Player': player_name,
                            'Filter': filter_name,
                            'Prop Type': prop_type,
                            'Prop Value': prop_value
                        })
                    except Exception as e:
                        logging.error(f"Error scraping player container: {e}")
                        continue

            except Exception as e:
                logging.error(f"Error handling filter button {i}: {e}")
                continue

        print("Props scraping completed.")
        return pd.DataFrame(all_props)

    except Exception as e:
        logging.error(f"Error scraping props data: {e}")
        return pd.DataFrame()

# Main function to orchestrate everything
def main():
    # Initialize WebDriver
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = uc.Chrome(options=options)

    # Access PrizePicks website
    url = 'https://app.prizepicks.com/'
    driver.get(url)
    input("Solve CAPTCHA manually and press Enter to continue...")

    # Scrape props data
    props_df = scrape_props(driver)

    # Fetch all game logs in one batch
    all_logs = fetch_all_game_logs()

    # Analyze props
    analyzed_props = []
    for _, row in props_df.iterrows():
        player_name = row['Player']
        prop_type = row['Prop Type']
        prop_value = row['Prop Value']
        stat_avg, over_hits, total_games, likelihood = analyze_player_props(player_name, prop_type, prop_value, all_logs)
        analyzed_props.append({
            'Player': player_name,
            'Prop Type': prop_type,
            'Prop Value': round(prop_value, 2),
            'Avg Last 15': stat_avg,
            'Over Hits': over_hits,
            'Games Played': total_games,
            'Likelihood (%)': likelihood
        })

    # Save to CSV
    analyzed_df = pd.DataFrame(analyzed_props).sort_values(by='Likelihood (%)', ascending=False)
    csv_file_path = '/Users/willhart/Downloads/prizepicks_debugged_analysis.csv'
    analyzed_df.to_csv(csv_file_path, index=False)
    print(f"Data saved to {csv_file_path}")

    # Close the WebDriver
    driver.quit()

if __name__ == "__main__":
    main()

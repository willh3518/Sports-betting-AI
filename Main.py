import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import logging
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players

# Setup logging for debugging and error reporting
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

# Player logs cache for efficiency
player_logs_cache = {}

def fetch_cached_game_logs(player_id):
    if player_id in player_logs_cache:
        return player_logs_cache[player_id]
    else:
        logs = playergamelog.PlayerGameLog(player_id=player_id, season='2024-25').get_data_frames()[0]
        player_logs_cache[player_id] = logs
        return logs

def analyze_player_props(player_name, prop_type, prop_value):
    try:
        print(f"Analyzing props for {player_name} - {prop_type}")

        # Check if this is a combined prop
        if "+" in player_name:
            players_involved = [name.strip() for name in player_name.split("+")]
            print(f"Combined players detected: {players_involved}")

            # Initialize combined stats
            combined_stat_avg = 0
            combined_over_hits = 0
            total_games = 0

            for single_player in players_involved:
                single_stat_avg, single_over_hits, single_games_played, _ = analyze_player_props(
                    single_player, prop_type, prop_value
                )
                if single_stat_avg is None:
                    print(f"Could not fetch stats for {single_player}")
                    return None, None, None, None

                # Combine the stats
                combined_stat_avg += single_stat_avg * single_games_played
                combined_over_hits += single_over_hits
                total_games += single_games_played

            # Finalize combined stats
            combined_stat_avg = round(combined_stat_avg / total_games, 2) if total_games > 0 else None
            likelihood = round((combined_over_hits / total_games) * 100, 2) if total_games > 0 else 0.0

            return combined_stat_avg, combined_over_hits, total_games, likelihood

        player_data = players.find_players_by_full_name(player_name)
        if not player_data:
            return None, None, None, None

        player_id = player_data[0]['id']
        game_logs = fetch_cached_game_logs(player_id)
        recent_15_games = game_logs.iloc[:15]

        if 'Pts+Rebs+Asts' in prop_type:
            combined = recent_15_games['PTS'] + recent_15_games['REB'] + recent_15_games['AST']
            stat_avg = combined.mean()
            over_hits = (combined > prop_value).sum()
        elif 'Pts+Rebs' in prop_type:
            combined = recent_15_games['PTS'] + recent_15_games['REB']
            stat_avg = combined.mean()
            over_hits = (combined > prop_value).sum()
        elif 'Pts+Asts' in prop_type:
            combined = recent_15_games['PTS'] + recent_15_games['AST']
            stat_avg = combined.mean()
            over_hits = (combined > prop_value).sum()
        elif 'Rebs+Asts' in prop_type:
            combined = recent_15_games['REB'] + recent_15_games['AST']
            stat_avg = combined.mean()
            over_hits = (combined > prop_value).sum()
        elif 'Offensive Rebounds' in prop_type:
            stat_avg = recent_15_games['OREB'].mean()
            over_hits = (recent_15_games['OREB'] > prop_value).sum()
        elif 'Defensive Rebounds' in prop_type:
            stat_avg = recent_15_games['DREB'].mean()
            over_hits = (recent_15_games['DREB'] > prop_value).sum()
        elif 'Points' in prop_type:
            stat_avg = recent_15_games['PTS'].mean()
            over_hits = (recent_15_games['PTS'] > prop_value).sum()
        elif 'Rebounds' in prop_type:
            stat_avg = recent_15_games['REB'].mean()
            over_hits = (recent_15_games['REB'] > prop_value).sum()
        elif 'Assists' in prop_type:
            stat_avg = recent_15_games['AST'].mean()
            over_hits = (recent_15_games['AST'] > prop_value).sum()
        elif 'Blocked Shots' in prop_type:
            stat_avg = recent_15_games['BLK'].mean()
            over_hits = (recent_15_games['BLK'] > prop_value).sum()
        elif '3-PT Made' in prop_type:
            stat_avg = recent_15_games['FG3M'].mean()
            over_hits = (recent_15_games['FG3M'] > prop_value).sum()
        elif '3-PT Attempted' in prop_type:
            stat_avg = recent_15_games['FG3A'].mean()
            over_hits = (recent_15_games['FG3A'] > prop_value).sum()
        elif 'FG Attempted' in prop_type:
            stat_avg = recent_15_games['FGA'].mean()
            over_hits = (recent_15_games['FGA'] > prop_value).sum()
        elif 'FG Made' in prop_type:
            stat_avg = recent_15_games['FGM'].mean()
            over_hits = (recent_15_games['FGM'] > prop_value).sum()
        elif 'Free Throws Made' in prop_type:
            stat_avg = recent_15_games['FTM'].mean()
            over_hits = (recent_15_games['FTM'] > prop_value).sum()
        elif 'Fantasy Score' in prop_type:
            fantasy_scores = (
                recent_15_games['PTS'] +
                1.2 * recent_15_games['REB'] +
                1.5 * recent_15_games['AST'] +
                3 * recent_15_games['STL'] +
                3 * recent_15_games['BLK'] -
                recent_15_games['TOV']
            )
            stat_avg = fantasy_scores.mean()
            over_hits = (fantasy_scores > prop_value).sum()
        elif 'Steals' in prop_type:
            stat_avg = recent_15_games['STL'].mean()
            over_hits = (recent_15_games['STL'] > prop_value).sum()
        elif 'Turnovers' in prop_type:
            stat_avg = recent_15_games['TOV'].mean()
            over_hits = (recent_15_games['TOV'] > prop_value).sum()
        elif 'Blocks+Steals' in prop_type:
            combined = recent_15_games['BLK'] + recent_15_games['STL']
            stat_avg = combined.mean()
            over_hits = (combined > prop_value).sum()
        else:
            return None, None, None, None

        total_games = len(recent_15_games)
        likelihood = round((over_hits / total_games) * 100, 2) if total_games > 0 else 0.0

        return round(stat_avg, 2), over_hits, total_games, likelihood

    except Exception as e:
        logging.error(f"Error analyzing player {player_name}: {e}")
        return None, None, None, None

def process_filter(driver, filter_buttons, index):
    try:
        # Refresh buttons to avoid stale element issues
        filter_buttons = driver.find_elements(By.CSS_SELECTOR, "button.stat")
        button = filter_buttons[index]

        # Get the filter name
        filter_name = button.text.strip()

        # Scroll the button into view and click
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
        driver.execute_script("arguments[0].click();", button)
        time.sleep(5)  # Wait for content to load
        return filter_name
    except Exception as e:
        logging.error(f"Error processing filter at index {index}: {e}")
        return None


def scrape_props(driver):
    all_props = []
    filter_buttons = WebDriverWait(driver, 60).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.stat"))
    )
    visited_filters = set()

    for i in range(len(filter_buttons)):
        filter_name = process_filter(driver, filter_buttons, i)
        if not filter_name or filter_name in visited_filters:
            continue  # Skip if already processed or an error occurred
        visited_filters.add(filter_name)

        player_containers = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[class*='grid'][class*='grid-rows']"))
        )

        for container in player_containers:
            try:
                player_name = container.find_element(By.CSS_SELECTOR, "h3[id='test-player-name']").text
                prop_value = float(container.find_element(By.CSS_SELECTOR, "div[class='heading-md']").text)
                prop_type = container.find_element(By.CSS_SELECTOR, "span[class='break-words']").text

                # Extract the opposing team properly
                opposing_team_element = container.find_element(By.CSS_SELECTOR, "time.text-soClean-140.body-sm")
                raw_text = opposing_team_element.text.strip()

                # Refine the logic to extract the team abbreviation (exclude 'vs')
                if "vs" in raw_text:
                    opposing_team = raw_text.split("vs")[1].strip().split()[0]
                else:
                    opposing_team = raw_text.split()[0]  # Fallback for unexpected cases

                stat_avg, over_hits, games_played, likelihood = analyze_player_props(player_name, prop_type, prop_value)

                all_props.append({
                    'Player': player_name,
                    'Prop Type': prop_type,
                    'Prop Value': round(prop_value, 2),
                    'Opposing Team': opposing_team,
                    'Avg Last 15': stat_avg,
                    'Over Hits': over_hits,
                    'Games Played': games_played,
                    'Likelihood (%)': likelihood
                })

            except Exception as e:
                logging.error(f"Error processing player container: {e}")
                continue

    return pd.DataFrame(all_props)


def main():
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.geolocation": 1  # 2 = Block location, 1 = Allow
    })
    driver = uc.Chrome(options=options)

    url = 'https://app.prizepicks.com/'
    driver.get(url)
    input("Solve CAPTCHA manually and press Enter to continue...")

    props_df = scrape_props(driver)
    if not props_df.empty:
        # Sort the DataFrame by Likelihood (%) in descending order
        props_df = props_df.sort_values(by='Likelihood (%)', ascending=False)

        # Save the sorted DataFrame to a CSV
        props_df.to_csv('prizepicks_sorted.csv', index=False)
        print("Data saved to 'prizepicks_sorted.csv'.")
    else:
        print("No data collected.")

    driver.quit()

if __name__ == "__main__":
    main()

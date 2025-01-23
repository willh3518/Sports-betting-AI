import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import logging
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.static import players
from nba_api.stats.endpoints import commonplayerinfo

# Setup logging for debugging and error reporting
logging.basicConfig(filename='debug.log', level=logging.DEBUG)

# Player logs cache for efficiency
player_logs_cache = {}

# Season logs cache to avoid redundant API calls
season_logs_cache = {}

def fetch_cached_game_logs(player_id, season):
    """
    Fetches and caches game logs for a player for a specific season.

    Args:
        player_id (int): The player's NBA ID.
        season (str): The season in 'YYYY-YY' format.

    Returns:
        pd.DataFrame: The player's game logs for the season.
    """
    cache_key = f"{player_id}_{season}"
    if cache_key in season_logs_cache:
        return season_logs_cache[cache_key]

    try:
        logs = playergamelog.PlayerGameLog(player_id=player_id, season=season).get_data_frames()[0]
        season_logs_cache[cache_key] = logs
        return logs
    except Exception as e:
        logging.error(f"Error fetching game logs for player {player_id} in season {season}: {e}")
        return pd.DataFrame()

def fetch_h2h_game_logs(player_id, opponent_team, seasons):
    """
    Fetches a player's head-to-head game logs for specific seasons against a specific opponent team.

    Args:
        player_id (int): The player's NBA ID.
        opponent_team (str): The opponent team's abbreviation.
        seasons (list): List of seasons in 'YYYY-YY' format.

    Returns:
        pd.DataFrame: A DataFrame containing the filtered head-to-head game logs.
    """
    h2h_logs = pd.DataFrame()
    for season in seasons:
        logs = fetch_cached_game_logs(player_id, season)
        if not logs.empty:
            filtered_logs = logs[logs['MATCHUP'].str.contains(opponent_team, na=False)]
            if not filtered_logs.empty:
                h2h_logs = pd.concat([h2h_logs, filtered_logs], ignore_index=True)
    return h2h_logs

def analyze_player_props(player_name, prop_type, prop_value):
    try:
        print(f"Analyzing props for {player_name} - {prop_type}")

        player_data = players.find_players_by_full_name(player_name)
        if not player_data:
            return None, None, None, None, None, None, None

        player_id = player_data[0]['id']
        game_logs = fetch_cached_game_logs(player_id, '2024-25')
        recent_15_games = game_logs.iloc[:15]  # Last 15 games
        season_logs = game_logs  # Full season logs

        # Initialize averages and hits
        stat_avg = None
        season_stat_avg = None
        over_hits = None
        season_hits = None

        # Analyze props
        if 'Pts+Rebs+Asts' in prop_type:
            combined = recent_15_games['PTS'] + recent_15_games['REB'] + recent_15_games['AST']
            season_combined = season_logs['PTS'] + season_logs['REB'] + season_logs['AST']
        elif 'Pts+Rebs' in prop_type:
            combined = recent_15_games['PTS'] + recent_15_games['REB']
            season_combined = season_logs['PTS'] + season_logs['REB']
        elif 'Pts+Asts' in prop_type:
            combined = recent_15_games['PTS'] + recent_15_games['AST']
            season_combined = season_logs['PTS'] + season_logs['AST']
        elif 'Rebs+Asts' in prop_type:
            combined = recent_15_games['REB'] + recent_15_games['AST']
            season_combined = season_logs['REB'] + season_logs['AST']
        elif 'Offensive Rebounds' in prop_type:
            combined = recent_15_games['OREB']
            season_combined = season_logs['OREB']
        elif 'Defensive Rebounds' in prop_type:
            combined = recent_15_games['DREB']
            season_combined = season_logs['DREB']
        elif 'Points' in prop_type:
            combined = recent_15_games['PTS']
            season_combined = season_logs['PTS']
        elif 'Rebounds' in prop_type:
            combined = recent_15_games['REB']
            season_combined = season_logs['REB']
        elif 'Assists' in prop_type:
            combined = recent_15_games['AST']
            season_combined = season_logs['AST']
        elif 'Blocked Shots' in prop_type:
            combined = recent_15_games['BLK']
            season_combined = season_logs['BLK']
        elif '3-PT Made' in prop_type:
            combined = recent_15_games['FG3M']
            season_combined = season_logs['FG3M']
        elif '3-PT Attempted' in prop_type:
            combined = recent_15_games['FG3A']
            season_combined = season_logs['FG3A']
        elif 'FG Attempted' in prop_type:
            combined = recent_15_games['FGA']
            season_combined = season_logs['FGA']
        elif 'FG Made' in prop_type:
            combined = recent_15_games['FGM']
            season_combined = season_logs['FGM']
        elif 'Free Throws Made' in prop_type:
            combined = recent_15_games['FTM']
            season_combined = season_logs['FTM']
        elif 'Fantasy Score' in prop_type:
            combined = (
                    recent_15_games['PTS'] +
                    1.2 * recent_15_games['REB'] +
                    1.5 * recent_15_games['AST'] +
                    3 * recent_15_games['STL'] +
                    3 * recent_15_games['BLK'] -
                    recent_15_games['TOV']
            )
            season_combined = (
                    season_logs['PTS'] +
                    1.2 * season_logs['REB'] +
                    1.5 * season_logs['AST'] +
                    3 * season_logs['STL'] +
                    3 * season_logs['BLK'] -
                    season_logs['TOV']
            )
        elif 'Steals' in prop_type:
            combined = recent_15_games['STL']
            season_combined = season_logs['STL']
        elif 'Turnovers' in prop_type:
            combined = recent_15_games['TOV']
            season_combined = season_logs['TOV']
        elif 'Blocks+Steals' in prop_type:
            combined = recent_15_games['BLK'] + recent_15_games['STL']
            season_combined = season_logs['BLK'] + season_logs['STL']
        else:
            # Unknown prop type
            return None, None, None, None, None, None, None

        # Calculate averages, hits, and percentages
        stat_avg = combined.mean()
        season_stat_avg = season_combined.mean()
        over_hits = (combined > prop_value).sum()
        season_hits = (season_combined > prop_value).sum()

        total_games = len(recent_15_games)
        total_season_games = len(season_logs)
        likelihood = round((over_hits / total_games) * 100, 2) if total_games > 0 else 0.0
        season_hit_percentage = round((season_hits / total_season_games) * 100, 2) if total_season_games > 0 else 0.0

        return (
            round(stat_avg, 2),
            over_hits,
            total_games,
            likelihood,
            round(season_stat_avg, 2),
            season_hits,
            season_hit_percentage
        )

    except Exception as e:
        logging.error(f"Error analyzing player {player_name}: {e}")
        return None, None, None, None, None, None, None

def analyze_h2h_props(player_id, opponent_team, prop_type, prop_value):
    """
    Analyzes the head-to-head performance of a player against a specific opponent team for a given prop.

    Args:
        player_id (int): The player's NBA ID.
        opponent_team (str): The opponent team's abbreviation.
        prop_type (str): The type of prop to analyze (e.g., "Points", "Rebounds").
        prop_value (float): The target prop value.

    Returns:
        tuple: H2H averages and hit rates for the past 3 seasons and the last 15 matchups.
    """
    try:
        current_season = '2024-25'
        past_seasons = ['2023-24', '2022-23', '2021-22']
        all_seasons = [current_season] + past_seasons

        h2h_logs = fetch_h2h_game_logs(player_id, opponent_team, all_seasons)

        # Determine which stat to analyze based on prop_type
        if 'Pts+Rebs+Asts' in prop_type:
            stat = h2h_logs['PTS'] + h2h_logs['REB'] + h2h_logs['AST']
        elif 'Pts+Rebs' in prop_type:
            stat = h2h_logs['PTS'] + h2h_logs['REB']
        elif 'Pts+Asts' in prop_type:
            stat = h2h_logs['PTS'] + h2h_logs['AST']
        elif 'Rebs+Asts' in prop_type:
            stat = h2h_logs['REB'] + h2h_logs['AST']
        elif 'Offensive Rebounds' in prop_type:
            stat = h2h_logs['OREB']
        elif 'Defensive Rebounds' in prop_type:
            stat = h2h_logs['DREB']
        elif 'Points' in prop_type:
            stat = h2h_logs['PTS']
        elif 'Rebounds' in prop_type:
            stat = h2h_logs['REB']
        elif 'Assists' in prop_type:
            stat = h2h_logs['AST']
        elif 'Blocked Shots' in prop_type:
            stat = h2h_logs['BLK']
        elif 'Steals' in prop_type:
            stat = h2h_logs['STL']
        elif 'Turnovers' in prop_type:
            stat = h2h_logs['TOV']
        elif 'Blocks+Steals' in prop_type:
            stat = h2h_logs['BLK'] + h2h_logs['STL']
        elif '3-PT Made' in prop_type:
            stat = h2h_logs['FG3M']
        elif 'Fantasy Score' in prop_type:
            stat = (
                h2h_logs['PTS'] +
                1.2 * h2h_logs['REB'] +
                1.5 * h2h_logs['AST'] +
                3 * h2h_logs['STL'] +
                3 * h2h_logs['BLK'] -
                h2h_logs['TOV']
            )
        elif '3-PT Attempted' in prop_type:
            stat = h2h_logs['FG3A']
        elif 'FG Attempted' in prop_type:
            stat = h2h_logs['FGA']
        elif 'FG Made' in prop_type:
            stat = h2h_logs['FGM']
        elif 'Free Throws Made' in prop_type:
            stat = h2h_logs['FTM']
        else:
            # Unknown prop type
            return None, None, None, None

        # Calculate stats for the last 15 matchups
        last_15_logs = stat.tail(15)
        last_15_avg = last_15_logs.mean() if not last_15_logs.empty else None
        last_15_hits = (last_15_logs > prop_value).sum() if not last_15_logs.empty else 0
        last_15_hit_rate = round((last_15_hits / len(last_15_logs)) * 100, 2) if not last_15_logs.empty else 0.0

        # Calculate stats for the past 3 seasons
        past_3_avg = stat.mean() if not stat.empty else None
        past_3_hits = (stat > prop_value).sum() if not stat.empty else 0
        past_3_hit_rate = round((past_3_hits / len(stat)) * 100, 2) if not stat.empty else 0.0

        return round(last_15_avg, 2), last_15_hit_rate, round(past_3_avg, 2), past_3_hit_rate

    except Exception as e:
        logging.error(f"Error analyzing H2H props for player {player_id}: {e}")
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
            continue
        visited_filters.add(filter_name)

        player_containers = WebDriverWait(driver, 60).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[class*='grid']"))
        )

        for container in player_containers:
            try:
                player_name = container.find_element(By.CSS_SELECTOR, "h3[id='test-player-name']").text
                prop_value = float(container.find_element(By.CSS_SELECTOR, "div[class='heading-md']").text)
                prop_type = container.find_element(By.CSS_SELECTOR, "span[class='break-words']").text

                # Extract the Opposing Team abbreviation
                raw_text = container.find_element(By.CSS_SELECTOR, "time.text-soClean-140.body-sm").text.strip()
                if "vs" in raw_text:
                    opposing_team = raw_text.split("vs")[1].strip().split()[0]
                else:
                    opposing_team = None

                player_data = players.find_players_by_full_name(player_name)
                if not player_data:
                    continue
                player_id = player_data[0]['id']

                # Check for Demon/Goblin images
                demon_goblin_images = container.find_elements(By.CSS_SELECTOR,"button img[alt='Demon'], button img[alt='Goblin']")
                if demon_goblin_images:
                    for img in demon_goblin_images:
                        alt = img.get_attribute("alt")
                        line_type = alt  # "Demon" or "Goblin"
                        print(f"{line_type} detected: {player_name} - {prop_type}")
                        # Add the Demon/Goblin line to the CSV without analyzing
                        all_props.append({
                            'Player': player_name,
                            'Prop Type': prop_type,
                            'Prop Value': round(prop_value, 2),
                            'Line Type': line_type,
                            'Opposing Team': opposing_team,
                            'Avg Last 15': None,
                            'Games Played': None,
                            'Likelihood (%)': None
                        })
                        break
                    continue  # Skip analysis for Demon/Goblin lines

                # Analyze general props
                stat_avg, over_hits, games_played, likelihood, season_stat_avg, season_hits, season_hit_percentage = analyze_player_props(
                    player_name, prop_type, prop_value
                )

                # Call analyze_h2h_props with all required arguments
                last_15_avg, last_15_hit_rate, past_3_avg, past_3_hit_rate = analyze_h2h_props(
                    player_id, opposing_team, prop_type, prop_value
                )

                # Append all stats to the list
                all_props.append({
                    'Player': player_name,
                    'Prop Type': prop_type,
                    'Prop Value': round(prop_value, 2),
                    'Line Type': "Regular",
                    'Opposing Team': opposing_team,
                    'Avg Last 15': stat_avg,
                    'Season Avg': season_stat_avg,
                    'Over Hits': over_hits,
                    'Games Played': games_played,
                    'Likelihood (%)': likelihood,
                    'Season Hits': season_hits,
                    'Season Hit %': season_hit_percentage,
                    'Last 15 H2H Avg': last_15_avg,
                    'Last 15 H2H Hit Rate (%)': last_15_hit_rate,
                    'Past 3 Seasons H2H Avg': past_3_avg,
                    'Past 3 Seasons H2H Hit Rate (%)': past_3_hit_rate
                })

            except Exception as e:
                print(f"Error processing player container: {e}")
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
        props_df = props_df.sort_values(by='Likelihood (%)', ascending=False)
        props_df.to_csv('prizepicks_sorted.csv', index=False)
        print("Data saved to 'prizepicks_sorted.csv'.")
    else:
        print("No data collected.")

    driver.quit()

if __name__ == "__main__":
    main()

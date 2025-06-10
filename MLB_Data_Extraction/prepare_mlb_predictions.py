# prepare_mlb_predictions.py
import pandas as pd
import numpy as np
import os
import datetime
import requests
import logging
from bs4 import BeautifulSoup
import time
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mlb_prep.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Config
MLB_DATA_DIR = "MLB_Prop_Data_CSV"
STATS_DIR = "MLB_Stats"
WEATHER_DIR = "MLB_Weather"
PROPS_DIR = "MLB_Props"
TODAY_DATE = datetime.datetime.now().strftime("%Y-%m-%d")

# Ensure directories exist
for directory in [MLB_DATA_DIR, STATS_DIR, WEATHER_DIR, PROPS_DIR]:
    os.makedirs(directory, exist_ok=True)

# File paths
HITTER_STATS_PATH = os.path.join(STATS_DIR, "hitter_stats_merged.csv")
PITCHER_STATS_PATH = os.path.join(STATS_DIR, "pitcher_stats_merged.csv")
WEATHER_PATH = os.path.join(WEATHER_DIR, "stadium_weather.csv")
PARK_FACTORS_PATH = os.path.join(STATS_DIR, "park_factors.csv")
PROPS_PATH = os.path.join(PROPS_DIR, f"{TODAY_DATE}_mlb_props.csv")
HITTER_PRED_PATH = os.path.join(MLB_DATA_DIR, "hitter_prediction_data.csv")
PITCHER_PRED_PATH = os.path.join(MLB_DATA_DIR, "pitcher_prediction_data.csv")


def fetch_todays_props():
    """Fetch today's MLB player props from sportsbooks"""
    logger.info("Fetching today's MLB player props...")

    # Check if we already have today's props
    if os.path.exists(PROPS_PATH):
        logger.info(f"Using existing props file: {PROPS_PATH}")
        return pd.read_csv(PROPS_PATH)

    # This would normally connect to a sportsbook API or scrape a website
    # For this example, we'll create a sample dataset

    # Sample teams playing today
    teams = [
        ("NYY", "BOS"), ("LAD", "SF"), ("CHC", "STL"),
        ("HOU", "TEX"), ("ATL", "NYM"), ("PHI", "WSH")
    ]

    # Sample players and props
    hitter_props = []
    pitcher_props = []

    # Generate sample start times throughout the day
    start_times = [
        f"{TODAY_DATE} 13:05:00", f"{TODAY_DATE} 16:10:00",
        f"{TODAY_DATE} 19:05:00", f"{TODAY_DATE} 19:10:00",
        f"{TODAY_DATE} 19:40:00", f"{TODAY_DATE} 20:15:00"
    ]

    # Generate sample hitter props
    hitter_names = [
        "Aaron Judge", "Rafael Devers", "Mookie Betts", "Buster Posey",
        "Kris Bryant", "Paul Goldschmidt", "Yordan Alvarez", "Marcus Semien",
        "Ronald Acuña Jr.", "Pete Alonso", "Bryce Harper", "Juan Soto"
    ]

    for i, name in enumerate(hitter_names):
        team_idx = i // 2
        if team_idx >= len(teams):
            break

        home_team = teams[team_idx][1]
        away_team = teams[team_idx][0]
        team = home_team if i % 2 else away_team
        opponent = away_team if i % 2 else home_team
        is_home = i % 2 == 0

        # Hits prop
        hitter_props.append({
            "Player": name,
            "Team": team,
            "Opponent": opponent,
            "Home": is_home,
            "Prop Type": "Hits",
            "Prop Value": 0.5 if random.random() < 0.3 else 1.5,
            "Over Odds": -110 - random.randint(0, 50),
            "Under Odds": -110 - random.randint(0, 50),
            "Start Time": start_times[team_idx],
            "Pitcher": f"Opponent Pitcher {i + 1}",
            "Pitcher Handedness": "right" if random.random() < 0.7 else "left"
        })

        # Total Bases prop
        hitter_props.append({
            "Player": name,
            "Team": team,
            "Opponent": opponent,
            "Home": is_home,
            "Prop Type": "Total Bases",
            "Prop Value": 1.5 if random.random() < 0.4 else 2.5,
            "Over Odds": -110 - random.randint(0, 50),
            "Under Odds": -110 - random.randint(0, 50),
            "Start Time": start_times[team_idx],
            "Pitcher": f"Opponent Pitcher {i + 1}",
            "Pitcher Handedness": "right" if random.random() < 0.7 else "left"
        })

    # Generate sample pitcher props
    pitcher_names = [
        "Gerrit Cole", "Chris Sale", "Clayton Kershaw", "Logan Webb",
        "Kyle Hendricks", "Jack Flaherty", "Justin Verlander", "Nathan Eovaldi",
        "Max Fried", "Jacob deGrom", "Aaron Nola", "Stephen Strasburg"
    ]

    for i, name in enumerate(pitcher_names):
        team_idx = i // 2
        if team_idx >= len(teams):
            break

        home_team = teams[team_idx][1]
        away_team = teams[team_idx][0]
        team = home_team if i % 2 else away_team
        opponent = away_team if i % 2 else home_team
        is_home = i % 2 == 0

        # Strikeouts prop
        pitcher_props.append({
            "Player": name,
            "Team": team,
            "Opponent": opponent,
            "Home": is_home,
            "Prop Type": "Pitcher Strikeouts",
            "Prop Value": 4.5 + random.randint(0, 4),
            "Over Odds": -110 - random.randint(0, 50),
            "Under Odds": -110 - random.randint(0, 50),
            "Start Time": start_times[team_idx]
        })

        # Earned Runs prop
        pitcher_props.append({
            "Player": name,
            "Team": team,
            "Opponent": opponent,
            "Home": is_home,
            "Prop Type": "Earned Runs Allowed",
            "Prop Value": 1.5 + (1 if random.random() < 0.5 else 0),
            "Over Odds": -110 - random.randint(0, 50),
            "Under Odds": -110 - random.randint(0, 50),
            "Start Time": start_times[team_idx]
        })

    # Combine all props
    all_props = pd.DataFrame(hitter_props + pitcher_props)

    # Save to file
    all_props.to_csv(PROPS_PATH, index=False)
    logger.info(f"Saved {len(all_props)} props to {PROPS_PATH}")

    return all_props


def load_player_stats():
    """Load player stats from files"""
    logger.info("Loading player stats...")

    try:
        hitter_stats = pd.read_csv(HITTER_STATS_PATH)
        logger.info(f"Loaded hitter stats with shape: {hitter_stats.shape}")
    except FileNotFoundError:
        logger.error(f"Hitter stats not found at {HITTER_STATS_PATH}")
        hitter_stats = pd.DataFrame()

    try:
        pitcher_stats = pd.read_csv(PITCHER_STATS_PATH)
        logger.info(f"Loaded pitcher stats with shape: {pitcher_stats.shape}")
    except FileNotFoundError:
        logger.error(f"Pitcher stats not found at {PITCHER_STATS_PATH}")
        pitcher_stats = pd.DataFrame()

    try:
        weather = pd.read_csv(WEATHER_PATH)
        logger.info(f"Loaded weather data with shape: {weather.shape}")
    except FileNotFoundError:
        logger.error(f"Weather data not found at {WEATHER_PATH}")
        weather = pd.DataFrame()

    try:
        park_factors = pd.read_csv(PARK_FACTORS_PATH)
        logger.info(f"Loaded park factors with shape: {park_factors.shape}")
    except FileNotFoundError:
        logger.error(f"Park factors not found at {PARK_FACTORS_PATH}")
        park_factors = pd.DataFrame()

    return hitter_stats, pitcher_stats, weather, park_factors


def prepare_hitter_data(props, hitter_stats, weather, park_factors):
    """Prepare hitter prediction data"""
    logger.info("Preparing hitter prediction data...")

    # Filter for hitter props
    hitter_props = [
        "Hits", "Runs", "RBIs", "Walks", "Hitter Strikeouts", "Total Bases",
        "Hits+Runs+RBIs", "Hits+Runs", "Runs+RBIs", "Hitter Fantasy Score"
    ]
    hitter_data = props[props["Prop Type"].isin(hitter_props)].copy()

    if len(hitter_data) == 0:
        logger.warning("No hitter props found")
        return pd.DataFrame()

    # Merge with hitter stats if available
    if not hitter_stats.empty:
        # Normalize player names for matching
        hitter_data["Player_Normalized"] = hitter_data["Player"].str.lower().str.replace(' jr.', '').str.replace(' sr.',
                                                                                                                 '')
        hitter_stats["Player_Normalized"] = hitter_stats["Player"].str.lower().str.replace(' jr.', '').str.replace(
            ' sr.', '')

        # Merge on normalized player name
        hitter_data = pd.merge(
            hitter_data,
            hitter_stats,
            on="Player_Normalized",
            how="left",
            suffixes=("", "_stats")
        )

        # Drop the normalized column
        hitter_data.drop("Player_Normalized", axis=1, inplace=True)

        # Keep the original player name
        if "Player_stats" in hitter_data.columns:
            hitter_data.drop("Player_stats", axis=1, inplace=True)

    # Merge with weather data if available
    if not weather.empty:
        # Extract date from Start Time
        hitter_data["Game_Date"] = pd.to_datetime(hitter_data["Start Time"]).dt.date.astype(str)

        # Merge on team and date
        weather["Game_Date"] = pd.to_datetime(weather["Date"]).dt.date.astype(str)

        hitter_data = pd.merge(
            hitter_data,
            weather,
            left_on=["Team", "Game_Date"],
            right_on=["Home Team", "Game_Date"],
            how="left"
        )

        # If that didn't work, try merging on the opponent (for away games)
        mask = hitter_data["Temperature"].isna()
        if mask.any():
            away_data = pd.merge(
                hitter_data[mask],
                weather,
                left_on=["Opponent", "Game_Date"],
                right_on=["Home Team", "Game_Date"],
                how="left",
                suffixes=("", "_away")
            )

            # Update the missing weather data
            for col in ["Temperature", "Humidity", "Wind Speed", "Wind Direction", "Weather Condition"]:
                if col in away_data.columns and f"{col}_away" in away_data.columns:
                    hitter_data.loc[mask, col] = away_data[f"{col}_away"]

        # Rename columns to match expected format
        hitter_data.rename(columns={
            "Temperature": "Game-Time Temp (°F)",
            "Humidity": "Game-Time Humidity (%)",
            "Wind Speed": "Game-Time Wind Speed (mph)",
            "Wind Direction": "Game-Time Wind Direction",
            "Weather Condition": "Game-Time Weather"
        }, inplace=True)

        # Add wind effect column
        hitter_data["Game-Time Effect on Hitters"] = "No wind: no effect on hitters."

        # If wind speed > 10 mph, determine effect
        wind_mask = hitter_data["Game-Time Wind Speed (mph)"] > 10
        if wind_mask.any():
            # This is simplified - in reality you'd need to check wind direction relative to field orientation
            hitter_data.loc[wind_mask, "Game-Time Effect on Hitters"] = np.random.choice([
                "Tailwind: fly balls likely to carry → helps hitters.",
                "Headwind: fly balls suppressed → hurts hitters.",
                "Crosswind: minimal effect on hitters."
            ], size=wind_mask.sum())

    # Merge with park factors if available
    if not park_factors.empty:
        # Normalize team names for matching
        if "Team" in hitter_data.columns and "Team" in park_factors.columns:
            hitter_data = pd.merge(
                hitter_data,
                park_factors,
                left_on="Team",
                right_on="Team",
                how="left"
            )

    # Ensure we have the Hit column (will be NaN for predictions)
    hitter_data["Hit"] = np.nan

    return hitter_data


def prepare_pitcher_data(props, pitcher_stats, weather, park_factors):
    """Prepare pitcher prediction data"""
    logger.info("Preparing pitcher prediction data...")

    # Filter for pitcher props
    pitcher_props = [
        "Pitcher Strikeouts", "Earned Runs Allowed", "Pitches Thrown",
        "Pitching Outs", "Pitcher Fantasy Score"
    ]
    pitcher_data = props[props["Prop Type"].isin(pitcher_props)].copy()

    if len(pitcher_data) == 0:
        logger.warning("No pitcher props found")
        return pd.DataFrame()

    # Merge with pitcher stats if available
    if not pitcher_stats.empty:
        # Normalize player names for matching
        pitcher_data["Player_Normalized"] = pitcher_data["Player"].str.lower().str.replace(' jr.', '').str.replace(
            ' sr.', '')
        pitcher_stats["Player_Normalized"] = pitcher_stats["Player"].str.lower().str.replace(' jr.', '').str.replace(
            ' sr.', '')

        # Merge on normalized player name
        pitcher_data = pd.merge(
            pitcher_data,
            pitcher_stats,
            on="Player_Normalized",
            how="left",
            suffixes=("", "_stats")
        )

        # Drop the normalized column
        pitcher_data.drop("Player_Normalized", axis=1, inplace=True)

        # Keep the original player name
        if "Player_stats" in pitcher_data.columns:
            pitcher_data.drop("Player_stats", axis=1, inplace=True)

    # Merge with weather data if available (same as hitter data)
    if not weather.empty:
        # Extract date from Start Time
        pitcher_data["Game_Date"] = pd.to_datetime(pitcher_data["Start Time"]).dt.date.astype(str)

        # Merge on team and date
        weather["Game_Date"] = pd.to_datetime(weather["Date"]).dt.date.astype(str)

        pitcher_data = pd.merge(
            pitcher_data,
            weather,
            left_on=["Team", "Game_Date"],
            right_on=["Home Team", "Game_Date"],
            how="left"
        )

        # If that didn't work, try merging on the opponent (for away games)
        mask = pitcher_data["Temperature"].isna()
        if mask.any():
            away_data = pd.merge(
                pitcher_data[mask],
                weather,
                left_on=["Opponent", "Game_Date"],
                right_on=["Home Team", "Game_Date"],
                how="left",
                suffixes=("", "_away")
            )

            # Update the missing weather data
            for col in ["Temperature", "Humidity", "Wind Speed", "Wind Direction", "Weather Condition"]:
                if col in away_data.columns and f"{col}_away" in away_data.columns:
                    pitcher_data.loc[mask, col] = away_data[f"{col}_away"]

        # Rename columns to match expected format
        pitcher_data.rename(columns={
            "Temperature": "Game-Time Temp (°F)",
            "Humidity": "Game-Time Humidity (%)",
            "Wind Speed": "Game-Time Wind Speed (mph)",
            "Wind Direction": "Game-Time Wind Direction",
            "Weather Condition": "Game-Time Weather"
        }, inplace=True)

        # Add wind effect column
        pitcher_data["Game-Time Effect on Hitters"] = "No wind: no effect on hitters."

        # If wind speed > 10 mph, determine effect
        wind_mask = pitcher_data["Game-Time Wind Speed (mph)"] > 10
        if wind_mask.any():
            # This is simplified - in reality you'd need to check wind direction relative to field orientation
            pitcher_data.loc[wind_mask, "Game-Time Effect on Hitters"] = np.random.choice([
                "Tailwind: fly balls likely to carry → helps hitters.",
                "Headwind: fly balls suppressed → hurts hitters.",
                "Crosswind: minimal effect on hitters."
            ], size=wind_mask.sum())

    # Merge with park factors if available
    if not park_factors.empty:
        # Normalize team names for matching
        if "Team" in pitcher_data.columns and "Team" in park_factors.columns:
            pitcher_data = pd.merge(
                pitcher_data,
                park_factors,
                left_on="Team",
                right_on="Team",
                how="left"
            )

    # Ensure we have the Hit column (will be NaN for predictions)
    pitcher_data["Hit"] = np.nan

    return pitcher_data


def main():
    """Main function to prepare MLB prediction data"""
    logger.info("Starting MLB prediction data preparation")

    # Fetch today's props
    props = fetch_todays_props()

    # Load player stats and other data
    hitter_stats, pitcher_stats, weather, park_factors = load_player_stats()

    # Prepare hitter prediction data
    hitter_data = prepare_hitter_data(props, hitter_stats, weather, park_factors)

    # Prepare pitcher prediction data
    pitcher_data = prepare_pitcher_data(props, pitcher_stats, weather, park_factors)

    # Save prediction data
    if not hitter_data.empty:
        hitter_data.to_csv(HITTER_PRED_PATH, index=False)
        logger.info(f"Saved hitter prediction data with shape {hitter_data.shape} to {HITTER_PRED_PATH}")
    else:
        logger.warning("No hitter prediction data to save")

    if not pitcher_data.empty:
        pitcher_data.to_csv(PITCHER_PRED_PATH, index=False)
        logger.info(f"Saved pitcher prediction data with shape {pitcher_data.shape} to {PITCHER_PRED_PATH}")
    else:
        logger.warning("No pitcher prediction data to save")

    logger.info("MLB prediction data preparation completed")

    return hitter_data, pitcher_data


if __name__ == "__main__":
    main()
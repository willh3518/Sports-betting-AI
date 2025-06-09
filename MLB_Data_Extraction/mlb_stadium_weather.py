#!/usr/bin/env python3
"""
mlb_stadium_weather.py
Extract and summarize weather data for MLB home games scheduled for today.
Uses OpenWeatherMap API to fetch weather forecasts and computes wind effects.
"""

import os
import time
import pandas as pd
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed
from mlb_utils import parse_schedule_date, manual_parse_time, compute_wind_effect, fetch_forecast_weather, TEAM_ABBREV_MAP

# Configuration
OWM_API_KEY = "6db6b866a5090601c4b967df2d80d5dc"

# File paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FOLDER = os.path.join(ROOT, "MLB_Prop_Data_CSV")
SCHEDULE_CSV = os.path.join(CSV_FOLDER, "mlb_full_schedule.csv")
ORIENTATION_CSV = os.path.join(CSV_FOLDER, "ballpark_orientation_with_coords.csv")
PRIZEPICKS_CSV = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
TEAM_MAP_CSV = os.path.join(CSV_FOLDER, "team_abbrev_map.csv")
OUTPUT_CSV = os.path.join(CSV_FOLDER, "stadium_weather_summary.csv")

WEATHER_UNITS = "imperial"
GEOCODER_PAUSE_SECONDS = 1.0   # (not used here, but kept for reference)

raw_date = input("Enter game date (YYYY-M-D), or leave blank for today: ").strip()

if raw_date:
    try:
        TODAY = datetime.strptime(raw_date, "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Use YYYY-M-D (e.g., 2025-6-5).")
        exit(1)
else:
    TODAY = datetime.now().date()

def main():
    # 1) Load schedule CSV (only Team, Date, Home/Away); parse dates
    sched_df = pd.read_csv(
        SCHEDULE_CSV,
        usecols=["Team", "Date", "Home/Away"],
        dtype=str
    )
    required = {"Team", "Date", "Home/Away"}
    if not required.issubset(set(sched_df.columns)):
        raise ValueError(f"Expected columns {required} in {SCHEDULE_CSV}.")

    sched_df["ParsedDate"] = sched_df["Date"].apply(parse_schedule_date)

    # 2) Filter for TODAY & "Home" games
    today_homes = sched_df[
        (sched_df["ParsedDate"] == TODAY) &
        (sched_df["Home/Away"].str.strip().str.lower().str.startswith("home", na=False))
    ].copy()
    if today_homes.empty:
        print(f"No home games found for {TODAY.strftime('%Y-%m-%d')}. Exiting.")
        return

    today_homes["SchedTeamNorm"] = today_homes["Team"].str.strip().str.upper()

    # 3) Load ballpark orientation CSV
    orient_df = pd.read_csv(
        ORIENTATION_CSV,
        index_col="TEAM",
        dtype={
            "STADIUM": str,
            "ORIENTATION_DEGREES": float,
            "LATITUDE": float,
            "LONGITUDE": float
        }
    )
    required_orient = {"STADIUM", "ORIENTATION_DEGREES", "LATITUDE", "LONGITUDE"}
    if not required_orient.issubset(set(orient_df.columns)):
        raise ValueError(f"Expected columns {required_orient} in {ORIENTATION_CSV}.")

    # 4) Load team_abbrev_map.csv (if present) to normalize schedule→PrizePicks codes
    team_map = {}
    if os.path.exists(TEAM_MAP_CSV):
        tm = pd.read_csv(
            TEAM_MAP_CSV,
            usecols=["schedule_abbrev", "prize_abbrev"],
            dtype=str
        )
        if {"schedule_abbrev", "prize_abbrev"}.issubset(set(tm.columns)):
            team_map = dict(
                zip(
                    tm["schedule_abbrev"].str.strip().str.upper(),
                    tm["prize_abbrev"].str.strip().str.upper()
                )
            )
        else:
            raise ValueError(f"Expected ['schedule_abbrev','prize_abbrev'] in {TEAM_MAP_CSV}.")
    else:
        print(f"Warning: Could not find {TEAM_MAP_CSV}. Using built-in team abbreviation map.")
        team_map = {k.upper(): v.upper() for k, v in TEAM_ABBREV_MAP.items()}

    # 5) Load PrizePicks CSV (to get each team's start time)
    pp_lookup = {}
    if os.path.exists(PRIZEPICKS_CSV):
        pp_df = pd.read_csv(
            PRIZEPICKS_CSV,
            usecols=["Team", "Start Time"],
            dtype=str
        )
        if {"Team", "Start Time"}.issubset(set(pp_df.columns)):
            pp_df["Team"] = pp_df["Team"].str.strip().str.upper()
            pp_lookup = dict(zip(pp_df["Team"], pp_df["Start Time"].astype(str)))
        else:
            print("Warning: PrizePicks CSV missing 'Team' or 'Start Time'. All games will use fallback time.")
    else:
        print(f"Warning: Could not find {PRIZEPICKS_CSV}. All games will use fallback time.")

    # 6) Gather all games to query
    games_to_query = []
    for _, row in today_homes.iterrows():
        sched_team = row["SchedTeamNorm"]
        prize_team = team_map.get(sched_team, sched_team)

        # Get raw_time from PrizePicks lookup (via prize_team), fallback if missing
        raw_time = pp_lookup.get(prize_team)
        if raw_time is None:
            # fallback to 7:00 PM if PrizePicks has no entry
            sched_date = row["ParsedDate"]
            dt_obj = datetime(sched_date.year, sched_date.month, sched_date.day, 19, 0)
            game_time_str = dt_obj.strftime("%Y-%m-%d %I:%M %p")
        else:
            # parse PrizePicks "Start Time"
            sched_date = row["ParsedDate"]
            dt_obj, game_time_str = manual_parse_time(raw_time, sched_date)
            if dt_obj is None:
                # fallback to 7:00 PM if parsing fails
                dt_obj = datetime(sched_date.year, sched_date.month, sched_date.day, 19, 0)
                game_time_str = dt_obj.strftime("%Y-%m-%d %I:%M %p")

        # Get ballpark orientation and coordinates
        if sched_team not in orient_df.index:
            print(f"Warning: No orientation data for {sched_team}. Skipping.")
            continue

        orient_row = orient_df.loc[sched_team]
        stadium = orient_row["STADIUM"]
        orientation_deg = orient_row["ORIENTATION_DEGREES"]
        lat = orient_row["LATITUDE"]
        lon = orient_row["LONGITUDE"]

        games_to_query.append({
            "sched_team": sched_team,
            "prize_team": prize_team,
            "stadium": stadium,
            "orientation_deg": orientation_deg,
            "lat": lat,
            "lon": lon,
            "dt_obj": dt_obj,
            "game_time_str": game_time_str
        })

    # 7) Query weather for each game
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_game = {
            executor.submit(fetch_forecast_weather, game["lat"], game["lon"], game["dt_obj"]): game
            for game in games_to_query
        }

        for future in as_completed(future_to_game):
            game = future_to_game[future]
            try:
                weather = future.result()
                if weather:
                    temp = weather.get("temp")
                    humidity = weather.get("humidity")
                    wind_speed = weather.get("wind_speed")
                    wind_deg = weather.get("wind_deg")

                    pitcher_note, hitter_note = compute_wind_effect(
                        game["orientation_deg"], wind_deg
                    )

                    results.append({
                        "Team": game["prize_team"],
                        "Stadium": game["stadium"],
                        "GameTime": game["game_time_str"],
                        "Temp": f"{temp:.1f}°F" if temp is not None else "N/A",
                        "Humidity": f"{humidity}%" if humidity is not None else "N/A",
                        "WindSpeed": f"{wind_speed} mph" if wind_speed is not None else "N/A",
                        "WindDirection": f"{wind_deg}°" if wind_deg is not None else "N/A",
                        "PitcherNote": pitcher_note,
                        "HitterNote": hitter_note
                    })
                else:
                    results.append({
                        "Team": game["prize_team"],
                        "Stadium": game["stadium"],
                        "GameTime": game["game_time_str"],
                        "Temp": "N/A",
                        "Humidity": "N/A",
                        "WindSpeed": "N/A",
                        "WindDirection": "N/A",
                        "PitcherNote": "No weather data available",
                        "HitterNote": "No weather data available"
                    })
            except Exception as e:
                print(f"Error processing {game['prize_team']}: {e}")
                results.append({
                    "Team": game["prize_team"],
                    "Stadium": game["stadium"],
                    "GameTime": game["game_time_str"],
                    "Temp": "Error",
                    "Humidity": "Error",
                    "WindSpeed": "Error",
                    "WindDirection": "Error",
                    "PitcherNote": f"Error: {str(e)}",
                    "HitterNote": f"Error: {str(e)}"
                })

    # 8) Write results to CSV
    if results:
        df_out = pd.DataFrame(results)
        os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
        df_out.to_csv(OUTPUT_CSV, index=False)
        print(f"\nWrote {len(df_out)} stadium weather entries to {OUTPUT_CSV}")

        # Print summary to console
        print("\nWeather Summary:")
        for r in results:
            print(f"{r['Team']} @ {r['Stadium']} ({r['GameTime']})")
            print(f"  Temp: {r['Temp']}, Humidity: {r['Humidity']}, Wind: {r['WindSpeed']} @ {r['WindDirection']}")
            print(f"  Pitcher: {r['PitcherNote']}")
            print(f"  Hitter: {r['HitterNote']}")
            print()
    else:
        print("No weather data was collected. Check for errors above.")

if __name__ == "__main__":
    main()
import os
import time
import requests
import pandas as pd
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed

# ───────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────────────────────────────────────

OWM_API_KEY = "6db6b866a5090601c4b967df2d80d5dc"

SCHEDULE_CSV    = "../MLB_Prop_Data_CSV/mlb_full_schedule.csv"
ORIENTATION_CSV = "../MLB_Prop_Data_CSV/ballpark_orientation_with_coords.csv"
PRIZEPICKS_CSV  = "../MLB_Prop_Data_CSV/mlb_prizepicks.csv"
TEAM_MAP_CSV    = "../MLB_Prop_Data_CSV/team_abbrev_map.csv"
OUTPUT_CSV      = "../MLB_Prop_Data_CSV/stadium_weather_summary.csv"

WEATHER_UNITS          = "imperial"
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


team_abbrev_map = {
    "ATL": "Braves", "ARI": "Diamondbacks", "BAL": "Orioles", "BOS": "Red Sox", "CHC": "Cubs",
    "CIN": "Reds", "CLE": "Guardians", "COL": "Rockies", "CHW": "White Sox", "DET": "Tigers",
    "HOU": "Astros", "KC": "Royals", "LAA": "Angels", "LAD": "Dodgers", "MIA": "Marlins",
    "MIL": "Brewers", "MIN": "Twins", "NYM": "Mets", "NYY": "Yankees", "ATH": "Athletics",
    "PHI": "Phillies", "PIT": "Pirates", "SD": "Padres", "SEA": "Mariners", "SFG": "Giants",
    "STL": "Cardinals", "TBR": "Rays", "TEX": "Rangers", "TOR": "Blue Jays", "WSN": "Nationals", "SDP": "Padres"
}

# ───────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ───────────────────────────────────────────────────────────────────────────────

def parse_schedule_date(col_str: str) -> date:
    """
    Parse a string like "Wed 5/28" → date(TODAY.year, 5, 28).
    Return None on parse failure.
    """
    try:
        md = col_str.strip().split()[-1]  # e.g. "5/28"
        m_str, d_str = md.split("/")
        return date(TODAY.year, int(m_str), int(d_str))
    except Exception:
        return None

def manual_parse_time(raw_time: str, sched_date: date):
    """
    Given something like "Thu 7:10 PM" or "7:10 PM" and a date,
    return a tuple (datetime, "YYYY-MM-DD hh:mm AM/PM").
    Return (None, None) on failure.
    """
    tokens = raw_time.split()
    if len(tokens) >= 3 and tokens[0].isalpha() and ":" in tokens[1]:
        tstr = " ".join(tokens[1:])  # e.g. "7:10 PM"
    else:
        tstr = raw_time.strip()
    try:
        time_part = tstr.upper()
        hour_min, ampm = time_part.split()
        hour_str, min_str = hour_min.split(":")
        hour = int(hour_str)
        minute = int(min_str)
        if ampm == "PM" and hour != 12:
            hour += 12
        if ampm == "AM" and hour == 12:
            hour = 0
        dt_obj = datetime(sched_date.year, sched_date.month, sched_date.day, hour, minute)
        game_time_str = dt_obj.strftime("%Y-%m-%d %I:%M %p")
        return dt_obj, game_time_str
    except Exception:
        return None, None

def compute_wind_effect(orientation_deg: float, wind_deg: float) -> (str, str):
    """
    Given field orientation (home plate→CF) and wind_deg (where wind is coming from):
      rel = (wind_deg - orientation_deg + 360) % 360

    • rel in [315..360) ∪ [0..45]   → HEADWIND
    • rel in [135..225]            → TAILWIND
    • otherwise                    → CROSSWIND

    Returns (pitcher_note, hitter_note). If wind_deg is None: both "Unknown (no wind data)".
    """
    if wind_deg is None:
        return ("Unknown (no wind data)", "Unknown (no wind data)")

    rel = (wind_deg - orientation_deg + 360) % 360
    if (rel >= 315) or (rel <= 45):
        return (
            "Headwind: balls into the air will be knocked down → helps pitchers.",
            "Headwind: balls in the air won’t carry → hinders hitters."
        )
    if 135 <= rel <= 225:
        return (
            "Tailwind: fly balls may carry farther → can hurt pitchers.",
            "Tailwind: fly balls likely to carry → helps hitters."
        )
    return (
        "Crosswind: pushes balls to foul lines. Neutral-ish for pitchers.",
        "Crosswind: pushes balls to foul lines. Neutral-ish for hitters."
    )

def fetch_forecast_weather_session(session, lat: float, lon: float, target_dt: datetime) -> dict:
    """
    Use OWM free-tier "5 day / 3 hour" endpoint via requests.Session.
    Find the forecast entry whose UNIX timestamp is closest to target_dt.
    Return { temp, humidity, wind_speed, wind_deg } or None if none found.
    """
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat":   lat,
        "lon":   lon,
        "appid": OWM_API_KEY,
        "units": WEATHER_UNITS
    }
    resp = session.get(base_url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    forecast_list = data.get("list", [])
    if not forecast_list:
        return None

    target_unix = int(time.mktime(target_dt.timetuple()))
    closest = min(forecast_list, key=lambda ent: abs(ent["dt"] - target_unix))
    return {
        "temp":       closest["main"].get("temp"),
        "humidity":   closest["main"].get("humidity"),
        "wind_speed": closest["wind"].get("speed"),
        "wind_deg":   closest["wind"].get("deg")
    }

# ───────────────────────────────────────────────────────────────────────────────
# MAIN SCRIPT
# ───────────────────────────────────────────────────────────────────────────────

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
            "STADIUM":             str,
            "ORIENTATION_DEGREES":  float,
            "LATITUDE":            float,
            "LONGITUDE":           float
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
        print(f"Warning: Could not find {TEAM_MAP_CSV}. Assuming schedule_abbrev == prize_abbrev.")

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

        # Check orientation & coords
        if sched_team not in orient_df.index:
            print(f"Warning: '{sched_team}' not in orientation CSV. Skipping.")
            continue

        stadium_name = orient_df.at[sched_team, "STADIUM"]
        orientation  = orient_df.at[sched_team, "ORIENTATION_DEGREES"]
        lat          = orient_df.at[sched_team, "LATITUDE"]
        lon          = orient_df.at[sched_team, "LONGITUDE"]
        if pd.isna(lat) or pd.isna(lon):
            print(f"Warning: '{stadium_name}' has no coordinates. Skipping '{sched_team}'.")
            continue

        games_to_query.append({
            "sched_team":    sched_team,
            "stadium_name":  stadium_name,
            "orientation":   orientation,
            "lat":           lat,
            "lon":           lon,
            "dt_obj":        dt_obj,
            "game_time_str": game_time_str
        })

    if not games_to_query:
        print("No valid games to query. Exiting.")
        return

    # 7) Fetch all weather forecasts in parallel
    session   = requests.Session()
    forecasts = {}  # key: index in games_to_query → forecast dict or None

    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_index = {
            executor.submit(
                fetch_forecast_weather_session,
                session,
                game["lat"],
                game["lon"],
                game["dt_obj"]
            ): idx
            for idx, game in enumerate(games_to_query)
        }
        for future in as_completed(future_to_index):
            idx = future_to_index[future]
            try:
                forecasts[idx] = future.result()
            except Exception:
                forecasts[idx] = None

    # 8) Build output rows
    output_rows = []
    for idx, game in enumerate(games_to_query):
        sched_team    = game["sched_team"]
        stadium_name  = game["stadium_name"]
        orientation   = game["orientation"]
        lat           = game["lat"]
        lon           = game["lon"]
        game_time_str = game["game_time_str"]
        forecast_wx   = forecasts.get(idx)

        if forecast_wx:
            pitch_note_gt, hit_note_gt = compute_wind_effect(
                orientation, forecast_wx["wind_deg"]
            )
        else:
            pitch_note_gt, hit_note_gt = ("N/A", "N/A")

        output_rows.append({
            "Team":                          sched_team,
            "Team Name": team_abbrev_map.get(sched_team, "Unknown"),
            "Stadium":                       stadium_name,
            "Orientation (°)":               orientation,
            "Latitude":                      lat,
            "Longitude":                     lon,
            "Game Time":                     game_time_str,
            "Game-Time Temp (°F)":           (forecast_wx.get("temp")      if forecast_wx else None),
            "Game-Time Humidity (%)":        (forecast_wx.get("humidity")  if forecast_wx else None),
            "Game-Time Wind Speed (mph)":    (forecast_wx.get("wind_speed")if forecast_wx else None),
            "Game-Time Wind Dir (°)":        (forecast_wx.get("wind_deg")  if forecast_wx else None),
            "Game-Time Effect on Pitchers":  pitch_note_gt,
            "Game-Time Effect on Hitters":   hit_note_gt,
        })

    # 9) Write results to CSV
    if not output_rows:
        print("No stadium/game-time weather data to write. Exiting.")
    else:
        out_df = pd.DataFrame(output_rows)
        out_df.to_csv(OUTPUT_CSV, index=False)
        print(f"Done! Wrote {len(output_rows)} rows to '{OUTPUT_CSV}'.")
        print(out_df)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
mlb_hitter_vs_pitches.py
Extract and analyze MLB hitter performance against various pitch types.
Uses Baseball Savant data to get pitch arsenal statistics.
"""

import os
import requests
import pandas as pd
import io
from mlb_utils import normalize_name

# File paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FOLDER = os.path.join(ROOT, "MLB_Prop_Data_CSV")
PRIZEPICKS_CSV = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
OUTPUT_CSV = os.path.join(CSV_FOLDER, "mlb_hitter_vs_pitchtype.csv")

# Baseball Savant URL for pitch arsenal stats
CSV_URL = (
    "https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats"
    "?type=batter"
    "&pitchType="
    "&year=2025"
    "&team="
    "&min=1"
    "&minPitches=q"
    "&sort=4"
    "&sortDir=desc"
    "&csv=true"
)

def main():
    # Validate input file
    if not os.path.isfile(PRIZEPICKS_CSV):
        raise FileNotFoundError(f"Could not find `{PRIZEPICKS_CSV}`.")

    # Load PrizePicks list
    df_prize = pd.read_csv(PRIZEPICKS_CSV)
    if "Player" not in df_prize.columns:
        raise KeyError("`mlb_prizepicks.csv` needs a column named `Player` (Firstname Lastname).")

    hitters_today = set(df_prize["Player"].dropna().str.strip().map(normalize_name).tolist())
    if not hitters_today:
        raise ValueError("No valid `Player` names found in PrizePicks CSV.")

    # Download and parse Baseball Savant CSV
    print("  Fetching CSV from Baseball Savant")
    resp = requests.get(CSV_URL)
    resp.raise_for_status()

    df_savant = pd.read_csv(io.StringIO(resp.text))
    print(" Savant returned columns:", list(df_savant.columns))

    # Verify required columns exist
    required = {
        "last_name, first_name",
        "pitch_name",
        "run_value_per_100",
        "woba",
        "est_woba",
        "hard_hit_percent"
    }
    if not required.issubset(df_savant.columns):
        missing = required - set(df_savant.columns)
        raise RuntimeError(
            f"Savant CSV is missing required column(s): {missing}. "
            f"Found columns: {list(df_savant.columns)}"
        )

    # Create normalized Player column and filter
    df_savant["Player"] = df_savant["last_name, first_name"].apply(
        lambda x: normalize_name(" ".join(reversed(x.split(","))))
    )
    df_filtered = df_savant[df_savant["Player"].isin(hitters_today)].copy()

    # Select and rename columns
    df_out = df_filtered[[
        "Player",
        "pitch_name",         # becomes "Pitch"
        "run_value_per_100",  # becomes "RV/100"
        "woba",               # becomes "wOBA"
        "est_woba",           # becomes "xwOBA"
        "hard_hit_percent"    # becomes "Hard Hit %"
    ]].rename(columns={
        "pitch_name": "Pitch",
        "run_value_per_100": "RV/100",
        "woba": "wOBA",
        "est_woba": "xwOBA",
        "hard_hit_percent": "Hard Hit %",
    })

    # Sort by Player and RV/100
    df_out["RV/100_num"] = pd.to_numeric(df_out["RV/100"], errors="coerce")
    df_out.sort_values(["Player", "RV/100_num"], ascending=[True, False], inplace=True)
    df_out.drop(columns=["RV/100_num"], inplace=True)

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df_out.to_csv(OUTPUT_CSV, index=False)
    print(f" Done. Wrote {len(df_out)} rows to `{OUTPUT_CSV}`.")
    print(df_out.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
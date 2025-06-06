#!/usr/bin/env python3
"""
mlb_pitcher_last15_last30.py

For each unique pitcher listed in today’s PrizePicks export (mlb_prizepicks.csv),
this script fetches Statcast data for the last 15 and 30 days, computes
aggregate “stuff” metrics (fastball velo, spin, Hard-Hit %, Barrel %, GB/FB/LD %),
rounds numeric outputs, and writes two CSV files:
  • mlb_last15_avg.csv
  • mlb_last30_avg.csv

- mlb_prizepicks.csv must have at least these columns:
    • Player       (exact name matching player_fg_ids.csv)
    • Position     (use “P” to flag pitchers)
    • Start Time   (not actually used here; we assume the file is already today’s game props)
- player_fg_ids.csv must have:
    • Player
    • MLB_ID       (Statcast pitcher ID)

Dependencies:
    pip install pandas pybaseball
"""

import pandas as pd
from datetime import date, datetime, timedelta
from pybaseball import statcast_pitcher

# ───────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ───────────────────────────────────────────────────────────────────────────────
PRIZEPICKS_CSV = "../MLB_Prop_Data_CSV/mlb_prizepicks.csv"
ID_MAPPING_CSV = "../MLB_Prop_Data_CSV/player_fg_ids.csv"
OUTPUT_15_CSV  = "../MLB_Prop_Data_CSV/mlb_last15_avg.csv"
OUTPUT_30_CSV  = "../MLB_Prop_Data_CSV/mlb_last30_avg.csv"

PLAYER_COL   = "Player"      # must match exactly between both CSVs
POSITION_COL = "Position"    # should be "P" for pitchers
MLB_ID_COL   = "MLB_ID"      # column in player_fg_ids.csv
# We ignore "Start Time" here, assuming mlb_prizepicks.csv only contains today’s games

# ───────────────────────────────────────────────────────────────────────────────
# 1) LOAD DATA AND MERGE
# ───────────────────────────────────────────────────────────────────────────────
pp_df  = pd.read_csv(PRIZEPICKS_CSV)
map_df = pd.read_csv(ID_MAPPING_CSV)

# Only keep pitchers
pitchers_only = pp_df[pp_df[POSITION_COL] == "P"].copy()
if pitchers_only.empty:
    print(f"No rows found in {PRIZEPICKS_CSV} where Position=='P'. Exiting.")
    exit(1)

# Merge to get MLB_ID
merged = pitchers_only.merge(
    map_df[[PLAYER_COL, MLB_ID_COL]],
    on=PLAYER_COL,
    how="left"
)

# If any MLB_ID is missing, warn the user
missing_ids = merged[merged[MLB_ID_COL].isna()][PLAYER_COL].unique()
if len(missing_ids) > 0:
    print("Warning: The following pitchers have no MLB_ID in player_fg_ids.csv:")
    for nm in missing_ids:
        print(f"  • {nm}")
    print("Those pitchers will be skipped.")
    merged = merged.dropna(subset=[MLB_ID_COL])

# ───────────────────────────────────────────────────────────────────────────────
# 2) DEDUPE TO ONE ROW PER PITCHER
# ───────────────────────────────────────────────────────────────────────────────
# We only need to compute Statcast aggregates once per unique pitcher.
# Use drop_duplicates on ‘Player’ (or on ‘MLB_ID’, if you prefer).
unique_pitchers = merged.drop_duplicates(subset=[PLAYER_COL])[ [PLAYER_COL, MLB_ID_COL] ]

# If you’d rather dedupe by ID rather than Player name, use:
# unique_pitchers = merged.drop_duplicates(subset=[MLB_ID_COL])[[PLAYER_COL, MLB_ID_COL]]

if unique_pitchers.empty:
    print("After deduplication, no unique pitchers remain. Exiting.")
    exit(1)

# ───────────────────────────────────────────────────────────────────────────────
# 3) HELPER FUNCTION TO PULL & AGGREGATE STATCAST FOR A WINDOW
# ───────────────────────────────────────────────────────────────────────────────
def compute_window_stats(pitcher_id: int, start_date: str, end_date: str) -> dict:
    """
    Pulls Statcast data for one pitcher between start_date (inclusive)
    and end_date (exclusive). Returns a dict of aggregates:
      • fastball_velo: avg release_speed (“FF”)
      • fastball_spin: avg release_spin_rate (“FF”)
      • hard_hit_pct:  pct of BIP with launch_speed >= 95
      • barrel_pct:    pct of BIP where bb_type == "barrel"
      • gb_pct:        pct of batted balls labeled ground_ball
      • fb_pct:        pct of batted balls labeled fly_ball
      • ld_pct:        pct of batted balls labeled line_drive
    If no Statcast rows in that window, all values → NaN.
    """
    df_stat = statcast_pitcher(start_date, end_date, pitcher_id)

    result = {
        "fastball_velo": float("nan"),
        "fastball_spin": float("nan"),
        "hard_hit_pct":  float("nan"),
        "barrel_pct":    float("nan"),
        "gb_pct":        float("nan"),
        "fb_pct":        float("nan"),
        "ld_pct":        float("nan"),
    }

    if df_stat.empty:
        return result

    # Fastball = Statcast pitch_type "FF"
    ff = df_stat[df_stat["pitch_type"] == "FF"]
    if not ff.empty:
        result["fastball_velo"] = ff["release_speed"].mean()
        result["fastball_spin"] = ff["release_spin_rate"].mean()

    # Batted-ball events = events ∈ {single, double, triple, home_run, field_out, grounded_into_double_play}
    bip_events = {"single", "double", "triple", "home_run", "field_out", "grounded_into_double_play"}
    bips = df_stat[df_stat["events"].isin(bip_events)]

    if not bips.empty:
        # Hard-Hit %: launch_speed ≥ 95
        result["hard_hit_pct"] = (bips["launch_speed"] >= 95).mean()
        # Barrel %: bb_type == "barrel"
        result["barrel_pct"] = (bips["bb_type"] == "barrel").mean()
        # GB/FB/LD %
        result["gb_pct"] = (bips["bb_type"] == "ground_ball").mean()
        result["fb_pct"] = (bips["bb_type"] == "fly_ball").mean()
        result["ld_pct"] = (bips["bb_type"] == "line_drive").mean()

    return result

# ───────────────────────────────────────────────────────────────────────────────
# 4) LOOP OVER UNIQUE PITCHERS & BUILD RECS FOR 15/30
# ───────────────────────────────────────────────────────────────────────────────
today_str = date.today().strftime("%Y-%m-%d")
records_15 = []
records_30 = []

for _, row in unique_pitchers.iterrows():
    name   = row[PLAYER_COL]
    mlb_id = int(row[MLB_ID_COL])

    # Compute start dates for 15 and 30 days ago
    game_date = datetime.strptime(today_str, "%Y-%m-%d")
    start_15  = (game_date - timedelta(days=15)).strftime("%Y-%m-%d")
    start_30  = (game_date - timedelta(days=30)).strftime("%Y-%m-%d")

    # Pull/aggregate the last 15 days
    stats15 = compute_window_stats(mlb_id, start_15, today_str)
    stats15["Player"] = name
    stats15["MLB_ID"] = mlb_id
    records_15.append(stats15)

    # Pull/aggregate the last 30 days
    stats30 = compute_window_stats(mlb_id, start_30, today_str)
    stats30["Player"] = name
    stats30["MLB_ID"] = mlb_id
    records_30.append(stats30)

# Convert to DataFrames
df_15 = pd.DataFrame(records_15)
df_30 = pd.DataFrame(records_30)

# Re-order so Player, MLB_ID come first
cols_15 = ["Player", "MLB_ID"] + [c for c in df_15.columns if c not in ("Player", "MLB_ID")]
cols_30 = ["Player", "MLB_ID"] + [c for c in df_30.columns if c not in ("Player", "MLB_ID")]
df_15 = df_15[cols_15]
df_30 = df_30[cols_30]

# ───────────────────────────────────────────────────────────────────────────────
# 5) ROUND ALL NUMERIC COLUMNS
# ───────────────────────────────────────────────────────────────────────────────
round_map = {
    "fastball_velo": 2,
    "fastball_spin": 0,
    "hard_hit_pct":  3,
    "barrel_pct":    3,
    "gb_pct":        3,
    "fb_pct":        3,
    "ld_pct":        3
}

df_15 = df_15.round(round_map)
df_30 = df_30.round(round_map)

# ───────────────────────────────────────────────────────────────────────────────
# 6) WRITE OUTPUT
# ───────────────────────────────────────────────────────────────────────────────
df_15.to_csv(OUTPUT_15_CSV, index=False)
df_30.to_csv(OUTPUT_30_CSV, index=False)

print(f"Done. Wrote:\n  • {OUTPUT_15_CSV}\n  • {OUTPUT_30_CSV}")

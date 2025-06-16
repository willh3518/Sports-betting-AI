#!/usr/bin/env python3
"""
mlb_hitter_advanced_stats_pybb.py

Uses pybaseball's statcast_batter to grab every PA for each hitter,
splits by pitcher hand, and computes advanced rates for vs LHP / vs RHP.
Outputs two files: mlb_advanced_vs_lhp.csv & mlb_advanced_vs_rhp.csv
"""

import os
import time
import pandas as pd
from pybaseball import statcast_batter
from mlb_utils import normalize_name

# File paths
ROOT            = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FOLDER      = os.path.join(ROOT, "MLB_Prop_Data_CSV")
PRIZEPICKS_CSV  = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
PLAYER_IDS_CSV  = os.path.join(CSV_FOLDER, "player_fg_ids.csv")
OUTPUT_LHP_CSV  = os.path.join(CSV_FOLDER, "mlb_advanced_vs_lhp.csv")
OUTPUT_RHP_CSV  = os.path.join(CSV_FOLDER, "mlb_advanced_vs_rhp.csv")

# Season date range
SEASON_START = "2025-03-01"
SEASON_END   = "2025-10-01"

def compute_advanced(df: pd.DataFrame) -> dict:
    """
    From a statcast_batter DataFrame, compute:
    BB%, K%, BB/K, AVG, OBP, SLG, OPS, ISO, BABIP.
    """
    df = df[df["events"].notnull()]
    PA  = len(df)
    BB  = (df["events"] == "walk").sum()
    K   = (df["events"] == "strikeout").sum()
    H1  = (df["events"] == "single").sum()
    H2  = (df["events"] == "double").sum()
    H3  = (df["events"] == "triple").sum()
    HR  = (df["events"] == "home_run").sum()
    H   = H1 + H2 + H3 + HR
    AB  = len(df[~df["events"].isin(["walk","hit_by_pitch","other_event"])])
    TB  = H1 + 2*H2 + 3*H3 + 4*HR
    SF  = (df["events"] == "sac_fly").sum()
    HBP = (df["events"] == "hit_by_pitch").sum()

    bb_pct  = BB/PA if PA else None
    k_pct   = K/PA if PA else None
    bbk     = BB/K if K else None
    avg     = H/AB if AB else None
    obp     = (H + BB + HBP)/(AB + BB + HBP + SF) if (AB + BB + HBP + SF) else None
    slg     = TB/AB if AB else None
    ops     = (obp + slg) if (obp is not None and slg is not None) else None
    iso     = slg - avg if (slg is not None and avg is not None) else None
    babip   = ((H - HR)/(AB - K - HR + SF)) if (AB - K - HR + SF) else None

    return {
        "PA":    PA,
        "BB%":   round(bb_pct, 3) if bb_pct is not None else None,
        "K%":    round(k_pct, 3) if k_pct is not None else None,
        "BB/K":  round(bbk,   3) if bbk is not None else None,
        "AVG":   round(avg,   3) if avg is not None else None,
        "OBP":   round(obp,   3) if obp is not None else None,
        "SLG":   round(slg,   3) if slg is not None else None,
        "OPS":   round(ops,   3) if ops is not None else None,
        "ISO":   round(iso,   3) if iso is not None else None,
        "BABIP": round(babip, 3) if babip is not None else None,
    }

def main():
    # load PrizePicks list
    df_pp = pd.read_csv(PRIZEPICKS_CSV, dtype=str)
    if "Player" not in df_pp:
        raise SystemExit("Need a 'Player' column in mlb_prizepicks.csv")
    prize_players = set(df_pp["Player"].dropna().map(normalize_name))

    # load your ID map (must have MLB_ID and FG_Position)
    df_ids = pd.read_csv(PLAYER_IDS_CSV, dtype=str)
    df_ids["Player"] = df_ids["Player"].map(normalize_name)
    df_ids = df_ids[df_ids["Player"].isin(prize_players)].copy()
    if df_ids.empty:
        raise SystemExit("No matching players in player_fg_ids.csv")

    out_rows = []
    for _, row in df_ids.iterrows():
        player = row["Player"]
        mlb_id = int(row["MLB_ID"])
        pos    = row["FG_Position"]
        print(f"Fetching statcast for {player} ({mlb_id})…", end=" ")

        try:
            statcast_df = statcast_batter(SEASON_START, SEASON_END, mlb_id)
        except Exception as e:
            print(f"ERROR: {e}")
            continue

        if statcast_df.empty:
            print("no data.")
            continue

        for side, label in [("L","vs L"), ("R","vs R")]:
            sub = statcast_df[statcast_df["p_throws"] == side]
            if sub.empty:
                continue
            metrics = compute_advanced(sub)
            metrics.update({
                "Player":   player,
                "FG_ID":    row["FG_ID"],
                "Position": pos,
                "Split":    label
            })
            out_rows.append(metrics)

        print("done.")
        time.sleep(1.0)

    # split into two DataFrames and write them out
    df_out = pd.DataFrame(out_rows)
    df_l = df_out[df_out["Split"] == "vs L"].drop(columns="Split")
    df_r = df_out[df_out["Split"] == "vs R"].drop(columns="Split")

    os.makedirs(CSV_FOLDER, exist_ok=True)
    df_l.to_csv(OUTPUT_LHP_CSV, index=False)
    df_r.to_csv(OUTPUT_RHP_CSV, index=False)
    print(f"\nWrote {len(df_l)} rows to {OUTPUT_LHP_CSV}")
    print(f"Wrote {len(df_r)} rows to {OUTPUT_RHP_CSV}")

if __name__ == "__main__":
    main()

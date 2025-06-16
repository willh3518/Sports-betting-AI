#!/usr/bin/env python3
"""
mlb_pitcher_advanced_stats_pybb.py
Uses pybaseball.statcast_pitcher to pull each MLB pitcher's plate
appearances for 2025, then computes K%, BB%, K–BB%, AVG, BABIP & WHIP.
"""

import os
import time
import pandas as pd
from pybaseball import statcast_pitcher
from mlb_utils import normalize_name

# ── CONFIG ─────────────────────────────────────────────────────────────────────
ROOT               = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FOLDER         = os.path.join(ROOT, "MLB_Prop_Data_CSV")
PRIZEPICKS_CSV     = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
PLAYER_IDS_CSV     = os.path.join(CSV_FOLDER, "player_fg_ids.csv")
OUTPUT_PITCHER_CSV = os.path.join(CSV_FOLDER, "mlb_pitcher_advanced_stats.csv")

SEASON_START       = "2025-03-01"
SEASON_END         = "2025-10-01"
REQUEST_DELAY      = 1.0  # seconds between each API call

# ── METRIC COMPUTATION ─────────────────────────────────────────────────────────
def compute_pitcher_advanced(df_pa):
    """
    Input: raw statcast_pitcher DataFrame (pitch-level).
    Returns dict of K%, BB%, K–BB%, AVG, BABIP, WHIP for that pitcher-season.
    """
    # collapse to one row per PA
    df_pa = (
        df_pa
        .dropna(subset=["events"])
        .groupby(["game_pk", "at_bat_number"], as_index=False)
        .last()
    )
    PA  = len(df_pa)
    BB  = (df_pa["events"] == "walk").sum()
    K   = (df_pa["events"] == "strikeout").sum()
    H1  = (df_pa["events"] == "single").sum()
    H2  = (df_pa["events"] == "double").sum()
    H3  = (df_pa["events"] == "triple").sum()
    HR  = (df_pa["events"] == "home_run").sum()
    H   = H1 + H2 + H3 + HR
    SF  = (df_pa["events"] == "sac_fly").sum()
    HBP = (df_pa["events"] == "hit_by_pitch").sum()
    AB  = PA - BB - HBP - SF
    # total baserunners allowed for WHIP
    WH  = BB + H
    # innings pitched ≈ outs recorded / 3
    # statcast_pitcher gives 'outs_when_up' at start, but we can infer outs per PA by:
    #   outs recorded this PA = delta in outs_when_up?  simpler: count 'events' that produce an out:
    out_events = {
        "strikeout","field_out","force_out","grounded_into_double_play",
        "sac_fly","pop_out","lineout"
    }
    outs = df_pa["events"].isin(out_events).sum()
    IP = round(outs / 3, 2) if outs else 0

    return {
        "PA":      PA,
        "K%":      round(K/PA,3) if PA else None,
        "BB%":     round(BB/PA,3) if PA else None,
        "K-BB%":   round((K - BB)/PA,3) if PA else None,
        "AVG":     round(H/AB,3) if AB>0 else None,
        "BABIP":   round((H - HR)/(AB - K - HR + SF),3)
                    if (AB - K - HR + SF)>0 else None,
        "WHIP":    round(WH/IP,3) if IP>0 else None,
        "IP":      IP
    }

# ── MAIN ────────────────────────────────────────────────────────────────────────
def main():
    # load PrizePicks hitters
    df_pp = pd.read_csv(PRIZEPICKS_CSV, dtype=str)
    if "Player" not in df_pp.columns:
        raise SystemExit("mlb_prizepicks.csv needs a 'Player' column.")
    df_pp["Player"] = df_pp["Player"].map(normalize_name)

    # load your FG ID map (which has MLB_ID and FG_Position)
    df_ids = pd.read_csv(PLAYER_IDS_CSV, dtype=str)
    df_ids["Player"] = df_ids["Player"].map(normalize_name)
    # keep only pitchers
    df_pitch = (
        df_ids
        .merge(df_pp[["Player"]].drop_duplicates(), on="Player", how="inner")
        .query("FG_Position == 'P'")
        .dropna(subset=["MLB_ID"])
    )
    if df_pitch.empty:
        raise SystemExit("No pitchers found in your PrizePicks list.")

    rows = []
    for _, row in df_pitch.iterrows():
        player  = row["Player"]
        mlb_id  = int(row["MLB_ID"])
        fg_id   = row["FG_ID"]
        print(f"▶ {player} ({mlb_id})…", end=" ", flush=True)

        try:
            df_raw = statcast_pitcher(SEASON_START, SEASON_END, mlb_id)
        except Exception as e:
            print(f"ERROR({e})")
            time.sleep(REQUEST_DELAY)
            continue

        if df_raw.empty:
            print("no data.")
            time.sleep(REQUEST_DELAY)
            continue

        metrics = compute_pitcher_advanced(df_raw)
        metrics.update({
            "Player": player,
            "FG_ID":  fg_id
        })
        rows.append(metrics)
        print("done.")
        time.sleep(REQUEST_DELAY)

    # dump CSV
    df_out = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(OUTPUT_PITCHER_CSV), exist_ok=True)
    df_out.to_csv(OUTPUT_PITCHER_CSV, index=False)
    print(f"\nWrote {len(df_out)} pitchers to {OUTPUT_PITCHER_CSV}")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
mlb_hitter_advanced_stats.py
Extract advanced hitting statistics for MLB players against LHP and RHP.
"""

import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from mlb_utils import normalize_name

# File paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FOLDER = os.path.join(ROOT, "MLB_Prop_Data_CSV")
PRIZEPICKS_CSV = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
PLAYER_IDS_CSV = os.path.join(CSV_FOLDER, "player_fg_ids.csv")
OUTPUT_LHP_CSV = os.path.join(CSV_FOLDER, "mlb_advanced_vs_lhp.csv")
OUTPUT_RHP_CSV = os.path.join(CSV_FOLDER, "mlb_advanced_vs_rhp.csv")

# Configuration
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)
REQUEST_DELAY = 1.0  # seconds between each FanGraphs request

def slugify(name: str) -> str:
    """Turn player name into URL-friendly slug."""
    import re
    s = name.lower().strip()
    s = s.replace(" ", "-")
    s = s.replace("", "").replace("'", "")
    s = s.replace(".", "")
    s = re.sub(r"[^a-z0-9\-]", "", s)
    return s

def fetch_vs_row(player_slug: str, fg_id: str, position: str, vs_side: str) -> pd.Series:
    """Fetch splits data from FanGraphs for a specific handedness."""
    base_url = f"https://www.fangraphs.com/players/{player_slug}/{fg_id}/splits?position={quote_plus(position)}"
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(base_url, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"[{fg_id}] HTTP {resp.status_code} for URL:\n  {base_url}")

    soup = BeautifulSoup(resp.text, "html.parser")
    advanced_div = soup.find("div", {"id": "advanced"})
    if not advanced_div:
        raise RuntimeError(f"[{fg_id}] No <div id='advanced'> found on FanGraphs page.")

    table = advanced_div.find("table")
    if not table:
        raise RuntimeError(f"[{fg_id}] No <table> inside <div id='advanced'>.")

    header_tr = table.find("tr")
    columns = [th.get_text(strip=True) for th in header_tr.find_all("th")]

    target_row = None
    for row in table.find_all("tr", {"class": "row-mlb-season"}):
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cells) >= 2 and cells[1] == vs_side:
            target_row = cells
            break

    if not target_row:
        raise RuntimeError(f"[{fg_id}] No 'vs {vs_side[-1]}' row found under Advanced.")

    ser = pd.Series(data=target_row, index=columns[: len(target_row)])
    return ser

def main():
    # Read PrizePicks CSV
    df_pp = pd.read_csv(PRIZEPICKS_CSV, dtype=str)
    if "Player" not in df_pp.columns:
        raise SystemExit("mlb_prizepicks.csv must have a 'Player' column (exact name).")

    prize_players = df_pp["Player"].dropna().map(normalize_name).unique().tolist()

    # Read player IDs CSV
    df_ids = pd.read_csv(PLAYER_IDS_CSV, dtype=str)
    if not {"Player", "FG_ID", "FG_Position"}.issubset(df_ids.columns):
        raise SystemExit("player_fg_ids.csv must have columns: Player, FG_ID, FG_Position.")

    df_ids["Player"] = df_ids["Player"].map(normalize_name)
    df_ids = df_ids[df_ids["Player"].isin(prize_players)].copy()
    if df_ids.empty:
        raise SystemExit("None of the PrizePicks players were found in player_fg_ids.csv.")

    rows_vs_l = []
    rows_vs_r = []

    for _, row in df_ids.iterrows():
        player_name = row["Player"]
        fg_id = row["FG_ID"]
        position = row["FG_Position"]

        if position == "P":
            print(f" Skipping {player_name} (FG_ID={fg_id}, Pos={position}) because they are a pitcher.")
            continue

        player_slug = slugify(player_name)
        print(f" Processing {player_name} (FG_ID={fg_id}, Pos={position})", end=" ")

        try:
            series_l = fetch_vs_row(player_slug, fg_id, position, "vs L")
            series_l["Player"] = player_name
            series_l["FG_ID"] = fg_id
            rows_vs_l.append(series_l)
        except Exception as e:
            print(f"[no vs L] {e}")

        try:
            series_r = fetch_vs_row(player_slug, fg_id, position, "vs R")
            series_r["Player"] = player_name
            series_r["FG_ID"] = fg_id
            rows_vs_r.append(series_r)
        except Exception as e:
            print(f"[no vs R] {e}")

        print("done.")
        time.sleep(REQUEST_DELAY)

    # Process LHP data
    if rows_vs_l:
        df_vs_l = pd.DataFrame(rows_vs_l)
        prefixes = ["BB%", "K%", "BB/K", "ISO", "BABIP", "wOBA", "wRC+"]
        keep_cols = ["Player", "FG_ID"]
        for p in prefixes:
            matched = [c for c in df_vs_l.columns if c.startswith(p)]
            keep_cols += matched
        keep_cols = [c for c in keep_cols if c in df_vs_l.columns]
        df_vs_l = df_vs_l[keep_cols]

        desired_order = ["Player", "FG_ID"] + [c for c in df_vs_l.columns if c not in ("Player", "FG_ID")]
        existing_order = [c for c in desired_order if c in df_vs_l.columns]
        df_vs_l = df_vs_l[existing_order]

        os.makedirs(os.path.dirname(OUTPUT_LHP_CSV), exist_ok=True)
        df_vs_l.to_csv(OUTPUT_LHP_CSV, index=False)
        print(f" Wrote LHP CSV: {OUTPUT_LHP_CSV} ({len(df_vs_l)} rows)")
    else:
        print("  No 'vs L' rows found for any player; skipping LHP output.")

    # Process RHP data
    if rows_vs_r:
        df_vs_r = pd.DataFrame(rows_vs_r)
        prefixes = ["BB%", "K%", "BB/K", "ISO", "BABIP", "wOBA", "wRC+"]
        keep_cols = ["Player", "FG_ID"]
        for p in prefixes:
            matched = [c for c in df_vs_r.columns if c.startswith(p)]
            keep_cols += matched
        keep_cols = [c for c in keep_cols if c in df_vs_r.columns]
        df_vs_r = df_vs_r[keep_cols]

        desired_order = ["Player", "FG_ID"] + [c for c in df_vs_r.columns if c not in ("Player", "FG_ID")]
        existing_order = [c for c in desired_order if c in df_vs_r.columns]
        df_vs_r = df_vs_r[existing_order]

        os.makedirs(os.path.dirname(OUTPUT_RHP_CSV), exist_ok=True)
        df_vs_r.to_csv(OUTPUT_RHP_CSV, index=False)
        print(f" Wrote RHP CSV: {OUTPUT_RHP_CSV} ({len(df_vs_r)} rows)")
    else:
        print("  No 'vs R' rows found for any player; skipping RHP output.")

    print(" All done.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
mlb_pitcher_advanced_stats.py
Fetches advanced pitching statistics from FanGraphs for pitchers in PrizePicks list.
"""

import os
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from mlb_utils import normalize_name

# File paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FOLDER = os.path.join(ROOT, "MLB_Prop_Data_CSV")
PRIZEPICKS_CSV = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
PLAYER_IDS_CSV = os.path.join(CSV_FOLDER, "player_fg_ids.csv")
OUTPUT_PITCHER_CSV = os.path.join(CSV_FOLDER, "mlb_pitcher_advanced_stats.csv")

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

def fetch_pitcher_advanced(player_slug: str, fg_id: str) -> pd.DataFrame:
    """Fetch advanced pitching stats from FanGraphs."""
    url = f"https://www.fangraphs.com/players/{player_slug}/{fg_id}/stats?position=P"
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"[{fg_id}] HTTP {resp.status_code} at URL: {url}")

    soup = BeautifulSoup(resp.text, "html.parser")
    adv_div = soup.find("div", id="advanced")
    if adv_div is None:
        raise RuntimeError(f"[{fg_id}] No <div id='advanced'> found on page.")

    table_tag = adv_div.find("table")
    if table_tag is None:
        raise RuntimeError(f"[{fg_id}] Found <div id='advanced'> but no <table> inside it.")

    df_list = pd.read_html(str(table_tag))
    if not df_list:
        raise RuntimeError(f"[{fg_id}] pd.read_html failed to extract any table from <div id='advanced'>.")
    df = df_list[0]

    df.columns = [str(c).strip() for c in df.columns]
    return df

def main():
    # Read PrizePicks CSV
    if not os.path.isfile(PRIZEPICKS_CSV):
        raise SystemExit(f"Cannot find PrizePicks CSV at: {PRIZEPICKS_CSV}")

    df_prizepicks = pd.read_csv(PRIZEPICKS_CSV, dtype=str)
    df_prizepicks["Player"] = df_prizepicks["Player"].map(normalize_name)
    if "Player" not in df_prizepicks.columns:
        raise SystemExit("`mlb_prizepicks.csv` must have at least a `Player` column.")

    # Read player IDs CSV
    if not os.path.isfile(PLAYER_IDS_CSV):
        raise SystemExit(f"Cannot find player IDs CSV at: {PLAYER_IDS_CSV}")

    df_ids = pd.read_csv(PLAYER_IDS_CSV, dtype=str)
    df_ids["Player"] = df_ids["Player"].map(normalize_name)
    required_cols = {"Player", "FG_ID", "FG_Position"}
    if not required_cols.issubset(df_ids.columns):
        raise SystemExit("`player_fg_ids.csv` must have columns: Player, FG_ID, FG_Position.")

    # Merge PrizePicks with FG IDs
    df_merged = pd.merge(
        df_prizepicks[["Player"]].drop_duplicates(),
        df_ids[["Player", "FG_ID", "FG_Position"]],
        on="Player",
        how="left"
    )

    # Check for missing FG IDs
    missing_fg = df_merged[df_merged["FG_ID"].isna()]["Player"].unique()
    if len(missing_fg) > 0:
        print("  The following PrizePicks players were not found in player_fg_ids.csv and will be skipped:")
        for p in missing_fg:
            print(f"     {p}")
        print()

    # Filter to pitchers only
    df_pitchers = df_merged[
        (df_merged["FG_Position"] == "P") & (df_merged["FG_ID"].notna())
    ].copy()

    if df_pitchers.empty:
        raise SystemExit("No pitchers (FG_Position == 'P') found after merging. Exiting.")

    all_pitcher_dfs = []

    for _, row in df_pitchers.iterrows():
        player_name = row["Player"]
        fg_id = row["FG_ID"]
        player_slug = slugify(player_name)

        print(f" Fetching advanced stats for {player_name} (FG_ID={fg_id})", end=" ")
        try:
            df_adv = fetch_pitcher_advanced(player_slug, fg_id)

            # Filter to 2025 MLB
            df_adv["Season"] = df_adv["Season"].astype(str).str.strip()
            df_adv["Level"] = df_adv["Level"].astype(str).str.strip()
            df_2025_mlb = df_adv[
                (df_adv["Season"] == "2025") &
                (df_adv["Level"] == "MLB")
            ].copy()

            if df_2025_mlb.empty:
                raise RuntimeError(f"[{fg_id}] No 2025MLB row found in Advanced table.")

            # Keep only relevant columns
            keep_prefixes = [
                "K%", "BB%", "K-BB%", "AVG", "WHIP", "BABIP",
                "LOB%", "ERA-", "FIP-", "FIP"
            ]

            final_cols = ["Player", "FG_ID"]
            for col in df_2025_mlb.columns:
                lower = str(col).lower()
                if "divider" in lower:
                    continue
                for prefix in keep_prefixes:
                    if str(col).startswith(prefix):
                        final_cols.append(col)
                        break

            df_2025_mlb.insert(0, "FG_ID", fg_id)
            df_2025_mlb.insert(0, "Player", player_name)

            final_cols = [c for c in final_cols if c in df_2025_mlb.columns]
            df_trimmed = df_2025_mlb[final_cols].copy()
            all_pitcher_dfs.append(df_trimmed)

        except Exception as e:
            print(f"[error] {e}")
        else:
            print("done.")

        time.sleep(REQUEST_DELAY)

    # Combine results
    if not all_pitcher_dfs:
        print("  No 2025MLB pitcher rows were fetched; exiting without writing CSV.")
        return

    df_combined = pd.concat(all_pitcher_dfs, ignore_index=True)
    df_combined = df_combined.loc[:, df_combined.columns]

    # Write output
    os.makedirs(os.path.dirname(OUTPUT_PITCHER_CSV), exist_ok=True)
    df_combined.to_csv(OUTPUT_PITCHER_CSV, index=False)
    print(f" Wrote pitcher advanced stats CSV: {OUTPUT_PITCHER_CSV} ({len(df_combined)} rows)")
    print(" All done.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
mlb_pitcher_advanced_stats.py

1) Reads the PrizePicks list of players from `mlb_prizepicks.csv`.
2) Cross‐references against `player_fg_ids.csv` to get each player’s FG_ID and position.
3) Keeps only those with FG_Position == "P" (pitchers).
4) Fetches the “Advanced Pitcher” table from FanGraphs for each pitcher.
5) Filters to only the Season==2025 and Level=="MLB" row.
6) From that row, keeps only K% and everything to its right (drops all earlier columns and any “divider” columns).
7) Outputs a combined CSV to `mlb_pitcher_advanced_stats.csv` that begins with Player, FG_ID, then the trimmed stat columns.
"""

import os, unidecode
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

# ─── CONFIG ───────────────────────────────────────────────────────────────────────
PRIZEPICKS_CSV       = "../MLB_Prop_Data_CSV/mlb_prizepicks.csv"
PLAYER_IDS_CSV       = "../MLB_Prop_Data_CSV/player_fg_ids.csv"
OUTPUT_PITCHER_CSV   = "../MLB_Prop_Data_CSV/mlb_pitcher_advanced_stats.csv"

USER_AGENT           = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/136.0.0.0 Safari/537.36"
)
REQUEST_DELAY        = 1.0   # seconds between each FanGraphs request

# ─── UTILITIES ─────────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """
    Turn "Tarik Skubal" → "tarik-skubal", "Luis Urías" → "luis-urias", etc.
    Removes punctuation, lowercases, replaces spaces with hyphens.
    """
    s = name.lower().strip()
    s = s.replace(" ", "-")
    s = s.replace("’", "").replace("'", "")
    s = s.replace(".", "")
    s = re.sub(r"[^a-z0-9\-]", "", s)
    return s

def normalize_name(name: str) -> str:
    name = str(name)
    name = unidecode.unidecode(name)
    name = name.replace(".", "").replace("Jr", "").replace("II", "").replace("III", "")
    name = " ".join(name.split())
    name = name.title()

    corrections = {
        "Dj Lemahieu": "DJ LeMahieu",
        "Cj Abrams": "CJ Abrams",
        "Tj Friedl": "TJ Friedl",
        "Jp Crawford": "JP Crawford",
        "Andrew Mccutchen": "Andrew McCutchen",
    }

    return corrections.get(name, name)

def fetch_pitcher_advanced(player_slug: str, fg_id: str) -> pd.DataFrame:
    """
    1) Builds the URL:
         https://www.fangraphs.com/players/{player_slug}/{fg_id}/stats?position=P
    2) GETs the HTML.
    3) Uses BeautifulSoup to find <div id="advanced">…</div>, then grabs the <table> inside it.
    4) Feeds that <table> into pandas.read_html, returns the resulting DataFrame.
    """
    url = f"https://www.fangraphs.com/players/{player_slug}/{fg_id}/stats?position=P"
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"[{fg_id}] HTTP {resp.status_code} at URL: {url}")

    soup = BeautifulSoup(resp.text, "html.parser")

    # 1) Locate the <div id="advanced">
    adv_div = soup.find("div", id="advanced")
    if adv_div is None:
        raise RuntimeError(f"[{fg_id}] No <div id='advanced'> found on page.")

    # 2) Within that DIV, find the first <table>
    table_tag = adv_div.find("table")
    if table_tag is None:
        raise RuntimeError(f"[{fg_id}] Found <div id='advanced'> but no <table> inside it.")

    # 3) Convert the <table> tag to a string and read via pandas
    df_list = pd.read_html(str(table_tag))
    if not df_list:
        raise RuntimeError(f"[{fg_id}] pd.read_html failed to extract any table from <div id='advanced'>.")
    df = df_list[0]

    # 4) Clean column names (strip whitespace)
    df.columns = [str(c).strip() for c in df.columns]
    return df

# ─── MAIN ─────────────────────────────────────────────────────────────────────────

def main():
    # 1) Read PrizePicks CSV (must contain “Player” column)
    if not os.path.isfile(PRIZEPICKS_CSV):
        raise SystemExit(f"Cannot find PrizePicks CSV at: {PRIZEPICKS_CSV}")

    df_prizepicks = pd.read_csv(PRIZEPICKS_CSV, dtype=str)
    df_prizepicks["Player"] = df_prizepicks["Player"].map(normalize_name)
    if "Player" not in df_prizepicks.columns:
        raise SystemExit("`mlb_prizepicks.csv` must have at least a `Player` column.")

    # 2) Read player_fg_ids.csv (must contain Player, FG_ID, FG_Position)
    if not os.path.isfile(PLAYER_IDS_CSV):
        raise SystemExit(f"Cannot find player IDs CSV at: {PLAYER_IDS_CSV}")

    df_ids = pd.read_csv(PLAYER_IDS_CSV, dtype=str)
    df_ids["Player"] = df_ids["Player"].map(normalize_name)
    required_cols = {"Player", "FG_ID", "FG_Position"}
    if not required_cols.issubset(df_ids.columns):
        raise SystemExit("`player_fg_ids.csv` must have columns: Player, FG_ID, FG_Position.")

    # 3) Merge PrizePicks list with FG IDs on “Player”
    df_merged = pd.merge(
        df_prizepicks[["Player"]].drop_duplicates(),
        df_ids[["Player", "FG_ID", "FG_Position"]],
        on="Player",
        how="left"
    )

    # 4) Warn if any PrizePicks names failed to join
    missing_fg = df_merged[df_merged["FG_ID"].isna()]["Player"].unique()
    if len(missing_fg) > 0:
        print("⚠️  The following PrizePicks players were not found in player_fg_ids.csv and will be skipped:")
        for p in missing_fg:
            print(f"    • {p}")
        print()

    # 5) Filter to only those with FG_Position == "P"
    df_pitchers = df_merged[
        (df_merged["FG_Position"] == "P") & (df_merged["FG_ID"].notna())
    ].copy()

    if df_pitchers.empty:
        raise SystemExit("No pitchers (FG_Position == 'P') found after merging. Exiting.")

    all_pitcher_dfs = []

    for _, row in df_pitchers.iterrows():
        player_name = row["Player"]
        fg_id       = row["FG_ID"]
        player_slug = slugify(player_name)

        print(f"→ Fetching advanced stats for {player_name} (FG_ID={fg_id})…", end=" ")
        try:
            df_adv = fetch_pitcher_advanced(player_slug, fg_id)

            # ─── FILTER TO 2025 / MLB ─────────────────────────────────────────────
            df_adv["Season"] = df_adv["Season"].astype(str).str.strip()
            df_adv["Level"]  = df_adv["Level"].astype(str).str.strip()

            # Keep only rows where Season == "2025" and Level == "MLB"
            df_2025_mlb = df_adv[
                (df_adv["Season"] == "2025") &
                (df_adv["Level"] == "MLB")
            ].copy()

            if df_2025_mlb.empty:
                raise RuntimeError(f"[{fg_id}] No 2025‐MLB row found in Advanced table.")

            # ─── KEEP ONLY COLUMNS FROM K% FORWARD ────────────────────────────────
            # We’ll drop everything up through HR/9 and also drop any column whose name contains “divider”.

            keep_prefixes = [
                "K%",      # Strikeout Percentage
                "BB%",     # Walk Percentage
                "K-BB%",   # Difference between strikeout % and walk %
                "AVG",     # Batting Average Against
                "WHIP",    # Walks + Hits divided by Innings Pitched
                "BABIP",   # Batting Average on Balls in Play
                "LOB%",    # Left on Base Percentage
                "ERA-",    # ERA- (adjusted)
                "FIP-",    # FIP- (adjusted)
                "FIP"      # FIP (on ERA scale)
            ]

            # Build our final column order, starting with Player & FG_ID
            final_cols = ["Player", "FG_ID"]
            for col in df_2025_mlb.columns:
                lower = str(col).lower()
                if "divider" in lower:
                    continue
                for prefix in keep_prefixes:
                    if str(col).startswith(prefix):
                        final_cols.append(col)
                        break

            # Ensure Player/FG_ID exist in df_2025_mlb (they do not yet), so insert them
            df_2025_mlb.insert(0, "FG_ID", fg_id)
            df_2025_mlb.insert(0, "Player", player_name)

            # Make sure we only keep columns that actually exist in df_2025_mlb
            final_cols = [c for c in final_cols if c in df_2025_mlb.columns]

            df_trimmed = df_2025_mlb[final_cols].copy()
            all_pitcher_dfs.append(df_trimmed)

        except Exception as e:
            print(f"[error] {e}")
        else:
            print("done.")

        time.sleep(REQUEST_DELAY)

    # 6) Combine into one DataFrame (if any pitchers succeeded)
    if not all_pitcher_dfs:
        print("⚠️  No 2025‐MLB pitcher rows were fetched; exiting without writing CSV.")
        return

    df_combined = pd.concat(all_pitcher_dfs, ignore_index=True)

    # 7) The columns are already in the desired order (Player, FG_ID, then K% → FIP).
    #    Just double‐check that ordering:
    df_combined = df_combined.loc[:, df_combined.columns]

    # 8) Write out CSV
    os.makedirs(os.path.dirname(OUTPUT_PITCHER_CSV), exist_ok=True)
    df_combined.to_csv(OUTPUT_PITCHER_CSV, index=False)
    print(f"→ Wrote pitcher advanced stats CSV: {OUTPUT_PITCHER_CSV} ({len(df_combined)} rows)")
    print("✅ All done.")

if __name__ == "__main__":
    main()

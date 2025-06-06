# mlb_hitter_advanced_splits.py

import os
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# ─── CONFIG ───────────────────────────────────────────────────────────────────────
PRIZEPICKS_CSV = "../MLB_Prop_Data_CSV/mlb_prizepicks.csv"
PLAYER_IDS_CSV = "../MLB_Prop_Data_CSV/player_fg_ids.csv"
OUTPUT_LHP_CSV = "../MLB_Prop_Data_CSV/mlb_advanced_vs_lhp.csv"
OUTPUT_RHP_CSV = "../MLB_Prop_Data_CSV/mlb_advanced_vs_rhp.csv"

USER_AGENT    = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 " \
                "(KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
REQUEST_DELAY = 1.0   # seconds between each FanGraphs request

# ─── UTILITIES ─────────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """
    Turn a name like "Brent Rooker" → "brent-rooker", "Luis Urías" → "luis-urias", etc.
    Strips punctuation, lowercases, replaces spaces with hyphens, removes any non-alphanumeric (a–z, 0–9, -).
    """
    s = name.lower().strip()
    s = s.replace(" ", "-")
    s = s.replace("’", "").replace("'", "")     # drop apostrophes
    s = s.replace(".", "")                      # drop periods
    # remove any character that isn’t a–z, 0–9, or hyphen
    s = re.sub(r"[^a-z0-9\-]", "", s)
    return s

def fetch_vs_row(player_slug: str, fg_id: str, position: str, vs_side: str) -> pd.Series:
    """
    1) Builds the URL:
         https://www.fangraphs.com/players/{player_slug}/{fg_id}/splits?position={position}
       where position might be "DH/OF", "P", "3B", etc.
    2) GETs the HTML.
    3) Locates <div id="advanced">, then grabs the FIRST <table> inside it (the "Handedness" sub-table).
    4) Looks for exactly one <tr class="row-mlb-season"> whose second column text == vs_side
       (vs_side must be "vs L" or "vs R").
    5) Returns that row as a pandas.Series (with the same columns as the table header).
       If anything fails (404, no advanced table, no matching row), raises an Exception.
    """
    # Build the splits URL, quoting the position
    base_url = f"https://www.fangraphs.com/players/{player_slug}/{fg_id}/splits?position={quote_plus(position)}"
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(base_url, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"[{fg_id}] HTTP {resp.status_code} for URL:\n  {base_url}")

    soup = BeautifulSoup(resp.text, "html.parser")
    advanced_div = soup.find("div", {"id": "advanced"})
    if not advanced_div:
        raise RuntimeError(f"[{fg_id}] No <div id='advanced'> found on FanGraphs page.")

    # The first <table> under <div id="advanced"> is the "Handedness" table (vs L, vs R, vs L as R, vs R as R, etc.)
    table = advanced_div.find("table")
    if not table:
        raise RuntimeError(f"[{fg_id}] No <table> inside <div id='advanced'>.")

    # Extract header row (first <tr> containing <th> elements)
    header_tr = table.find("tr")
    columns = [th.get_text(strip=True) for th in header_tr.find_all("th")]

    # Now find exactly the <tr class="row-mlb-season"> whose second cell matches vs_side.
    target_row = None
    for row in table.find_all("tr", {"class": "row-mlb-season"}):
        cells = [td.get_text(strip=True) for td in row.find_all("td")]
        if len(cells) >= 2 and cells[1] == vs_side:
            target_row = cells
            break

    if not target_row:
        # If the player has zero AB vs L (or vs R) this row might not exist. We treat that as missing.
        raise RuntimeError(f"[{fg_id}] No 'vs {vs_side[-1]}' row found under Advanced.")

    # Build a pandas.Series out of it (using same column names)
    # Note: sometimes the number of <td> equals len(columns). If columns is longer, we only keep exactly len(cells).
    ser = pd.Series(data=target_row, index=columns[: len(target_row)])
    return ser

# ─── MAIN ─────────────────────────────────────────────────────────────────────────

def main():
    # 1) Read mlb_prizepicks.csv to get exactly which Player names to process
    df_pp = pd.read_csv(PRIZEPICKS_CSV, dtype=str)
    if "Player" not in df_pp.columns:
        raise SystemExit("mlb_prizepicks.csv must have a 'Player' column (exact name).")

    prize_players = df_pp["Player"].dropna().unique().tolist()

    # 2) Read player_fg_ids.csv (to pull FG_ID and FG_Position)
    df_ids = pd.read_csv(PLAYER_IDS_CSV, dtype=str)
    if not {"Player", "FG_ID", "FG_Position"}.issubset(df_ids.columns):
        raise SystemExit("player_fg_ids.csv must have columns: Player, FG_ID, FG_Position.")

    # Keep just the rows in df_ids whose Player is in prize_players (case-sensitive match)
    df_ids = df_ids[df_ids["Player"].isin(prize_players)].copy()
    if df_ids.empty:
        raise SystemExit("None of the PrizePicks players were found in player_fg_ids.csv.")

    # We'll accumulate two lists of pandas.Series: one for vs L, one for vs R
    rows_vs_l = []
    rows_vs_r = []

    for idx, row in df_ids.iterrows():
        player_name = row["Player"]
        fg_id       = row["FG_ID"]
        position    = row["FG_Position"]

        # Skip any pitcher entries
        if position == "P":
            print(f"→ Skipping {player_name} (FG_ID={fg_id}, Pos={position}) because they are a pitcher.")
            continue

        player_slug = slugify(player_name)
        print(f"→ Processing {player_name} (FG_ID={fg_id}, Pos={position})…", end=" ")

        try:
            # Fetch exactly the "vs L" row
            series_l = fetch_vs_row(player_slug, fg_id, position, "vs L")
            series_l["Player"] = player_name
            series_l["FG_ID"]  = fg_id
            rows_vs_l.append(series_l)

        except Exception as e:
            print(f"[no vs L] ", e)

        try:
            # Fetch exactly the "vs R" row
            series_r = fetch_vs_row(player_slug, fg_id, position, "vs R")
            series_r["Player"] = player_name
            series_r["FG_ID"]  = fg_id
            rows_vs_r.append(series_r)

        except Exception as e:
            print(f"[no vs R] ", e)

        print("done.")
        time.sleep(REQUEST_DELAY)

    # 3) Combine into two DataFrames (if we got any rows at all)
    if rows_vs_l:
        df_vs_l = pd.DataFrame(rows_vs_l)

        # ─── KEEP ONLY THE COLUMNS YOU WANT ─────────────────────────────────────
        prefixes = ["BB%", "K%", "BB/K", "ISO", "BABIP", "wOBA", "wRC+"]
        keep_cols = ["Player", "FG_ID"]
        for p in prefixes:
            matched = [c for c in df_vs_l.columns if c.startswith(p)]
            keep_cols += matched
        # only keep columns that actually exist
        keep_cols = [c for c in keep_cols if c in df_vs_l.columns]
        df_vs_l = df_vs_l[keep_cols]
        # ────────────────────────────────────────────────────────────────────

        # Reorder columns so "Player" and "FG_ID" come first, then everything else
        desired_order = ["Player", "FG_ID"] + [c for c in df_vs_l.columns if c not in ("Player", "FG_ID")]
        existing_order = [c for c in desired_order if c in df_vs_l.columns]
        df_vs_l = df_vs_l[existing_order]

        df_vs_l.to_csv(OUTPUT_LHP_CSV, index=False)
        print(f"→ Wrote LHP CSV: {OUTPUT_LHP_CSV} ({len(df_vs_l)} rows)")
    else:
        print("⚠️  No 'vs L' rows found for any player; skipping LHP output.")

    if rows_vs_r:
        df_vs_r = pd.DataFrame(rows_vs_r)

        # ─── KEEP ONLY THE COLUMNS YOU WANT ─────────────────────────────────────
        prefixes = ["BB%", "K%", "BB/K", "ISO", "BABIP", "wOBA", "wRC+"]
        keep_cols = ["Player", "FG_ID"]
        for p in prefixes:
            matched = [c for c in df_vs_r.columns if c.startswith(p)]
            keep_cols += matched
        keep_cols = [c for c in keep_cols if c in df_vs_r.columns]
        df_vs_r = df_vs_r[keep_cols]
        # ────────────────────────────────────────────────────────────────────

        desired_order = ["Player", "FG_ID"] + [c for c in df_vs_r.columns if c not in ("Player", "FG_ID")]
        existing_order = [c for c in desired_order if c in df_vs_r.columns]
        df_vs_r = df_vs_r[existing_order]

        df_vs_r.to_csv(OUTPUT_RHP_CSV, index=False)
        print(f"→ Wrote RHP CSV: {OUTPUT_RHP_CSV} ({len(df_vs_r)} rows)")
    else:
        print("⚠️  No 'vs R' rows found for any player; skipping RHP output.")

    print("✅ All done.")

if __name__ == "__main__":
    main()

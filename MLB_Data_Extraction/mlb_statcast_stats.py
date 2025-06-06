# mlb_hitter_statcast_stats.py

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
OUTPUT_CSV     = "../MLB_Prop_Data_CSV/mlb_hitter_statcast_stats.csv"

USER_AGENT    = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
)
REQUEST_DELAY = 1.0   # seconds between each FanGraphs request

# ─── UTILITIES ─────────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """
    Convert a player name like "Shohei Ohtani" → "shohei-ohtani",
    drop punctuation, lowercase, replace spaces with hyphens.
    """
    s = name.lower().strip()
    s = s.replace(" ", "-")
    s = s.replace("’", "").replace("'", "")
    s = s.replace(".", "")
    s = re.sub(r"[^a-z0-9\-]", "", s)
    return s

def fetch_statcast_table(player_slug: str, fg_id: str, position: str) -> pd.DataFrame:
    """
    1) Build URL:
       https://www.fangraphs.com/players/{player_slug}/{fg_id}/stats?position={position}#statcast
    2) GET HTML, parse <div id="statcast"> → first <table>.
    3) Skip any <th> whose text is "divider" or blank, build valid_columns + valid_indices.
    4) For each <tr class="row-mlb-season">, extract only valid_indices → Series(valid_columns).
    5) Return DataFrame of all seasons for that player.
    """
    base_url = (
        f"https://www.fangraphs.com/players/{player_slug}/{fg_id}/stats"
        f"?position={quote_plus(position)}#statcast"
    )
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(base_url, headers=headers, timeout=15)
    if resp.status_code != 200:
        raise RuntimeError(f"[{fg_id}] HTTP {resp.status_code} for URL:\n  {base_url}")

    soup = BeautifulSoup(resp.text, "html.parser")
    statcast_div = soup.find("div", {"id": "statcast"})
    if not statcast_div:
        raise RuntimeError(f"[{fg_id}] No <div id='statcast'> found.")

    table = statcast_div.find("table")
    if not table:
        raise RuntimeError(f"[{fg_id}] No <table> inside <div id='statcast'>.")

    # Build header-to-index mapping, skipping any <th> with text "divider" or "".
    header_tr = table.find("thead").find("tr")
    th_list = header_tr.find_all("th")
    valid_columns = []
    valid_indices = []
    for idx, th in enumerate(th_list):
        txt = th.get_text(strip=True)
        if txt.lower() == "divider" or txt == "":
            continue
        valid_columns.append(txt)
        valid_indices.append(idx)

    # Parse each season row
    rows = []
    for tr in table.find("tbody").find_all("tr", {"class": "row-mlb-season"}):
        td_list = tr.find_all("td")
        if len(td_list) < len(th_list):
            continue
        row_values = [td_list[i].get_text(strip=True) for i in valid_indices]
        rows.append(pd.Series(data=row_values, index=valid_columns))

    if not rows:
        raise RuntimeError(f"[{fg_id}] No statcast rows found.")

    return pd.DataFrame(rows)

# ─── MAIN ─────────────────────────────────────────────────────────────────────────

def main():
    # 1) Read mlb_prizepicks.csv → list of Player names
    df_pp = pd.read_csv(PRIZEPICKS_CSV, dtype=str)
    if "Player" not in df_pp.columns:
        raise SystemExit("mlb_prizepicks.csv must have a 'Player' column.")
    prize_players = df_pp["Player"].dropna().unique().tolist()

    # 2) Read player_fg_ids.csv → filter to those Players
    df_ids = pd.read_csv(PLAYER_IDS_CSV, dtype=str)
    required = {"Player", "FG_ID", "FG_Position"}
    if not required.issubset(df_ids.columns):
        raise SystemExit("player_fg_ids.csv must have columns: Player, FG_ID, FG_Position.")
    df_ids = df_ids[df_ids["Player"].isin(prize_players)].copy()
    if df_ids.empty:
        raise SystemExit("None of the PrizePicks players found in player_fg_ids.csv.")

    all_rows = []
    for _, row in df_ids.iterrows():
        player_name = row["Player"]
        fg_id       = row["FG_ID"]
        position    = row["FG_Position"]

        # Skip pitchers
        if position == "P":
            print(f"→ Skipping {player_name} (FG_ID={fg_id})—pitcher.")
            continue

        player_slug = slugify(player_name)
        print(f"→ Fetching Statcast for {player_name} (FG_ID={fg_id})…", end=" ")
        try:
            df_statcast = fetch_statcast_table(player_slug, fg_id, position)

            # ─── KEEP ONLY 2025 ROW ─────────────────────────────────────────
            df_2025 = df_statcast[df_statcast["Season"] == "2025"].copy()
            if df_2025.empty:
                print("[no 2025 row] skipped.")
                continue
            # ────────────────────────────────────────────────────────────────

            # Insert Player + FG_ID, then append the single-2025-row to all_rows
            df_2025.insert(0, "FG_ID", fg_id)
            df_2025.insert(0, "Player", player_name)
            all_rows.append(df_2025)

        except Exception as e:
            print(f"[ERROR] {e}")
        else:
            print("done.")

        time.sleep(REQUEST_DELAY)

    if not all_rows:
        print("⚠️  No 2025 data collected; exiting.")
        return

    # 3) Concatenate all single-rows into one DataFrame
    df_all = pd.concat(all_rows, ignore_index=True)

    # ─── KEEP ONLY COLUMNS WE WANT ───────────────────────────────────────────────
    # We only need: Player, FG_ID, EV, Barrel%, HardHit%, xBA, xwOBA
    prefixes = ["EV", "Barrel%", "HardHit%", "xBA", "xwOBA"]
    keep = ["Player", "FG_ID"]  # always keep
    for p in prefixes:
        matched = [c for c in df_all.columns if c.startswith(p)]
        keep += matched
    keep = [c for c in keep if c in df_all.columns]
    df_final = df_all[keep]
    # ───────────────────────────────────────────────────────────────────────────

    # 4) Write to CSV
    df_final.to_csv(OUTPUT_CSV, index=False)
    print(f"→ Wrote Statcast CSV: {OUTPUT_CSV} ({len(df_final)} rows)")

if __name__ == "__main__":
    main()

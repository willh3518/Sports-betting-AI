import asyncio
import os
import aiohttp
import logging
import pandas as pd
import random
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from Data_Extraction.utils import clean_player_name
from MLB_Data_Extraction.mlb_utils import normalize_name

# ——— Logging ———
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ——— File paths ———
INPUT_CSV    = "MLB_Prop_Data_CSV/mlb_prizepicks.csv"
HITTER_OUT   = "MLB_Prop_Data_CSV/hitter_boxscore_results.csv"
PITCHER_OUT  = "MLB_Prop_Data_CSV/pitcher_boxscore_results.csv"

# ——— StatMuse MLB endpoint & UAs ———
STATMUSE_URL = "https://www.statmuse.com/mlb/ask/{player}-box-score-last-game"
USER_AGENTS  = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)…",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)…",
    "Mozilla/5.0 (X11; Linux x86_64)…",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)…"
]

# ——— which headers to scrape ———
HITTER_STATS  = {"AB","R","H","2B","3B","HR","RBI","BB","HBP","SO","SB","CS","PA","TB","XBH","SH","SF","IBB","GIDP"}
PITCHER_STATS = {"DEC","GS","ERA","SO","CG","SHO","SV","IP","H","ER","R","HR","BB","HBP","GF","IBB","TBF","WP"}

# ─── 0) Fetch yesterday’s pitcher boxscore stats via MLB API ───
def fetch_yesterday_pitchers():
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    sched_url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={yesterday}"
    sched = requests.get(sched_url).json()
    stats = {}
    for date in sched.get("dates", []):
        for game in date.get("games", []):
            box = requests.get(f"https://statsapi.mlb.com/api/v1/game/{game['gamePk']}/boxscore").json()
            for side in ("home","away"):
                for pdata in box["teams"][side]["players"].values():
                    ps = pdata.get("stats", {}).get("pitching")
                    if ps:
                        raw = pdata["person"]["fullName"]
                        name = normalize_name(raw)
                        stats[name] = {
                            "Pitches Thrown": ps.get("numberOfPitches", 0),
                            "Pitching Outs":  ps.get("outs", 0)
                        }
    return stats

PITCHER_API_STATS = fetch_yesterday_pitchers()

# ─── safe cast ───
def safe_float(x):
    try:
        return float(x)
    except:
        return 0.0

# Then the update_prediction_files function
async def update_prediction_files(date_str):
    """Update prediction files with actual results and stats"""
    # Define prediction file paths with the provided date format
    prediction_files = [
        f"MLB_Results/{date_str}_mlb_predictions.csv",
        f"MLB_Results/{date_str}_mlb_top_picks.csv",
        f"MLB_Results/{date_str}_mlb_xgb_predictions.csv",
        f"MLB_Results/{date_str}_mlb_xgb_top_picks.csv"
    ]

    # Load hitter and pitcher results
    try:
        hitter_results = pd.read_csv(HITTER_OUT)
        pitcher_results = pd.read_csv(PITCHER_OUT)

        # Combine results for easier lookup
        all_results = pd.concat([hitter_results, pitcher_results])

        # Create lookup dictionaries for actual stats and results
        stat_lookup = {}
        result_lookup = {}

        for _, row in all_results.iterrows():
            player = row['Player']
            prop_type = row['Prop Type']
            prop_value = row['Prop Value']
            key = f"{player}|{prop_type}|{prop_value}"

            stat_lookup[key] = row['Actual Stat']
            # Convert hit to Over/Under
            if row['Hit'] == 1:
                result_lookup[key] = 'Over'
            elif row['Hit'] == 0:
                result_lookup[key] = 'Under'
            else:
                result_lookup[key] = None

        # Update each prediction file
        for pred_file in prediction_files:
            if os.path.exists(pred_file):
                logging.info(f"Updating prediction file: {pred_file}")

                # Load prediction file
                pred_df = pd.read_csv(pred_file)

                # Normalize player names to match boxscore results
                pred_df['Player_Normalized'] = (
                    pred_df['Player']
                    .astype(str)
                    .apply(clean_player_name)
                    .apply(normalize_name)
                    .str.lower()
                    .str.strip()
                )

                # Add Actual_Stat and Actual_Result columns if they don't exist
                if 'Actual_Stat' not in pred_df.columns:
                    # Insert Actual_Stat column before Actual_Result if it exists, otherwise at the end
                    if 'Actual_Result' in pred_df.columns:
                        actual_result_idx = pred_df.columns.get_loc('Actual_Result')
                        pred_df.insert(actual_result_idx, 'Actual_Stat', None)
                    else:
                        pred_df['Actual_Stat'] = None

                if 'Actual_Result' not in pred_df.columns:
                    # Add Actual_Result column after LLM_Justification
                    if 'LLM_Justification' in pred_df.columns:
                        llm_just_idx = pred_df.columns.get_loc('LLM_Justification')
                        pred_df.insert(llm_just_idx + 1, 'Actual_Result', None)
                    else:
                        pred_df['Actual_Result'] = None

                # Update with actual stats and results
                for idx, row in pred_df.iterrows():
                    player = row['Player_Normalized']
                    prop_type = row['Prop Type']
                    prop_value = row['Prop Value']
                    key = f"{player}|{prop_type}|{prop_value}"

                    if key in stat_lookup:
                        pred_df.at[idx, 'Actual_Stat'] = stat_lookup[key]
                        pred_df.at[idx, 'Actual_Result'] = result_lookup[key]

                # Drop the temporary normalized player column
                pred_df = pred_df.drop(columns=['Player_Normalized'])

                # Add Reflection column if it doesn't exist
                if 'Reflection' not in pred_df.columns:
                    # Insert Reflection column after Actual_Result
                    if 'Actual_Result' in pred_df.columns:
                        actual_result_idx = pred_df.columns.get_loc('Actual_Result')
                        pred_df.insert(actual_result_idx + 1, 'Reflection', None)
                    else:
                        pred_df['Reflection'] = None

                # Save updated prediction file
                pred_df.to_csv(pred_file, index=False)
                logging.info(f"Updated {sum(pred_df['Actual_Result'].notna())} results in {pred_file}")
            else:
                logging.warning(f"Prediction file not found: {pred_file}")

    except Exception as e:
        logging.error(f"Error updating prediction files: {e}")

# ─── fantasy scoring ───
def compute_hitter_score(r):
    H       = safe_float(r.get("H"))
    doubles = safe_float(r.get("2B"))
    triples = safe_float(r.get("3B"))
    hrs     = safe_float(r.get("HR"))
    runs    = safe_float(r.get("R"))
    rbis    = safe_float(r.get("RBI"))
    walks   = safe_float(r.get("BB"))
    hbp     = safe_float(r.get("HBP"))
    sb      = safe_float(r.get("SB"))
    singles = max(0.0, H - doubles - triples - hrs)
    return (
        singles*3 + doubles*5 + triples*8 + hrs*10 +
        runs*2 + rbis*2 + walks*2 + hbp*2 + sb*5
    )

def compute_pitcher_score(r):
    ip = safe_float(r.get("IP"))
    if pd.isna(ip):
        return -999.0  # skip broken row safely

    innings = int(ip)
    outs = int(round((ip - innings)*10))
    total_outs = innings * 3 + outs

    win = 6 if r.get("DEC") == "W" else 0
    qs = 4 if (innings >= 6 and safe_float(r.get("ER")) <= 3) else 0
    er_pts = safe_float(r.get("ER")) * -3
    so_pts = safe_float(r.get("SO")) * 3

    return win + qs + er_pts + so_pts + total_outs

# ─── fetch + parse StatMuse ───
async def fetch_html(url, retries=5):
    for i in range(retries):
        ua = random.choice(USER_AGENTS)
        try:
            async with aiohttp.ClientSession(headers={"User-Agent": ua}) as sess:
                async with sess.get(url, timeout=10) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    if resp.status in (403, 429):
                        logging.warning(f"Rate-limited({resp.status}); retry {i+1}")
        except Exception as e:
            logging.warning(f"Fetch error({e}); retry {i+1}")
        await asyncio.sleep(2**i * 0.5)
    logging.error(f"Failed to fetch {url}")
    return None

def parse_stats(html):
    soup = BeautifulSoup(html, "lxml")
    out  = {}
    for tbl in soup.select("div.relative.overflow-x-auto table"):
        headers = [th.get_text(strip=True) for th in tbl.select("thead th")]
        idx     = {h:i for i,h in enumerate(headers)}
        row     = tbl.select_one("tbody tr")
        if not row:
            continue
        vals = [td.get_text(strip=True) for td in row.select("td")]
        if HITTER_STATS & set(idx):
            for stat in HITTER_STATS:
                j = idx.get(stat)
                if j is not None and j < len(vals):
                    out[stat] = vals[j]
        if PITCHER_STATS & set(idx):
            for stat in PITCHER_STATS:
                j = idx.get(stat)
                if j is not None and j < len(vals):
                    out[stat] = vals[j]
    return out

async def scrape_player(player):
    url   = STATMUSE_URL.format(player=player.replace(" ", "-").lower())
    html  = await fetch_html(url)
    stats = parse_stats(html) if html else {}
    if stats:
        stats["Player"] = player
    return stats

# ─── main pipeline ───
async def main():
    date_str = input("Enter date (YYYY-MM-DD): ").strip()

    if not os.path.exists(INPUT_CSV):
        logging.error(f"Missing {INPUT_CSV}")
        return

    df = pd.read_csv(INPUT_CSV)
    df["Player"] = df["Player"].apply(clean_player_name).apply(normalize_name)

    players = df["Player"].dropna().unique().tolist()
    results = await asyncio.gather(*[scrape_player(p) for p in players])
    stats_df = pd.DataFrame(r for r in results if r)
    if stats_df.empty:
        logging.error("No stats scraped; aborting.")
        return

    merged = df.merge(stats_df, on="Player", how="left")

    # merge in API pitches & outs
    merged["Pitches Thrown"] = merged["Player"].map(
        lambda n: PITCHER_API_STATS.get(n, {}).get("Pitches Thrown", 0)
    )
    merged["Pitching Outs"] = merged["Player"].map(
        lambda n: PITCHER_API_STATS.get(n, {}).get("Pitching Outs", 0)
    )

    # split into hitter vs pitcher
    hitter_props = [
        "Hits", "Runs", "RBIs", "Walks", "Hitter Strikeouts", "Total Bases",
        "Hits+Runs+RBIs", "Hits+Runs", "Runs+RBIs", "Hitter Fantasy Score"
    ]
    pitcher_props = [
        "Pitcher Strikeouts", "Earned Runs Allowed",
        "Pitches Thrown", "Pitching Outs", "Pitcher Fantasy Score"
    ]

    hitter_temp = merged[merged["Prop Type"].isin(hitter_props)].copy()
    pitcher_temp = merged[merged["Prop Type"].isin(pitcher_props)].copy()

    # mappings
    HMAP = {
        "Hits": ["H"], "Runs": ["R"], "RBIs": ["RBI"],
        "Walks": ["BB"], "Hitter Strikeouts": ["SO"],
        "Total Bases": ["TB"], "Hits+Runs+RBIs": ["H", "R", "RBI"],
        "Hits+Runs": ["H", "R"], "Runs+RBIs": ["R", "RBI"]
    }
    PMAP = {
        "Pitcher Strikeouts": ["SO"],
        "Earned Runs Allowed": ["ER"],
        "Pitches Thrown": ["Pitches Thrown"],
        "Pitching Outs": ["Pitching Outs"]
    }

    # compute hitters
    def h_actual(r):
        pt = r["Prop Type"]
        if pt == "Hitter Fantasy Score":
            return compute_hitter_score(r)
        cols = HMAP.get(pt)
        return sum(safe_float(r.get(c)) for c in (cols or [])) if cols else -999.0

    hitter_temp["Actual Stat"] = hitter_temp.apply(h_actual, axis=1)
    hitter_temp["Hit"] = hitter_temp.apply(
        lambda r: -999 if r["Actual Stat"] == -999.0 else int(r["Actual Stat"] >= safe_float(r["Prop Value"])),
        axis=1
    )

    # compute pitchers
    def p_actual(r):
        pt = r["Prop Type"]
        if pt == "Pitcher Fantasy Score":
            return compute_pitcher_score(r)
        cols = PMAP.get(pt)
        return sum(safe_float(r.get(c)) for c in (cols or [])) if cols else -999.0

    pitcher_temp["Actual Stat"] = pitcher_temp.apply(p_actual, axis=1)
    pitcher_temp["Hit"] = pitcher_temp.apply(
        lambda r: -999 if r["Actual Stat"] == -999.0 else int(r["Actual Stat"] >= safe_float(r["Prop Value"])),
        axis=1
    )

    # Lowercase names
    hitter_temp["Player"] = hitter_temp["Player"].astype(str).str.lower().str.strip()
    pitcher_temp["Player"] = pitcher_temp["Player"].astype(str).str.lower().str.strip()

    # write out
    hitter_temp.to_csv(HITTER_OUT, index=False)
    pitcher_temp.to_csv(PITCHER_OUT, index=False)

    # Update prediction files with actual results
    await update_prediction_files(date_str)

    logging.info(f"Done → {HITTER_OUT}, {PITCHER_OUT}")

if __name__ == "__main__":
    asyncio.run(main())
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
HITTER_OUT   = "MLB_Prop_Data_CSV/hitter_temp_results.csv"
PITCHER_OUT  = "MLB_Prop_Data_CSV/pitcher_temp_results.csv"

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
    ip         = safe_float(r.get("IP"))
    innings    = int(ip)
    outs       = int(round((ip - innings)*10))
    total_outs = innings*3 + outs
    win   = 6 if r.get("DEC")=="W" else 0
    qs    = 4 if (innings>=6 and safe_float(r.get("ER"))<=3) else 0
    er_pts= safe_float(r.get("ER")) * -3
    so_pts= safe_float(r.get("SO")) * 3
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
        "Hits","Runs","RBIs","Walks","Hitter Strikeouts","Total Bases",
        "Hits+Runs+RBIs","Hits+Runs","Runs+RBIs","Hitter Fantasy Score"
    ]
    pitcher_props = [
        "Pitcher Strikeouts","Earned Runs Allowed",
        "Pitches Thrown","Pitching Outs","Pitcher Fantasy Score"
    ]

    hitter_temp  = merged[merged["Prop Type"].isin(hitter_props)].copy()
    pitcher_temp = merged[merged["Prop Type"].isin(pitcher_props)].copy()

    # mappings
    HMAP = {
        "Hits": ["H"], "Runs": ["R"], "RBIs": ["RBI"],
        "Walks": ["BB"], "Hitter Strikeouts": ["SO"],
        "Total Bases": ["TB"], "Hits+Runs+RBIs": ["H","R","RBI"],
        "Hits+Runs": ["H","R"], "Runs+RBIs": ["R","RBI"]
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
        lambda r: -999 if r["Actual Stat"]==-999.0 else int(r["Actual Stat"]>=safe_float(r["Prop Value"])),
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
        lambda r: -999 if r["Actual Stat"]==-999.0 else int(r["Actual Stat"]>=safe_float(r["Prop Value"])),
        axis=1
    )

    # write out
    hitter_temp.to_csv(HITTER_OUT, index=False)
    pitcher_temp.to_csv(PITCHER_OUT, index=False)
    logging.info(f"Done → {HITTER_OUT}, {PITCHER_OUT}")

    # Re-merge into one file for your model
    combined = pd.concat([hitter_temp, pitcher_temp], ignore_index=True)
    combined.to_csv("actual_results.csv", index=False)
    logging.info("Wrote combined actual_results.csv")

if __name__ == "__main__":
    asyncio.run(main())

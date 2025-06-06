#!/usr/bin/env python3
"""
mlb_lhp_avg.py
For each non-pitcher in mlb_prizepicks.csv, fetch their vs-LHP line from StatMuse
and extract only G, AB, H, HR, RBI, PA, AVG, OBP, SLG & OPS. Writes mlb_vs_lhp_stats.csv.
"""

import asyncio
import os
import sys
import logging
import unicodedata
import re
from io import StringIO

import aiohttp
import pandas as pd

# ──────────────────────────────────────────────────────────────────────────────
# Add project root so we can import your utils if needed
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
from Data_Extraction.utils import clean_player_name  # optional

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ── File paths ─────────────────────────────────────────────────────────────────
CSV_FOLDER = os.path.join(ROOT, "MLB_Prop_Data_CSV")
INPUT_CSV   = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
OUTPUT_CSV  = os.path.join(CSV_FOLDER, "mlb_vs_lhp_last10.csv")

# ── StatMuse URL template ─────────────────────────────────────────────────────
STATMUSE_URL = "https://www.statmuse.com/mlb/ask/{slug}-vs-left-handed-pitchers-last-10-games"

# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """Turn a player name into a clean ASCII slug for the URL."""
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = nfkd.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^\w\s-]", "", ascii_name).strip().lower()
    return re.sub(r"[\s_]+", "-", cleaned)

async def fetch_html(url: str, session: aiohttp.ClientSession) -> str:
    """Fetch the HTML text with up to 3 retries."""
    for i in range(3):
        try:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.text()
        except Exception as e:
            logging.warning(f"{e} on {url} (retry {i+1}/3)")
            await asyncio.sleep(1)
    logging.error(f"❌ Max retries reached for {url}")
    return ""

def extract_table_stats(html: str) -> dict:
    """
    Parse the first HTML table into a DataFrame and pull only:
      G, AB, H, HR, RBI, PA, AVG, OBP, SLG, OPS
    """
    cols = ["G","AB","H","HR","RBI","PA","AVG","OBP","SLG","OPS"]
    stats = {c: "N/A" for c in cols}

    if not html:
        return stats

    try:
        tables = pd.read_html(StringIO(html))
        df = tables[0]
        row = df.iloc[0]
    except Exception:
        logging.error("Failed to parse table; defaulting to N/A")
        return stats

    for c in cols:
        stats[c] = row[c] if c in df.columns else "N/A"
    return stats

async def scrape_player(player: str, session: aiohttp.ClientSession) -> dict:
    slug = slugify(player)
    url  = STATMUSE_URL.format(slug=slug)
    logging.info(f"Fetching {player} → {url}")
    html = await fetch_html(url, session)
    stats = extract_table_stats(html)
    return {"Player": player, **stats}

# ── Main orchestrator ─────────────────────────────────────────────────────────
async def main():
    if not os.path.exists(INPUT_CSV):
        logging.error(f"Input file not found: {INPUT_CSV}")
        return

    df = pd.read_csv(INPUT_CSV)
    # drop any pitcher
    df = df[df["Position"].str.upper() != "P"]
    players = df["Player"].dropna().unique().tolist()

    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks = [scrape_player(p, session) for p in players]
        records = await asyncio.gather(*tasks)

    out_df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    logging.info(f"✅ Wrote {len(out_df)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    asyncio.run(main())

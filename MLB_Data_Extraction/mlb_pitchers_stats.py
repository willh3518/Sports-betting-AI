#!/usr/bin/env python3
"""
mlb_pitcher_stats.py
Fetch each pitcher’s season-to-date numbers from StatMuse summary table and save:
  Player, G, W, L, ERA, SO, K/9, BB/9, K/BB, HR/9 & H/9
Pitchers with zero appearances are removed.
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
# CONFIG
ROOT       = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FOLDER = os.path.join(ROOT, "MLB_Prop_Data_CSV")
INPUT_CSV  = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
OUTPUT_CSV = os.path.join(CSV_FOLDER, "mlb_pitcher_stats.csv")
URL_TMPL   = "https://www.statmuse.com/mlb/ask/{slug}-pitching-this-year"

# The exact columns we want from the summary table
STATS_COLS = ["G","W","L","ERA","SO","K/9","BB/9","K/BB","HR/9","H/9"]

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def slugify(name: str) -> str:
    """Normalize accents → ASCII, drop punctuation, lowercase & hyphenate."""
    nfkd = unicodedata.normalize("NFKD", name)
    ascii_name = nfkd.encode("ascii", "ignore").decode("ascii")
    cleaned = re.sub(r"[^\w\s-]", "", ascii_name).strip().lower()
    return re.sub(r"[\s_]+", "-", cleaned)

async def fetch_html(url: str, session: aiohttp.ClientSession) -> str:
    """GET the URL up to 3 times; return text or empty string."""
    for i in range(3):
        try:
            async with session.get(url) as r:
                r.raise_for_status()
                return await r.text()
        except Exception as e:
            logging.warning(f"{e} on {url} (retry {i+1}/3)")
            await asyncio.sleep(1)
    logging.error(f"❌ Max retries reached for {url}")
    return ""

def extract_pitcher_stats(html: str) -> dict:
    """
    Parse the summary table to pull:
      G, W, L, ERA, SO, K/9, BB/9, K/BB, HR/9, H/9
    """
    stats = {c: "N/A" for c in STATS_COLS}
    if not html:
        return stats

    try:
        tables = pd.read_html(StringIO(html))
        # pick first table that has both W & L columns
        df = next((t for t in tables if {"W","L"}.issubset(t.columns)), None)
        if df is not None and not df.empty:
            row = df.iloc[0]
            for col in STATS_COLS:
                stats[col] = row.get(col, "N/A")
        else:
            logging.error("⚠️ Could not find summary table with W & L columns")
    except Exception as e:
        logging.error(f"⚠️ Failed to parse summary table: {e}")

    return stats

async def scrape_player(player: str, session: aiohttp.ClientSession) -> dict:
    slug = slugify(player)
    url  = URL_TMPL.format(slug=slug)
    logging.info(f"Fetching {player} → {url}")
    html = await fetch_html(url, session)
    return {"Player": player, **extract_pitcher_stats(html)}

# ── Main ───────────────────────────────────────────────────────────────────────
async def main():
    if not os.path.exists(INPUT_CSV):
        logging.error(f"Input file not found: {INPUT_CSV}")
        return

    df = pd.read_csv(INPUT_CSV)
    pitchers = df[df["Position"].str.upper() == "P"]["Player"].dropna().unique().tolist()

    async with aiohttp.ClientSession(trust_env=True) as session:
        tasks   = [scrape_player(p, session) for p in pitchers]
        records = await asyncio.gather(*tasks)

    # build DataFrame
    out_df = pd.DataFrame(records, columns=["Player"] + STATS_COLS)

    # ── Filter out anyone with zero or non-numeric appearances (G) ────────────
    # convert G to numeric, coerce errors to NaN, then keep only >0
    out_df["G"] = pd.to_numeric(out_df["G"], errors="coerce")
    out_df = out_df[out_df["G"] > 0]

    # restore G to int for neatness
    out_df["G"] = out_df["G"].astype(int)

    # ── Save CSV ─────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    logging.info(f"✅ Wrote {len(out_df)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    asyncio.run(main())

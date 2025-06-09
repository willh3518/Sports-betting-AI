#!/usr/bin/env python3
"""
mlb_pitcher_stats.py
Fetch each pitcher season-to-date numbers from StatMuse summary table and save:
  Player, G, W, L, ERA, SO, K/9, BB/9, K/BB, HR/9 & H/9
Pitchers with zero appearances are removed.
"""

import asyncio
import os
import logging
from io import StringIO
import pandas as pd
from mlb_utils import fetch_html, normalize_name

# CONFIG
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FOLDER = os.path.join(ROOT, "MLB_Prop_Data_CSV")
INPUT_CSV = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
OUTPUT_CSV = os.path.join(CSV_FOLDER, "mlb_pitcher_stats.csv")
URL_TMPL = "https://www.statmuse.com/mlb/ask/{slug}-pitching-this-year"

# The exact columns we want from the summary table
STATS_COLS = ["G","W","L","ERA","SO","K/9","BB/9","K/BB","HR/9","H/9"]

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

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
            logging.error(" Could not find summary table with W & L columns")
    except Exception as e:
        logging.error(f" Failed to parse summary table: {e}")

    return stats

async def scrape_player(player: str) -> dict:
    """Scrape stats for a single player."""
    normalized_name = normalize_name(player)
    url = URL_TMPL.format(slug=normalized_name.lower().replace(" ", "-"))
    logging.info(f"Fetching {player} from {url}")
    html = await fetch_html(url)
    return {"Player": player, **extract_pitcher_stats(html)}

async def main():
    """Main execution function."""
    if not os.path.exists(INPUT_CSV):
        logging.error(f"Input file not found: {INPUT_CSV}")
        return

    df = pd.read_csv(INPUT_CSV)
    pitchers = df[df["Position"].str.upper() == "P"]["Player"].dropna().unique().tolist()

    tasks = [scrape_player(p) for p in pitchers]
    records = await asyncio.gather(*tasks)

    # build DataFrame
    out_df = pd.DataFrame(records, columns=["Player"] + STATS_COLS)

    # Filter out anyone with zero or non-numeric appearances (G)
    out_df["G"] = pd.to_numeric(out_df["G"], errors="coerce")
    out_df = out_df[out_df["G"] > 0]

    # restore G to int for neatness
    out_df["G"] = out_df["G"].astype(int)

    # Save CSV
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    logging.info(f" Wrote {len(out_df)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    asyncio.run(main())
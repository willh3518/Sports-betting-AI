#!/usr/bin/env python3
"""
mlb_rhp_last5.py
For each non-pitcher in mlb_prizepicks.csv, fetch their vs-RHP stats for last 5 games from StatMuse
and extract only G, AB, H, HR, RBI, PA, AVG, OBP, SLG & OPS. Writes mlb_vs_rhp_last5.csv.
"""

import asyncio
import os
import logging
from io import StringIO
import pandas as pd
from mlb_utils import fetch_html, normalize_name

# File paths
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CSV_FOLDER = os.path.join(ROOT, "MLB_Prop_Data_CSV")
INPUT_CSV = os.path.join(CSV_FOLDER, "mlb_prizepicks.csv")
OUTPUT_CSV = os.path.join(CSV_FOLDER, "mlb_vs_rhp_last5.csv")

# StatMuse URL template
STATMUSE_URL = "https://www.statmuse.com/mlb/ask/{slug}-vs-right-handed-pitchers-last-5-games"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

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

async def scrape_player(player: str) -> dict:
    """Scrape stats for a single player."""
    normalized_name = normalize_name(player)
    url = STATMUSE_URL.format(slug=normalized_name.lower().replace(" ", "-"))
    logging.info(f"Fetching {player} from {url}")
    html = await fetch_html(url)
    stats = extract_table_stats(html)
    return {"Player": player, **stats}

async def main():
    """Main execution function."""
    if not os.path.exists(INPUT_CSV):
        logging.error(f"Input file not found: {INPUT_CSV}")
        return

    df = pd.read_csv(INPUT_CSV)
    # drop any pitcher
    df = df[df["Position"].str.upper() != "P"]
    players = df["Player"].dropna().unique().tolist()

    tasks = [scrape_player(p) for p in players]
    records = await asyncio.gather(*tasks)

    out_df = pd.DataFrame(records)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    logging.info(f" Wrote {len(out_df)} rows to {OUTPUT_CSV}")

if __name__ == "__main__":
    asyncio.run(main())
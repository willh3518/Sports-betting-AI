# mlb_pitcher_pitch_usage.py

import os
import re
import time
import unicodedata
import requests
import pandas as pd
from bs4 import BeautifulSoup

# ─────────────────────────────────────────────────────────
# 1) Helper: slugify a player name so it matches Savant’s URL pattern
#    (e.g. “Zack Wheeler” → “zack-wheeler”, “José Altuve” → “jose-altuve”)
# ─────────────────────────────────────────────────────────
def slugify(name: str) -> str:
    """
    Convert a player name into a lowercase, hyphenated,
    ASCII-only slug. E.g. “Zack Wheeler” → “zack-wheeler”.
    """
    # 1) Normalize to NFD, strip diacritics
    normalized = unicodedata.normalize('NFD', name)
    no_diacritics = ''.join(ch for ch in normalized if unicodedata.category(ch) != 'Mn')
    # 2) Lowercase
    lower = no_diacritics.lower()
    # 3) Replace anything that is not a letter/number/space with empty string
    alnum_space = re.sub(r'[^a-z0-9 ]+', '', lower)
    # 4) Collapse multiple spaces, then replace spaces with hyphens
    collapse_spaces = re.sub(r'\s+', ' ', alnum_space).strip()
    slug = collapse_spaces.replace(' ', '-')
    return slug

# ─────────────────────────────────────────────────────────
# 2) Scrape a single Savant page for the “pitch‐usage” block
#    returns a dict { "Four Seamer": "41.6%", "Sinker": "15.3%", … }
# ─────────────────────────────────────────────────────────
def fetch_pitch_usage_for(mlb_id: str, player_name: str) -> dict:
    """
    Given an MLB_ID and a player_name (e.g. "Zack Wheeler"),
    build the Savant URL, fetch the page, and parse out the
    <div style="position: relative; line-height: 2.5rem;"> block.  Return
    a dict of {pitch_name: usage_pct_string}.
    """

    base_url = "https://baseballsavant.mlb.com/savant-player"
    slug = slugify(player_name)
    url = f"{base_url}/{slug}-{mlb_id}?stats=statcast-r-pitching-mlb"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; Python script)"
    }

    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        print(f"  → WARNING: Could not fetch {player_name} ({mlb_id}) at {url}")
        return {}

    soup = BeautifulSoup(resp.text, "html.parser")

    # Look for the exact style attribute that contains BOTH substrings:
    #   position: relative
    #   line-height: 2.5rem
    container = soup.find(
        "div",
        attrs={"style": lambda v: v
               and "position: relative" in v
               and "line-height: 2.5rem" in v}
    )
    if container is None:
        print(f"  → WARNING: No 'pitch-usage' div found for {player_name} ({mlb_id}).")
        return {}

    usage = {}
    # Inside that container, each pitch is in <div class="spin-pitches">
    for pitch_div in container.find_all("div", class_="spin-pitches"):
        # The first child <div> with inline color style is the pitch name
        name_div = pitch_div.find("div", attrs={"style": lambda v: v and "color" in v})
        # The next child <div> holds something like "(41.6%) ," or "(15.3%) ,"
        pct_divs = pitch_div.find_all("div", attrs={"style": lambda v: not (v and "color" in v)})

        if not name_div or not pct_divs:
            continue

        pitch_name = name_div.get_text(strip=True)
        raw_pct = pct_divs[0].get_text(strip=True)  # e.g. "(41.6%) ,"

        # Extract the "XX.X%" from within parentheses
        m = re.search(r"(\d+(\.\d+)?%)", raw_pct)
        pct_str = m.group(1) if m else raw_pct.strip("(), ")

        usage[pitch_name] = pct_str

    return usage

# ─────────────────────────────────────────────────────────
# 3) Main routine: read both CSVs, loop through each pitcher, scrape usage, build DataFrame
# ─────────────────────────────────────────────────────────
def main():
    # 3a) Paths to your CSVs (adjust these relative paths if necessary)
    prizepicks_path = os.path.join("../MLB_Prop_Data_CSV", "mlb_prizepicks.csv")
    fg_ids_path     = os.path.join("../MLB_Prop_Data_CSV", "player_fg_ids.csv")
    output_path     = os.path.join("../MLB_Prop_Data_CSV", "mlb_pitcher_pitch_usage.csv")

    # 3b) Load the “PrizePicks” file and filter to “Position == 'P'”
    df_prize = pd.read_csv(prizepicks_path, dtype=str)
    df_prize["Position"] = df_prize["Position"].astype(str).str.strip()
    pitchers_today = df_prize.loc[df_prize["Position"] == "P", "Player"].unique()

    # 3c) Load the FG IDs file so we can look up each pitcher’s MLB_ID
    df_ids = pd.read_csv(fg_ids_path, dtype=str)
    df_ids["Player"] = df_ids["Player"].astype(str).str.strip()

    # 3d) For each pitcher, grab their MLB_ID, then call fetch_pitch_usage_for(…).
    rows = []
    all_pitch_names = set()

    for pitcher in pitchers_today:
        pitcher = pitcher.strip()
        # Look up MLB_ID
        match = df_ids.loc[df_ids["Player"] == pitcher]
        if match.empty:
            print(f"⚠️  No MLB_ID found for '{pitcher}' in player_fg_ids.csv. Skipping.")
            continue

        mlb_id = match.iloc[0]["MLB_ID"]

        print(f"Fetching usage for {pitcher} ({mlb_id}) …")
        usage_dict = fetch_pitch_usage_for(mlb_id, pitcher)

        # Keep track of which pitch names we saw overall
        all_pitch_names.update(usage_dict.keys())

        # Build one row for this pitcher. Include Player + MLB_ID + each pitch usage.
        row = {
            "Player": pitcher,
            "MLB_ID": mlb_id
        }
        # Insert each (pitch_name → pct) into the row
        for nm, pct in usage_dict.items():
            row[nm] = pct

        rows.append(row)

        # Be polite and don’t hammer the server. Sleep 1–2s between requests
        time.sleep(1.5)

    # 3e) Now build a DataFrame. Any missing pitch (for a given pitcher) → NaN, then fill with "N/A"
    if not rows:
        print("No pitchers were successfully fetched. Exiting.")
        return

    df_out = pd.DataFrame(rows)
    # Guarantee that every column for every pitch name exists (even if some pitchers didn’t throw it)
    for pitch_name in sorted(all_pitch_names):
        if pitch_name not in df_out.columns:
            df_out[pitch_name] = pd.NA

    # Fill missing usage with "N/A"
    df_out = df_out.fillna("N/A")

    # 3f) Save to CSV
    df_out.to_csv(output_path, index=False)
    print(f"\n✅  Done. Wrote output to '{output_path}'.")

if __name__ == "__main__":
    main()

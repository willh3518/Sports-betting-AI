import os, unidecode
import time
import pandas as pd
from requests_html import HTMLSession

# ────────────────────────────────────────────────────────────────────────────────
# 1) CONFIGURATION
# ────────────────────────────────────────────────────────────────────────────────
PRIZEPICKS_CSV   = "../MLB_Prop_Data_CSV/mlb_prizepicks.csv"
ID_MAPPING_CSV   = "../MLB_Prop_Data_CSV/player_fg_ids.csv"
OUTPUT_CSV       = "../MLB_Prop_Data_CSV/mlb_pitcher_hotzones.csv"

SWING_TAKE_URL_TEMPLATE = (
    "https://baseballsavant.mlb.com/visuals/swing-take"
    "?playerId={mlb_id}"
    "&playerSet=hitters"
)

MAX_RENDER_ATTEMPTS   = 3    # how many times to retry rendering before giving up
RENDER_SLEEP_SECONDS  = 2    # seconds to wait after calling r.html.render()
BETWEEN_ATTEMPT_SLEEP = 1    # seconds to wait between retry attempts
BETWEEN_PLAYER_SLEEP  = 1    # polite pause after each pitcher

# ────────────────────────────────────────────────────────────────────────────────
# 2) LOAD PRIZEPICKS AND ID MAPPING
# ────────────────────────────────────────────────────────────────────────────────
if not os.path.isfile(PRIZEPICKS_CSV):
    raise FileNotFoundError(f"Could not find `{PRIZEPICKS_CSV}`.")
if not os.path.isfile(ID_MAPPING_CSV):
    raise FileNotFoundError(f"Could not find `{ID_MAPPING_CSV}` (Player→MLB_ID).")

# 2a) PrizePicks list of players (expects a "Player" column)
df_prize = pd.read_csv(PRIZEPICKS_CSV)
if "Player" not in df_prize.columns:
    raise KeyError("`mlb_prizepicks.csv` needs a column named `Player` (Firstname Lastname).")
df_prize["Player"] = df_prize["Player"].astype(str).str.strip()

# ───── INSERT NORMALIZATION FUNCTION & APPLY TO df_prize ─────
name_corrections = {
    "Dj Lemahieu": "DJ LeMahieu",
    "Jp Crawford": "JP Crawford",
    "Tj Friedl": "TJ Friedl",
    "Cj Abrams": "CJ Abrams",
    "Andrew Mccutchen": "Andrew McCutchen",
    "Matt Mclain": "Matt McLain"   # ← Add this line
}

def normalize_name(name):
    name = str(name)
    name = unidecode.unidecode(name)
    name = name.replace(".", "").replace("Jr", "").replace("II", "").replace("III", "").strip()
    name = " ".join(name.split())
    name = name.title()
    return name_corrections.get(name, name)

df_prize["Player"] = df_prize["Player"].map(normalize_name)

# 2b) Mapping file from PrizePicks name → MLB Statcast ID and FG_Position
df_map = pd.read_csv(ID_MAPPING_CSV)
if "MLB_ID" not in df_map.columns:
    raise KeyError("`player_fg_ids.csv` must contain a column named `MLB_ID`.")
df_map = df_map.rename(columns={"MLB_ID": "mlb_id"})

required_map_cols = {"Player", "mlb_id", "FG_ID", "FG_Position"}
if not required_map_cols.issubset(df_map.columns):
    raise KeyError(
        "`player_fg_ids.csv` must contain columns `Player`, `MLB_ID` (renamed to `mlb_id`), "
        "`FG_ID`, and `FG_Position`."
    )
df_map["Player"] = df_map["Player"].astype(str).str.strip()

# 2c) Merge so each PrizePicks player has mlb_id and FG_Position
df_merged = pd.merge(
    df_prize[["Player"]].drop_duplicates(),
    df_map[["Player", "mlb_id", "FG_ID", "FG_Position"]],
    on="Player",
    how="left"
)
missing_ids = df_merged[df_merged["mlb_id"].isna()]["Player"].tolist()
if missing_ids:
    raise RuntimeError(
        "The following PrizePicks players have no mlb_id in your mapping CSV:\n"
        + "\n".join(missing_ids)
    )

# 2d) Filter down to pitchers only (FG_Position == "P")
df_pitchers = df_merged[df_merged["FG_Position"].astype(str).str.upper() == "P"].copy()
if df_pitchers.empty:
    raise RuntimeError("No pitchers found under `FG_Position == 'P'` in your merged PrizePicks list.")

# ────────────────────────────────────────────────────────────────────────────────
# 3) HELPER: extract pitch-frequency counts + percentages from the SVG
# ────────────────────────────────────────────────────────────────────────────────
def extract_pitch_frequency(zone_map_element, zone_name):
    """
    Given the <g class="main"> root of the rendered SVG, and a zone name
    ("heart", "shadow", "chase", or "waste"), this finds
    <g class="zone-region-pitch-frequency"> → <g class="{zone_name}">,
    and returns a tuple (count:int, pct:float). If something is missing, returns (0, 0.0).
    """
    selector = f"g.zone-region-pitch-frequency g.{zone_name}"
    grp = zone_map_element.find(selector, first=True)
    if not grp:
        return 0, 0.0

    all_text_nodes = grp.find("text")
    if not all_text_nodes or len(all_text_nodes) < 2:
        return 0, 0.0

    # 1) raw count
    raw_count_text = all_text_nodes[0].text.strip()
    try:
        count = int(raw_count_text)
    except ValueError:
        count = 0

    # 2) percentage (take the first part before "%")
    pct_text = all_text_nodes[1].text.strip()  # e.g. "27% (27%)"
    try:
        pct_val = float(pct_text.split("%")[0])
    except Exception:
        pct_val = 0.0

    return count, pct_val

# ────────────────────────────────────────────────────────────────────────────────
# 4) MAIN: sequential rendering but reusing one session + batch-write CSV
# ────────────────────────────────────────────────────────────────────────────────
def main():
    # Create one HTMLSession and reuse it for all pitchers
    session = HTMLSession()

    results = []  # will store dicts for each pitcher

    for _, pitcher_row in df_pitchers.iterrows():
        player_name = pitcher_row["Player"]
        mlb_id      = pitcher_row["mlb_id"]
        url         = SWING_TAKE_URL_TEMPLATE.format(mlb_id=mlb_id)

        print(f"▶ Fetching pitch-frequency for {player_name} (mlb_id={mlb_id})…")

        # Retry loop that reuses the same session
        zone_map_element = None
        attempt = 0
        while attempt < MAX_RENDER_ATTEMPTS and zone_map_element is None:
            try:
                r = session.get(url)
                r.html.render(sleep=RENDER_SLEEP_SECONDS)
                zone_map_element = r.html.find("g.main", first=True)
                if zone_map_element:
                    break
            except Exception:
                zone_map_element = None

            attempt += 1
            if zone_map_element is None:
                print(f"   – Attempt {attempt} failed, retrying in {BETWEEN_ATTEMPT_SLEEP}s…")
                time.sleep(BETWEEN_ATTEMPT_SLEEP)

        # If we still don’t have <g class="main">, record zeros
        if not zone_map_element:
            print(f"⚠️  Could not find <g class='main'> after {MAX_RENDER_ATTEMPTS} tries for {player_name}. Writing zeros.")
            results.append({
                "Player":       player_name,
                "Heart_Count":  0, "Heart_Pct":  0.0,
                "Shadow_Count": 0, "Shadow_Pct": 0.0,
                "Chase_Count":  0, "Chase_Pct":  0.0,
                "Waste_Count":  0, "Waste_Pct":  0.0,
            })
            time.sleep(BETWEEN_PLAYER_SLEEP)
            continue

        # Extract counts + percentages for each zone
        heart_cnt,  heart_pct  = extract_pitch_frequency(zone_map_element, "heart")
        shadow_cnt, shadow_pct = extract_pitch_frequency(zone_map_element, "shadow")
        chase_cnt,  chase_pct  = extract_pitch_frequency(zone_map_element, "chase")
        waste_cnt,  waste_pct  = extract_pitch_frequency(zone_map_element, "waste")

        results.append({
            "Player":       player_name,
            "Heart_Count":  heart_cnt,  "Heart_Pct":  heart_pct,
            "Shadow_Count": shadow_cnt, "Shadow_Pct": shadow_pct,
            "Chase_Count":  chase_cnt,  "Chase_Pct":  chase_pct,
            "Waste_Count":  waste_cnt,  "Waste_Pct":  waste_pct,
        })

        print(
            f"✅  Extracted frequencies for {player_name} → "
            f"Heart={heart_cnt} ({heart_pct}%), "
            f"Shadow={shadow_cnt} ({shadow_pct}%), "
            f"Chase={chase_cnt} ({chase_pct}%), "
            f"Waste={waste_cnt} ({waste_pct}%)"
        )

        time.sleep(BETWEEN_PLAYER_SLEEP)

    session.close()

    # Batch-write results to CSV via pandas
    df_out = pd.DataFrame(results, columns=[
        "Player",
        "Heart_Count", "Heart_Pct",
        "Shadow_Count", "Shadow_Pct",
        "Chase_Count", "Chase_Pct",
        "Waste_Count", "Waste_Pct"
    ])
    df_out.to_csv(OUTPUT_CSV, index=False)
    print(f"\n✅  Finished writing {len(df_out)} pitchers to `{OUTPUT_CSV}`.")

if __name__ == "__main__":
    main()
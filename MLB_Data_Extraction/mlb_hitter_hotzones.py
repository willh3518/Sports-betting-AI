import os
import time
import csv
import pandas as pd
from requests_html import HTMLSession
import unicodedata
import re

# ────────────────────────────────────────────────────────────────────────────────
# CONFIGURATION
# ────────────────────────────────────────────────────────────────────────────────
PRIZEPICKS_CSV = "../MLB_Prop_Data_CSV/mlb_prizepicks.csv"
ID_MAPPING_CSV = "../MLB_Prop_Data_CSV/player_fg_ids.csv"      # must contain: Player, MLB_ID, FG_ID, FG_Position
OUTPUT_CSV     = "../MLB_Prop_Data_CSV/mlb_hitter_hotzones.csv"

SWING_TAKE_URL_TEMPLATE = (
    "https://baseballsavant.mlb.com/visuals/swing-take"
    "?playerId={mlb_id}"
    "&playerSet=hitters"
)

MAX_RENDER_ATTEMPTS = 3   # how many times to retry rendering before giving up
RENDER_SLEEP_SECONDS = 2  # how long to wait after calling r.html.render()

# ────────────────────────────────────────────────────────────────────────────────
# VALIDATE INPUT FILES
# ────────────────────────────────────────────────────────────────────────────────
if not os.path.isfile(PRIZEPICKS_CSV):
    raise FileNotFoundError(f"Could not find `{PRIZEPICKS_CSV}`.")

if not os.path.isfile(ID_MAPPING_CSV):
    raise FileNotFoundError(f"Could not find `{ID_MAPPING_CSV}` (Player→MLB_ID mapping).")

def normalize_name(name):
    import unicodedata
    import re

    # Remove accents
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode()
    # Remove common suffixes
    name = re.sub(r'\b(JR\.?|SR\.?|III|II|IV)\b', '', name, flags=re.IGNORECASE)
    # Remove all periods
    name = name.replace('.', '')
    # Fix known typos
    name = name.replace('GURRIEL', 'GURRIEL')  # in case typo was upstream
    # Normalize spaces and case
    name = ' '.join(name.upper().split())
    return name

# ────────────────────────────────────────────────────────────────────────────────
# LOAD PRIZEPICKS (HITTERS) AND ID MAPPING
# ────────────────────────────────────────────────────────────────────────────────

# 1) Read PrizePicks list of batters (expects a "Player" column)
df_prize = pd.read_csv(PRIZEPICKS_CSV)
if "Player" not in df_prize.columns:
    raise KeyError("`mlb_prizepicks.csv` needs a column named `Player` (Firstname Lastname).")
df_prize["Player"] = df_prize["Player"].astype(str).apply(normalize_name)

# 2) Read FG→MLB mapping (must contain: Player, MLB_ID, FG_ID, FG_Position)
df_map = pd.read_csv(ID_MAPPING_CSV)
required_cols = {"Player", "MLB_ID", "FG_ID", "FG_Position"}
if not required_cols.issubset(df_map.columns):
    missing = required_cols - set(df_map.columns)
    raise KeyError(f"`player_fg_ids.csv` is missing columns: {missing}")

# Rename columns to consistent names
df_map = df_map.rename(columns={
    "MLB_ID": "mlb_id",
    "FG_ID": "player_fg_id"
})
df_map["Player"] = df_map["Player"].astype(str).apply(normalize_name)

# 3) Merge PrizePicks batters with their mlb_id, player_fg_id, FG_Position
df_merged = pd.merge(
    df_prize[["Player"]].drop_duplicates(),
    df_map[["Player", "mlb_id", "player_fg_id", "FG_Position"]],
    on="Player",
    how="left"
)

# 4) Check for any missing mlb_id
missing = df_merged[df_merged["mlb_id"].isna()]["Player"].tolist()
if missing:
    raise RuntimeError(
        "The following PrizePicks hitters have no mlb_id in your mapping CSV:\n"
        + "\n".join(missing)
    )

# 5) Filter out any player whose FG_Position is exactly "P" (i.e. skip pitchers)
df_hitters = df_merged[df_merged["FG_Position"].astype(str).str.strip() != "P"].copy()
if df_hitters.empty:
    raise RuntimeError("After filtering out pitchers, no hitters remain.")

# ────────────────────────────────────────────────────────────────────────────────
# HELPER: Extract swing‐take counts for a given zone from <g class="main">
# ────────────────────────────────────────────────────────────────────────────────
def extract_counts(zone_map_element, zone_name):
    """
    zone_map_element: a <g class="main"> object returned by requests_html
    zone_name: one of "heart", "shadow", "chase", or "waste"
    Returns (swing_count:int, take_count:int)
    """
    selector = f"g.zone-region-swing-take g.{zone_name}"
    grp = zone_map_element.find(selector, first=True)
    if not grp:
        return 0, 0

    swing_node = grp.find("text.player-swing-count", first=True)
    take_node  = grp.find("text.player-take-count", first=True)

    try:
        swing = int(swing_node.text) if swing_node else 0
    except (ValueError, AttributeError):
        swing = 0

    try:
        take = int(take_node.text) if take_node else 0
    except (ValueError, AttributeError):
        take = 0

    return swing, take

# ────────────────────────────────────────────────────────────────────────────────
# HELPER: Extract run‐value for a given zone from <g class="zone-map">
# ────────────────────────────────────────────────────────────────────────────────
def extract_run_value(zone_map_element, zone_name):
    """
    zone_map_element: a <g class="main"> object returned by requests_html
    zone_name: one of "heart", "shadow", "chase", or "waste"
    Returns the run‐value (an integer, possibly negative or positive) for that zone.
    If missing, returns 0.
    """
    selector = f"g.zone-map g.labels text.label-{zone_name}"
    node = zone_map_element.find(selector, first=True)
    if not node:
        return 0

    raw = node.text.strip()    # e.g. "+3 Runs" or "-5 Runs"
    parts = raw.split()        # ["+3", "Runs"]
    if not parts:
        return 0

    num_str = parts[0]         # "+3" or "-5"
    try:
        return int(num_str)
    except ValueError:
        try:
            return int(num_str.replace("+", ""))
        except ValueError:
            return 0

# ────────────────────────────────────────────────────────────────────────────────
# SCRAPE Swing/Take SVG AND RUN‐VALUE FOR EACH HITTER → WRITE CSV
# with up to 3 render attempts before giving up
# ────────────────────────────────────────────────────────────────────────────────

with open(OUTPUT_CSV, mode="w", newline="") as csvfile_out:
    writer = csv.writer(csvfile_out)

    # Write header (we’ve added four new “_<zone>_Run” columns)
    writer.writerow([
        "Player",
        "Heart_Swing", "Heart_Take",
        "Shadow_Swing", "Shadow_Take",
        "Chase_Swing", "Chase_Take",
        "Waste_Swing", "Waste_Take",
        "Heart_Run", "Shadow_Run", "Chase_Run", "Waste_Run"
    ])

    for idx, row in df_hitters.iterrows():
        player_name = row["Player"]
        fg_id       = row["player_fg_id"]
        mlb_id      = row["mlb_id"]

        savant_url = SWING_TAKE_URL_TEMPLATE.format(mlb_id=mlb_id)
        session    = HTMLSession()

        print(f"▶ Fetching Swing/Take + Run‐Value for {player_name} (mlb_id={mlb_id})…")

        # ────────────────────────────────────────────────────────────────────
        # RETRY LOOP: attempt to render up to MAX_RENDER_ATTEMPTS times
        # ────────────────────────────────────────────────────────────────────
        zone_map_element = None
        attempt = 0

        while attempt < MAX_RENDER_ATTEMPTS and zone_map_element is None:
            try:
                r = session.get(savant_url)
                r.html.render(sleep=RENDER_SLEEP_SECONDS)
                zone_map_element = r.html.find("g.main", first=True)
                if zone_map_element:
                    break
            except Exception as e:
                # If rendering or finding fails, swallow exception for retry
                zone_map_element = None

            attempt += 1
            if not zone_map_element:
                print(f"   – Attempt {attempt} failed, retrying in 1s…")
                time.sleep(1)

        # ────────────────────────────────────────────────────────────────────
        # If we still don’t have <g class="main">, write zeros
        # ────────────────────────────────────────────────────────────────────
        if not zone_map_element:
            print(f"⚠️  Could not find <g class='main'> after {MAX_RENDER_ATTEMPTS} tries for {player_name}. Writing zeros.")
            writer.writerow([
                player_name,
                0, 0,    # Heart Swing, Heart Take
                0, 0,    # Shadow Swing, Shadow Take
                0, 0,    # Chase Swing, Chase Take
                0, 0,    # Waste Swing, Waste Take
                0,       # Heart_Run
                0,       # Shadow_Run
                0,       # Chase_Run
                0        # Waste_Run
            ])
            time.sleep(1)
            continue

        # ────────────────────────────────────────────────────────────────────
        # 1) Extract swing/take counts for each zone
        # ────────────────────────────────────────────────────────────────────
        heart_swing,  heart_take  = extract_counts(zone_map_element, "heart")
        shadow_swing, shadow_take = extract_counts(zone_map_element, "shadow")
        chase_swing,  chase_take  = extract_counts(zone_map_element, "chase")
        waste_swing,  waste_take  = extract_counts(zone_map_element, "waste")

        # ────────────────────────────────────────────────────────────────────
        # 2) Extract run‐values for each zone
        # ────────────────────────────────────────────────────────────────────
        heart_run  = extract_run_value(zone_map_element, "heart")
        shadow_run = extract_run_value(zone_map_element, "shadow")
        chase_run  = extract_run_value(zone_map_element, "chase")
        waste_run  = extract_run_value(zone_map_element, "waste")

        # ────────────────────────────────────────────────────────────────────
        # 3) Write one row to CSV
        # ────────────────────────────────────────────────────────────────────
        writer.writerow([
            player_name,
            heart_swing,  heart_take,
            shadow_swing, shadow_take,
            chase_swing,  chase_take,
            waste_swing,  waste_take,
            heart_run,
            shadow_run,
            chase_run,
            waste_run
        ])

        print(
            f"✅  {player_name} → "
            f"Heart: SW/TK=({heart_swing}/{heart_take}), RV={heart_run}; "
            f"Shadow: SW/TK=({shadow_swing}/{shadow_take}), RV={shadow_run}; "
            f"Chase: SW/TK=({chase_swing}/{chase_take}), RV={chase_run}; "
            f"Waste: SW/TK=({waste_swing}/{waste_take}), RV={waste_run}"
        )
        time.sleep(1)  # polite pause before next request

print(f"\n✅  Finished! All hitter hot‐zone data (counts + run‐values) written to `{OUTPUT_CSV}`.")

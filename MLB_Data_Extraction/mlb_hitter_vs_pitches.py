import os
import requests
import pandas as pd
import io

# ——————————————————————————————————————————————————————
# 1) CONFIGURATION
# ——————————————————————————————————————————————————————
PRIZEPICKS_CSV = "../MLB_Prop_Data_CSV/mlb_prizepicks.csv"
OUTPUT_CSV     = "../MLB_Prop_Data_CSV/mlb_hitter_vs_pitchtype.csv"

# This is the “pitch-arsenal-stats” URL with &csv=true
CSV_URL = (
    "https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats"
    "?type=batter"
    "&pitchType="
    "&year=2025"
    "&team="
    "&min=1"
    "&minPitches=q"
    "&sort=4"
    "&sortDir=desc"
    "&csv=true"
)

# ——————————————————————————————————————————————————————
# 2) LOAD YOUR PRIZEPICKS LIST
# ——————————————————————————————————————————————————————
if not os.path.isfile(PRIZEPICKS_CSV):
    raise FileNotFoundError(f"Could not find `{PRIZEPICKS_CSV}` in this folder.")

df_prize = pd.read_csv(PRIZEPICKS_CSV)
if "Player" not in df_prize.columns:
    raise KeyError("`mlb_prizepicks.csv` needs a column named `Player` (Firstname Lastname).")

hitters_today = set(df_prize["Player"].dropna().str.strip().tolist())
if not hitters_today:
    raise ValueError("No valid `Player` names found in PrizePicks CSV.")

# ——————————————————————————————————————————————————————
# 3) DOWNLOAD THE CSV AND PARSE IT
# ——————————————————————————————————————————————————————
print("▶  Fetching CSV from Baseball Savant…")
resp = requests.get(CSV_URL)
resp.raise_for_status()

# Use Python's io.StringIO (not pandas.compat.StringIO)
df_savant = pd.read_csv(io.StringIO(resp.text))

# Show the actual columns so you can verify
print("✔ Savant returned columns:", list(df_savant.columns))

# We expect at least these six columns to exist in the real CSV:
#   • "last_name, first_name"
#   • "pitch_name"
#   • "run_value_per_100"
#   • "woba"
#   • "est_woba"        ← xwOBA
#   • "hard_hit_percent"
required = {
    "last_name, first_name",
    "pitch_name",
    "run_value_per_100",
    "woba",
    "est_woba",
    "hard_hit_percent"
}
if not required.issubset(df_savant.columns):
    missing = required - set(df_savant.columns)
    raise RuntimeError(
        f"Savant CSV is missing required column(s): {missing}. "
        f"Found columns: {list(df_savant.columns)}"
    )

# ——————————————————————————————————————————————————————
# 4) NORMALIZE NAMES & FILTER
# ——————————————————————————————————————————————————————
def normalize_name(comma_name):
    # Input like "Carroll, Corbin" → output "Corbin Carroll"
    if "," in comma_name:
        last, first = comma_name.split(",", 1)
        return first.strip() + " " + last.strip()
    return comma_name.strip()

# Create a “Player” column in the same format as your PrizePicks CSV
df_savant["Player"] = df_savant["last_name, first_name"].map(normalize_name)

# Keep only rows whose “Player” is in hitters_today
df_filtered = df_savant[df_savant["Player"].isin(hitters_today)].copy()

# ——————————————————————————————————————————————————————
# 5) SELECT & RENAME THE COLUMNS YOU NEED
# ——————————————————————————————————————————————————————
df_out = df_filtered[[
    "Player",
    "pitch_name",         # → becomes "Pitch"
    "run_value_per_100",  # → becomes "RV/100"
    "woba",               # → becomes "wOBA"
    "est_woba",           # → becomes "xwOBA"
    "hard_hit_percent"    # → becomes "Hard Hit %"
]].rename(columns={
    "pitch_name":        "Pitch",
    "run_value_per_100": "RV/100",
    "woba":              "wOBA",
    "est_woba":          "xwOBA",
    "hard_hit_percent":  "Hard Hit %",
})

# ——————————————————————————————————————————————————————
# 6) SORT & WRITE OUT THE FINAL CSV
# ——————————————————————————————————————————————————————
# Convert RV/100 to float so we can sort descending
df_out["RV/100_num"] = pd.to_numeric(df_out["RV/100"], errors="coerce")
df_out.sort_values(["Player", "RV/100_num"], ascending=[True, False], inplace=True)
df_out.drop(columns=["RV/100_num"], inplace=True)

df_out.to_csv(OUTPUT_CSV, index=False)
print(f"✅ Done. Wrote {len(df_out)} rows to `{OUTPUT_CSV}`.")
print(df_out.head(10).to_string(index=False))

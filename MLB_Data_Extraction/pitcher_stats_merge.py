import pandas as pd
import os

# ───── CONFIG ─────
DATA_DIR = "../MLB_Prop_Data_CSV"
OUTPUT_FILE = os.path.join(DATA_DIR, "master_pitcher_dataset.csv")

# ───── LOAD DATA ─────
prizepicks         = pd.read_csv(os.path.join(DATA_DIR, "mlb_prizepicks.csv"))
pitcher_stats      = pd.read_csv(os.path.join(DATA_DIR, "mlb_pitcher_stats.csv"))
pitcher_advanced   = pd.read_csv(os.path.join(DATA_DIR, "mlb_pitcher_advanced_stats.csv"))
pitch_usage        = pd.read_csv(os.path.join(DATA_DIR, "mlb_pitcher_pitch_usage.csv"))
hotzones           = pd.read_csv(os.path.join(DATA_DIR, "mlb_pitcher_hotzones.csv"))
last15             = pd.read_csv(os.path.join(DATA_DIR, "mlb_last15_avg.csv"))
last30             = pd.read_csv(os.path.join(DATA_DIR, "mlb_last30_avg.csv"))

# ───── CLEAN NAMES ─────
def normalize_name(name):
    return str(name).strip().lower().replace(".", "")

for df in [prizepicks, pitcher_stats, pitcher_advanced, pitch_usage, hotzones, last15, last30]:
    df["Player"] = df["Player"].apply(normalize_name)

# ───── CLEAN ADVANCED PITCHER STATS ─────
def clean_advanced_pitcher_col(col):
    if col.startswith("K%"): return "K%"
    if col.startswith("BB%"): return "BB%"
    if col.startswith("K-BB%"): return "K-BB%"
    if col.startswith("AVG"): return "AVG Against"
    if col.startswith("WHIP"): return "WHIP"
    if col.startswith("BABIP"): return "BABIP"
    if col.startswith("LOB%"): return "LOB%"
    if col.startswith("ERA-"): return "ERA-"
    if col.startswith("FIP-"): return "FIP-"
    if col.startswith("FIP"): return "FIP"
    return col

pitcher_advanced = pitcher_advanced.rename(columns=clean_advanced_pitcher_col)

# ───── FILTER FOR PITCHERS ─────
pitchers_only = prizepicks[prizepicks["Position"].str.upper() == "P"].copy()

# ───── BASE MERGE ─────
base = pitchers_only.merge(pitcher_stats, on="Player", how="left")
base = base.merge(pitcher_advanced, on="Player", how="left")

# ───── PITCH USAGE ─────
pitch_usage = pitch_usage.drop(columns=["MLB_ID"], errors="ignore")
base = base.merge(pitch_usage, on="Player", how="left")

# ───── HOTZONES ─────
base = base.merge(hotzones, on="Player", how="left")

# ───── LAST 15-DAY AND 30-DAY STATS ─────
def prefix_stat_cols(df, prefix):
    drop_cols = [c for c in df.columns if "MLB_ID" in c]
    df = df.drop(columns=drop_cols, errors="ignore")
    return df.rename(columns={col: f"{prefix}_{col}" for col in df.columns if col != "Player"})

last15 = prefix_stat_cols(last15, "15_day")
last30 = prefix_stat_cols(last30, "30_day")

base = base.merge(last15, on="Player", how="left")
base = base.merge(last30, on="Player", how="left")

# ───── SAVE ─────
base.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Pitcher dataset saved to {OUTPUT_FILE}")

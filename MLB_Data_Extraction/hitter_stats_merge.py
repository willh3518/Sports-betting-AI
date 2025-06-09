import pandas as pd
import os

# ───── CONFIG ─────
DATA_DIR = "../MLB_Prop_Data_CSV"
OUTPUT_FILE = os.path.join(DATA_DIR, "master_hitter_dataset.csv")

# ───── LOAD DATA ─────
prizepicks = pd.read_csv(os.path.join(DATA_DIR, "mlb_prizepicks.csv"))
vs_rhp = pd.read_csv(os.path.join(DATA_DIR, "mlb_vs_rhp_avg.csv"))
vs_lhp = pd.read_csv(os.path.join(DATA_DIR, "mlb_vs_lhp_avg.csv"))
daily_lineups = pd.read_csv(os.path.join(DATA_DIR, "daily_lineups.csv"))
vs_rhp_5 = pd.read_csv(os.path.join(DATA_DIR, "mlb_vs_rhp_last5.csv"))
vs_rhp_10 = pd.read_csv(os.path.join(DATA_DIR, "mlb_vs_rhp_last10.csv"))
vs_rhp_15 = pd.read_csv(os.path.join(DATA_DIR, "mlb_vs_rhp_last15.csv"))
vs_lhp_5 = pd.read_csv(os.path.join(DATA_DIR, "mlb_vs_lhp_last5.csv"))
vs_lhp_10 = pd.read_csv(os.path.join(DATA_DIR, "mlb_vs_lhp_last10.csv"))
vs_lhp_15 = pd.read_csv(os.path.join(DATA_DIR, "mlb_vs_lhp_last15.csv"))
adv_rhp = pd.read_csv(os.path.join(DATA_DIR, "mlb_advanced_vs_rhp.csv"))
adv_lhp = pd.read_csv(os.path.join(DATA_DIR, "mlb_advanced_vs_lhp.csv"))
statcast = pd.read_csv(os.path.join(DATA_DIR, "mlb_hitter_statcast_stats.csv"))
hotzones = pd.read_csv(os.path.join(DATA_DIR, "mlb_hitter_hotzones.csv"))
pitchtype = pd.read_csv(os.path.join(DATA_DIR, "mlb_hitter_vs_pitchtype.csv"))
weather = pd.read_csv(os.path.join(DATA_DIR, "stadium_weather_summary.csv"))
park_factors = pd.read_csv(os.path.join(DATA_DIR, "Park_factors_2024.csv"))

# ───── CLEAN NAMES ─────
def normalize_name(name):
    return str(name).strip().lower().replace(".", "")

for df in [prizepicks, vs_rhp, vs_lhp, daily_lineups, vs_rhp_5, vs_rhp_10, vs_rhp_15,
           vs_lhp_5, vs_lhp_10, vs_lhp_15, adv_rhp, adv_lhp, statcast, hotzones, pitchtype]:
    df["Player"] = df["Player"].apply(normalize_name)

# ───── FILTER OUT PITCHERS ─────
hitters_only = prizepicks[prizepicks["Position"].str.upper() != "P"].copy()

# ───── TEAM NAME MAP ─────
team_abbrev_map = {
    "ATL": "Braves", "ARI": "Diamondbacks", "AZ": "Diamondbacks", "BAL": "Orioles", "BOS": "Red Sox", "CHC": "Cubs",
    "CIN": "Reds", "CLE": "Guardians", "COL": "Rockies", "CWS": "White Sox", "DET": "Tigers",
    "HOU": "Astros", "KC": "Royals", "LAA": "Angels", "LAD": "Dodgers", "MIA": "Marlins",
    "MIL": "Brewers", "MIN": "Twins", "NYM": "Mets", "NYY": "Yankees", "ATH": "Athletics",
    "PHI": "Phillies", "PIT": "Pirates", "SD": "Padres", "SEA": "Mariners", "SF": "Giants",
    "STL": "Cardinals", "TB": "Rays", "TEX": "Rangers", "TOR": "Blue Jays", "WSH": "Nationals", "SDP": "Padres"
}
hitters_only["Full Opposing Team"] = hitters_only["Opposing Team"].map(team_abbrev_map)

# ───── PITCHERS ─────
pitchers = daily_lineups[daily_lineups["Position"].isin(["RHP", "LHP"])].copy()
pitchers = pitchers[["Team", "Player", "Handedness"]].rename(columns={
    "Team": "Full Opposing Team",
    "Player": "Opposing Pitcher",
    "Handedness": "Pitcher Handedness"
})
base = hitters_only.merge(pitchers, on="Full Opposing Team", how="left")

# ───── CLEAN + RENAME STATS ─────
def rename_stat_columns(df, suffix):
    return df.rename(columns={col: f"{col}_{suffix}" for col in df.columns if col != "Player"})

def clean_advanced_labels(df):
    df = df.rename(columns=lambda c: c.split()[0] if c != "Player" else c)
    return df.drop(columns=[c for c in df.columns if "FG_ID" in c], errors="ignore")

vs_rhp   = rename_stat_columns(vs_rhp, "vs_rhp")
vs_rhp_5 = rename_stat_columns(vs_rhp_5, "vs_rhp_5")
vs_rhp_10 = rename_stat_columns(vs_rhp_10, "vs_rhp_10")
vs_rhp_15 = rename_stat_columns(vs_rhp_15, "vs_rhp_15")
vs_lhp   = rename_stat_columns(vs_lhp, "vs_lhp")
vs_lhp_5 = rename_stat_columns(vs_lhp_5, "vs_lhp_5")
vs_lhp_10 = rename_stat_columns(vs_lhp_10, "vs_lhp_10")
vs_lhp_15 = rename_stat_columns(vs_lhp_15, "vs_lhp_15")
adv_rhp = rename_stat_columns(clean_advanced_labels(adv_rhp), "vs_rhp")
adv_lhp = rename_stat_columns(clean_advanced_labels(adv_lhp), "vs_lhp")

for split_df in [vs_rhp, vs_rhp_5, vs_rhp_10, vs_rhp_15, adv_rhp,
                 vs_lhp, vs_lhp_5, vs_lhp_10, vs_lhp_15, adv_lhp]:
    base = base.merge(split_df, on="Player", how="left")

# ───── STATCAST + HOTZONES ─────
def clean_statcast_column(col):
    if "EV" in col: return "EV"
    if "Barrel%" in col: return "Barrel%"
    if "HardHit%" in col: return "Hard Hit %"
    if "xBA" in col: return "xBA"
    if "xwOBA" in col: return "xwOBA"
    return col

statcast = statcast.rename(columns=lambda c: clean_statcast_column(c))
statcast = statcast.drop(columns=[c for c in statcast.columns if "FG_ID" in c], errors="ignore")
base = base.merge(statcast, on="Player", how="left")
base = base.merge(hotzones, on="Player", how="left")

# ───── PITCH TYPE ─────
pitchtype_wide = pitchtype.pivot_table(index="Player", columns="Pitch", values=["RV/100", "wOBA", "xwOBA", "Hard Hit %"])
pitchtype_wide.columns = [f"{pitch.lower().replace('-', '').replace(' ', '_')}_{metric.replace(' ', '').replace('/', '')}"
                          for metric, pitch in pitchtype_wide.columns]
pitchtype_wide.reset_index(inplace=True)
base = base.merge(pitchtype_wide, on="Player", how="left")

# ───── STADIUM WEATHER ─────
# load the home-team weather summary (full names in “Team Name”)
weather = pd.read_csv(os.path.join(DATA_DIR, "stadium_weather_summary.csv"))
weather = weather.rename(columns={"Team Name": "Weather Team Name"})
weather_fields = [
    "Stadium", "Game-Time Temp (°F)", "Game-Time Humidity (%)",
    "Game-Time Wind Speed (mph)", "Game-Time Wind Dir (°)",
    "Game-Time Effect on Hitters"
]
weather = weather[["Weather Team Name"] + weather_fields]

# map PrizePicks codes → full names for both sides
base["Team Name"] = base["Team"].map(team_abbrev_map)
base["Opposing Team Name"] = base["Opposing Team"].map(team_abbrev_map)

# pick the home side’s full name (weather file only has home teams)
home_names = set(weather["Weather Team Name"])
base["Weather Team Name"] = base["Team Name"].where(
    base["Team Name"].isin(home_names),
    base["Opposing Team Name"]
)

# merge on that
base = base.merge(weather, on="Weather Team Name", how="left")

# clean up
base.drop(columns=["Opposing Team Name"], inplace=True)


# create a full team-name column in base so you can merge on it
base["Team Name"] = base["Team"].map(team_abbrev_map)

# ───── PARK FACTORS ─────
# Clean Park Factors team names
park_factors = park_factors.rename(columns={"Team": "Team Name"})

# Only merge on the home team field
park_factors_fields = ["Basic", "1B", "2B", "3B", "HR", "SO", "BB", "GB", "FB", "LD", "IFFB", "FIP"]
park_factors_renamed = park_factors[["Team Name"] + park_factors_fields].rename(
    columns={col: f"Park_Factor_{col}" for col in park_factors_fields}
)

# Merge park factors into main dataset using 'Team Name' as the key (home team)
base = base.merge(park_factors_renamed, on="Team Name", how="left")

# ───── COLUMN ORDER ─────
first_cols = ["Player", "Position", "Team", "Prop Type", "Prop Value", "Opposing Team"]
weather_cols = weather_fields
remaining_cols = [col for col in base.columns if col not in first_cols + weather_cols + ["Weather Team"]]
base = base[first_cols + weather_cols + remaining_cols]

# ───── CLEAN FINAL COLUMN NAMES ─────
def clean_duplicate_labels(col):
    if "_vs_" in col:
        parts = col.split("_vs_")
        stat = parts[0]
        suffix = parts[1]
        if len(stat) > 3 and stat[:len(stat)//2] == stat[len(stat)//2:]:
            stat = stat[:len(stat)//2]
        return f"{stat}_vs_{suffix}"
    return col

base.columns = [clean_duplicate_labels(c) for c in base.columns]
base.drop(columns=["Facing_RHP", "Weather Team"], errors="ignore", inplace=True)

# ───── SAVE ─────
base.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Hitter dataset saved to {OUTPUT_FILE}")

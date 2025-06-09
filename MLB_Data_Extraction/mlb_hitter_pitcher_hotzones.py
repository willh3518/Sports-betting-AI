#!/usr/bin/env python3
import requests
import pandas as pd
from io import StringIO
from mlb_utils import normalize_name  # use your shared normalization

# ─── CONFIG ────────────────────────────────────────────────────────────────────
YEAR               = 2025
RUN_VALUE          = "Neutral"   # "Neutral", "Leveraged", "off", "def"
ENDPOINT           = "https://baseballsavant.mlb.com/visuals/swing-take-data"
PRIZEPICKS_CSV     = "../MLB_Prop_Data_CSV/mlb_prizepicks.csv"
ID_MAPPING_CSV     = "../MLB_Prop_Data_CSV/player_fg_ids.csv"
HITTER_CSV_OUT     = "../MLB_Prop_Data_CSV/mlb_hitter_hotzones.csv"
PITCHER_CSV_OUT    = "../MLB_Prop_Data_CSV/mlb_pitcher_hotzones.csv"

# ─── LOAD & MERGE PLAYERS ─────────────────────────────────────────────────────
df_prize = pd.read_csv(PRIZEPICKS_CSV)
df_prize["Player"] = df_prize["Player"].astype(str).apply(normalize_name)

df_map = pd.read_csv(ID_MAPPING_CSV).rename(columns={"MLB_ID":"player_id"})
df_map["Player"] = df_map["Player"].astype(str).apply(normalize_name)

df_players = (
    pd.merge(df_prize[["Player"]],
             df_map[["Player","player_id","FG_Position"]],
             on="Player", how="left")
      .dropna(subset=["player_id"])
)
df_players["player_id"] = df_players["player_id"].astype(int)
id2name = dict(zip(df_players.player_id, df_players.Player))

# ─── FETCH ONE BIG CSV ────────────────────────────────────────────────────────
resp = requests.get(ENDPOINT, params={
    "year":      YEAR,
    "playerSet": "hitters",
    "runValue":  RUN_VALUE
})
resp.raise_for_status()
df_all = pd.read_csv(StringIO(resp.text))

# filter to 2025 / All grouping / X bat-side / Neutral
df_all = df_all[
    (df_all.year                == YEAR) &
    (df_all.grouping_code       == "All") &
    (df_all.group_bat_side      == "X") &
    (df_all.key_runvalue_method == RUN_VALUE)
]

zones = ("heart","shadow","chase","waste")

# ─── BUILD HITTER HOT-ZONES ─────────────────────────────────────────────────
hitters = []
for pid, sub in df_all[df_all.entity_code=="Batter"].groupby("player_id"):
    if pid not in id2name:
        continue
    row = sub.iloc[0]
    rec = {"Player": id2name[pid]}
    for z in zones:
        rec[f"{z.capitalize()}_Swing"] = int(row[f"n_pitches_swing_{z}"])
        rec[f"{z.capitalize()}_Take" ] = int(row[f"n_pitches_take_{z}"])
        rec[f"{z.capitalize()}_Run"  ] = int(row[f"formatted_n_runvalue_{z}"])
    hitters.append(rec)

pd.DataFrame(hitters).to_csv(HITTER_CSV_OUT, index=False)
print(f"Wrote {len(hitters)} hitters → {HITTER_CSV_OUT}")

# ─── BUILD PITCHER HOT-ZONES ────────────────────────────────────────────────
pitchers = []
for pid, sub in df_all[df_all.entity_code=="Pitcher"].groupby("player_id"):
    if pid not in id2name:
        continue
    row = sub.iloc[0]
    rec = {"Player": id2name[pid]}
    for z in zones:
        rec[f"{z.capitalize()}_Count"] = int(row[f"n_pitches_{z}"])
        pct = row[f"formatted_freq_pitches_{z}"]
        if isinstance(pct, str) and pct.endswith("%"):
            pct = pct.rstrip("%")
        rec[f"{z.capitalize()}_Pct"] = float(pct)
    pitchers.append(rec)

pd.DataFrame(pitchers).to_csv(PITCHER_CSV_OUT, index=False)
print(f"Wrote {len(pitchers)} pitchers → {PITCHER_CSV_OUT}")

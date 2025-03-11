import os
import pandas as pd
import logging, unicodedata

# ✅ Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# ✅ Function to Clean Player Names
def clean_player_name(name):
    """Cleans player names by removing accents, periods, and ensuring proper capitalization.
    Skips combo players that contain a '+' symbol.
    """
    if pd.isna(name):
        return None
    if "+" in name:
        return None  # Skip combo players

    name = name.replace(".", "")
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode("utf-8")
    return name.title()

# 📌 CSV Folder Path
CSV_FOLDER = "../Prop_Data_CSV"
OUTPUT_CSV = os.path.join(CSV_FOLDER, "final_combined_data.csv")  # ✅ Keep the same name

# 📌 Load Data
files = {
    "prizepicks": "prizepicks_data.csv",
    "opponent_def_ratings": "opponent_defensive_ratings.csv",
    "home_away": "home_away_status.csv",
    "season_hit_pct": "season_hit_percentage.csv",  # ✅ Added Season Hit Percentage
    "last_10_hit_pct": "last_10_hit_percentage.csv",  # ✅ Added Last 10 Hit Percentage
    "season_stats": "season_stats.csv",
    "last_5_avg": "last_5_games_avg.csv",
    "last_10_avg": "last_10_games_avg.csv",
    "h2h_current": "h2h_currentseason.csv",  # ✅ H2H Current Season
    "last_10_h2h": "last_10_h2h.csv",  # ✅ Last 10 H2H Matchups
    "season_without_injured": "season_stats_without_injured_players.csv"  # ✅ Added Season Stats Without Injured Players
}

def load_csv(filename):
    """Loads a CSV file into a Pandas DataFrame."""
    path = os.path.join(CSV_FOLDER, filename)
    if os.path.exists(path):
        df = pd.read_csv(path)

        # ✅ Clean Player Names if they exist in this dataframe
        if 'Player' in df.columns:
            df['Player'] = df['Player'].apply(clean_player_name)

        return df

    logging.warning(f"⚠️ File {filename} not found. Skipping...")
    return None

# ✅ Read all CSV files
dataframes = {name: load_csv(fname) for name, fname in files.items()}

# ✅ Ensure PrizePicks Data Exists
if dataframes["prizepicks"] is None:
    logging.error("🚨 Missing prizepicks_data.csv. Exiting...")
    exit()

# Start with PrizePicks Data
final_df = dataframes["prizepicks"].copy()

# ✅ Merge Opponent Defensive Rating
if dataframes["opponent_def_ratings"] is not None:
    final_df = final_df.merge(
        dataframes["opponent_def_ratings"],
        left_on="Opposing Team", right_on="Team",
        how="left"
    )

    # ✅ Rename Defensive Rating Column
    final_df.rename(columns={"Defensive Rating": "Opponent Defensive Rating"}, inplace=True)

    # ✅ Drop duplicate 'Team' if merge created 'Team_x' and 'Team_y'
    if "Team_y" in final_df.columns:
        final_df.drop(columns=["Team_y"], inplace=True)
    if "Team_x" in final_df.columns:
        final_df.rename(columns={"Team_x": "Team"}, inplace=True)

# ✅ Merge Home/Away Status
if dataframes["home_away"] is not None:
    final_df = final_df.merge(
        dataframes["home_away"],
        on=["Player", "Team"],
        how="left"
    )

# ✅ Merge Season Hit Percentage and Last 10 Hit Percentage Per Prop
for key, label in [("season_hit_pct", "Season Hit %"), ("last_10_hit_pct", "Last 10 Hit %")]:
    if dataframes[key] is not None:
        hit_df = dataframes[key].copy()

        # ✅ Standardize column names
        hit_df.rename(columns={"Hit Percentage": label, "Prop": "Full Prop"}, inplace=True)

        # ✅ Convert to lowercase to ensure case-insensitive matching
        hit_df["Full Prop"] = hit_df["Full Prop"].str.lower()
        final_df["Prop Type"] = final_df["Prop Type"].str.lower()

        # ✅ Split "Full Prop" into "Prop Type" and "Prop Value"
        hit_df["Prop Type"] = hit_df["Full Prop"].apply(lambda x: " ".join(x.split()[:-1]).strip())
        hit_df["Prop Value"] = hit_df["Full Prop"].apply(lambda x: x.split()[-1])

        # ✅ Convert "Prop Value" to float for correct merging
        hit_df["Prop Value"] = hit_df["Prop Value"].astype(float)

        # ✅ Ensure consistency before merging
        final_df["Prop Value"] = final_df["Prop Value"].astype(float)  # Ensure float type

        # ✅ Drop the original "Full Prop" column after splitting
        hit_df.drop(columns=["Full Prop"], inplace=True)

        # ✅ Merge on Player, Prop Type, and Prop Value (case-insensitive match)
        final_df = final_df.merge(hit_df, on=["Player", "Prop Type", "Prop Value"], how="left")

# ✅ Merge Season, Last 5, and Last 10 Stats
for key, label in [("season_stats", "Season Stats"), ("last_5_avg", "Last 5 Season"),
                   ("last_10_avg", "Last 10 Season")]:
    if dataframes[key] is not None:
        stats_df = dataframes[key].copy()
        stats_df.columns = [f"{col} ({label})" if col != "Player" else "Player" for col in stats_df.columns]
        final_df = final_df.merge(stats_df, on="Player", how="left")

# ✅ Merge H2H Current Season & Last 10 Matchups
for key, label in [("h2h_current", "H2H Current Season"), ("last_10_h2h", "Last 10 H2H")]:
    if dataframes[key] is not None:
        h2h_df = dataframes[key].copy()

        # ✅ Rename columns to specify they are from H2H data
        h2h_df.columns = [f"{col} ({label})" if col not in ["Player", "Opponent"] else col for col in h2h_df.columns]

        # ✅ Merge using Player and Opponent Team
        final_df = final_df.merge(
            h2h_df,
            on=["Player"],
            how="left"
        ).drop(columns=["Opponent"])  # ✅ Drop duplicate 'Opponent' column

# ✅ Merge Season Stats Without Injured Players
if dataframes["season_without_injured"] is not None:
    injured_df = dataframes["season_without_injured"].copy()

    # ✅ Create a unique index per Player + Team
    injured_df["Injured Index"] = injured_df.groupby(["Player", "Team"]).cumcount() + 1

    # ✅ Rename columns to indicate injured player stats
    injured_df = injured_df.pivot(index=["Player", "Team"], columns="Injured Index")

    # ✅ Flatten MultiIndex columns
    injured_df.columns = [f"{col[0]} (Injured {col[1]})" if col[1] else col[0] for col in injured_df.columns]
    injured_df.reset_index(inplace=True)

    # ✅ Merge into final DataFrame
    final_df = final_df.merge(injured_df, on=["Player", "Team"], how="left")

# ✅ Convert non-numeric columns to string before filling "N/A"
for col in final_df.select_dtypes(include=["float64"]).columns:
    final_df[col] = final_df[col].astype("object")

# ✅ Fill NaN values with "N/A"
final_df = final_df.drop_duplicates(subset=["Player", "Team", "Prop Type", "Prop Value"])
final_df.fillna("N/A", inplace=True)
final_df.to_csv(OUTPUT_CSV, index=False)
logging.info(f"✅ Updated {OUTPUT_CSV}")

import pandas as pd

# 📌 STEP 1: Load the merged dataset
file_path = "../Prop_Data_CSV/final_combined_data.csv"  # Adjust path if needed
data = pd.read_csv(file_path)

# 📌 STEP 2: Drop Unnecessary Columns

# Define columns to drop
drop_columns = [
    'GP (Last 10 H2H)', 'GP (Last 5 Season)', 'GP (Last 10 Season)',  # Unnecessary identifiers
    'Playing without Injured Player (Injured 1)', 'Playing without Injured Player (Injured 2)',
    'Playing without Injured Player (Injured 3)', 'Playing without Injured Player (Injured 4)',
    'Playing without Injured Player (Injured 5)',
    'PTS (Injured 1)', 'PTS (Injured 2)', 'PTS (Injured 3)', 'PTS (Injured 4)', 'PTS (Injured 5)',
    'REB (Injured 1)', 'REB (Injured 2)', 'REB (Injured 3)', 'REB (Injured 4)', 'REB (Injured 5)',
    'AST (Injured 1)', 'AST (Injured 2)', 'AST (Injured 3)', 'AST (Injured 4)', 'AST (Injured 5)',
    'STL (Injured 1)', 'STL (Injured 2)', 'STL (Injured 3)', 'STL (Injured 4)', 'STL (Injured 5)',
    'BLK (Injured 1)', 'BLK (Injured 2)', 'BLK (Injured 3)', 'BLK (Injured 4)', 'BLK (Injured 5)',
    'FGM (Injured 1)', 'FGM (Injured 2)', 'FGM (Injured 3)', 'FGM (Injured 4)', 'FGM (Injured 5)',
    'FGA (Injured 1)', 'FGA (Injured 2)', 'FGA (Injured 3)', 'FGA (Injured 4)', 'FGA (Injured 5)',
    '3PM (Injured 1)', '3PM (Injured 2)', '3PM (Injured 3)', '3PM (Injured 4)', '3PM (Injured 5)',
    '3PA (Injured 1)', '3PA (Injured 2)', '3PA (Injured 3)', '3PA (Injured 4)', '3PA (Injured 5)',
    'FTM (Injured 1)', 'FTM (Injured 2)', 'FTM (Injured 3)', 'FTM (Injured 4)', 'FTM (Injured 5)',
    'FTA (Injured 1)', 'FTA (Injured 2)', 'FTA (Injured 3)', 'FTA (Injured 4)', 'FTA (Injured 5)',
    'OREB (Injured 1)', 'OREB (Injured 2)', 'OREB (Injured 3)', 'OREB (Injured 4)', 'OREB (Injured 5)',
    'DREB (Injured 1)', 'DREB (Injured 2)', 'DREB (Injured 3)', 'DREB (Injured 4)', 'DREB (Injured 5)',
    'TOV (Injured 1)', 'TOV (Injured 2)', 'TOV (Injured 3)', 'TOV (Injured 4)', 'TOV (Injured 5)',
]

# Drop columns
data.drop(columns=drop_columns, inplace=True, errors='ignore')

# 📌 STEP 3: Remove Players with Missing Season Stats

# Define season stat columns (adjust based on actual dataset column names)
season_stat_cols = [
    'GP (Season Stats)', 'PPG (Season Stats)', 'RPG (Season Stats)',
    'APG (Season Stats)', 'SPG (Season Stats)', 'BPG (Season Stats)',
    'FGM (Season Stats)', 'FGA (Season Stats)', '3PM (Season Stats)',
    '3PA (Season Stats)', 'FTM (Season Stats)', 'FTA (Season Stats)',
    'OREB (Season Stats)', 'DREB (Season Stats)', 'TPG (Season Stats)'
]

# Remove rows where any of these season stat columns are missing (NaN)
data = data.dropna(subset=season_stat_cols)

# 📌 STEP 4: Handle Missing Values Without Removing Rows

# Define missing value marker
missing_value_marker = -999  # Model ignores these values

# Handle hit percentage columns
hit_percentage_cols = ['Season Hit %', 'Last 10 Hit Percentage']

for col in hit_percentage_cols:
    # Replace "N/A" with NaN
    data[col] = data[col].replace("N/A%", pd.NA)

    # Remove '%' sign and convert to float
    data[col] = data[col].astype(str).str.replace('%', '', regex=False)

    # Convert to numeric (force errors to NaN)
    data[col] = pd.to_numeric(data[col], errors='coerce')

    # Fill missing values with -999 (using .loc to avoid chained assignment issues)
    data.loc[data[col].isna(), col] = missing_value_marker

# For categorical columns, replace NaN with "Missing" (using .loc)
for col in data.select_dtypes(include=['object']).columns:
    data.loc[data[col].isna(), col] = "Missing"

# For numerical columns, replace NaN with -999 (using .loc)
for col in data.select_dtypes(include=['float64', 'int64']).columns:
    data.loc[data[col].isna(), col] = missing_value_marker

# 📌 STEP 5: Encode Team and Opposing Team Using Fixed Ordinal Encoding

# Define a fixed alphabetical mapping for all 30 NBA teams
nba_teams = [
    "ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW",
    "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK",
    "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
]

# Create a dictionary mapping team names to numerical values
team_mapping = {team: idx for idx, team in enumerate(nba_teams)}

# Apply the mapping to the 'Team' and 'Opposing Team' columns
data["Team"] = data["Team"].map(team_mapping)
data["Opposing Team"] = data["Opposing Team"].map(team_mapping)

# 📌 STEP 6: One-Hot Encode Prop Type While Keeping Column Order
prop_type_index = data.columns.get_loc("Prop Type")  # Find the column index
prop_type_encoded = pd.get_dummies(data["Prop Type"], prefix="Prop Type")  # One-hot encode

data.drop(columns=["Prop Type"], inplace=True)  # Remove original column
for i, col in enumerate(prop_type_encoded.columns):  # Insert new columns in place of original
    data.insert(prop_type_index + i, col, prop_type_encoded[col])

# 📌 STEP 7: Encode Home/Away as Binary (Home=1, Away=0)

# Find the position of the 'Home/Away' column
home_away_index = data.columns.get_loc("Home/Away")

# Convert to binary encoding
data["Home/Away"] = data["Home/Away"].map({"Home": 1, "Away": 0})

# Rename the column for clarity
data.rename(columns={"Home/Away": "Home"}, inplace=True)

# Convert all Prop Type columns from boolean (or string "True"/"False") to 1s and 0s
prop_type_cols = [col for col in data.columns if col.startswith("Prop Type")]
for col in prop_type_cols:
    data[col] = data[col].astype(int)  # Converts True -> 1, False -> 0

# Save cleaned dataset
data.to_csv("../Prop_Data_CSV/processed_data.csv", index=False)
print("✅ Processed dataset saved as 'processed_data.csv'. Open to review.")

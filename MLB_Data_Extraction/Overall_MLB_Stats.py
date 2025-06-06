
import pandas as pd
import re

def normalize_name(name):
    """Normalize player names by lowering case and removing non-alphanumeric characters."""
    if pd.isna(name):
        return ""
    return re.sub(r'[^a-z]', '', name.lower())

# Load datasets
hitter_df = pd.read_csv("../MLB_Prop_Data_CSV/master_hitter_dataset.csv")
pitcher_df = pd.read_csv("../MLB_Prop_Data_CSV/master_pitcher_dataset.csv")

# Normalize pitcher names
hitter_df['Normalized_Opposing_Pitcher'] = hitter_df['Opposing Pitcher'].apply(normalize_name)
pitcher_df['Normalized_Pitcher_Name'] = pitcher_df['Player'].apply(normalize_name)

# Merge on normalized names
merged_df = hitter_df.merge(
    pitcher_df,
    left_on='Normalized_Opposing_Pitcher',
    right_on='Normalized_Pitcher_Name',
    suffixes=('_hitter', '_pitcher')
)

# Drop helper columns
merged_df.drop(columns=['Normalized_Opposing_Pitcher', 'Normalized_Pitcher_Name'], inplace=True)

# Save merged dataset
merged_df.to_csv("../MLB_Prop_Data_CSV/merged_hitter_pitcher_dataset.csv", index=False)

print(f"Merged dataset saved to 'merged_hitter_pitcher_dataset.csv' with shape {merged_df.shape}")

import pandas as pd
import os
import numpy as np
from datetime import datetime

# Config
MLB_DATA_DIR = "../MLB_Prop_Data_CSV"
HITTER_OUTPUT = os.path.join(MLB_DATA_DIR, "hitter_training_data.csv")
PITCHER_OUTPUT = os.path.join(MLB_DATA_DIR, "pitcher_training_data.csv")


def create_training_datasets():
    """
    Creates separate training datasets for hitters and pitchers directly from source files
    """
    print("Starting training data creation process...")

    # Ensure output directory exists
    os.makedirs(os.path.dirname(HITTER_OUTPUT), exist_ok=True)

    # 1. Load master datasets
    print("Loading master datasets...")
    try:
        hitter_master = pd.read_csv(os.path.join(MLB_DATA_DIR, "master_hitter_dataset.csv"))
        pitcher_master = pd.read_csv(os.path.join(MLB_DATA_DIR, "master_pitcher_dataset.csv"))
        print(f"Loaded hitter master data: {hitter_master.shape}")
        print(f"Loaded pitcher master data: {pitcher_master.shape}")
    except FileNotFoundError as e:
        print(f"Error loading master data: {e}")
        return False

    # 2. Load box score results
    print("Loading box score results...")
    try:
        hitter_boxscore = pd.read_csv(os.path.join(MLB_DATA_DIR, "hitter_boxscore_results.csv"))
        pitcher_boxscore = pd.read_csv(os.path.join(MLB_DATA_DIR, "pitcher_boxscore_results.csv"))
        print(f"Loaded hitter boxscore data: {hitter_boxscore.shape}")
        print(f"Loaded pitcher boxscore data: {pitcher_boxscore.shape}")
    except FileNotFoundError as e:
        print(f"Error loading boxscore data: {e}")
        # Continue without boxscore data
        hitter_boxscore = None
        pitcher_boxscore = None

    # 3. Process Hitter Training Data
    print("\nProcessing hitter training data...")
    hitter_training = hitter_master.copy()

    # Add boxscore results if available
    if hitter_boxscore is not None:
        # Select only the relevant columns from boxscore data
        boxscore_cols = ['Player', 'Prop Type', 'Prop Value', 'Start Time',
                         'TB', 'AB', 'IBB', 'XBH', 'H', 'CS', 'BB', 'RBI',
                         'HBP', 'SB', '2B', 'R', 'SH', 'PA', 'SO', '3B',
                         'SF', 'GIDP', 'HR', 'Actual Stat', 'Hit']

        # Filter to only include columns that exist
        existing_cols = [col for col in boxscore_cols if col in hitter_boxscore.columns]
        hitter_boxscore_filtered = hitter_boxscore[existing_cols]

        # Merge with master data
        merge_cols = ['Player', 'Prop Type', 'Prop Value']
        if 'Start Time' in hitter_boxscore_filtered.columns and 'Start Time' in hitter_training.columns:
            merge_cols.append('Start Time')

        print(f"Merging hitter data on columns: {merge_cols}")
        hitter_training = hitter_training.merge(
            hitter_boxscore_filtered,
            on=merge_cols,
            how='left',
            suffixes=('', '_y')
        )

    # 4. Process Pitcher Training Data
    print("\nProcessing pitcher training data...")
    pitcher_training = pitcher_master.copy()

    # Add boxscore results if available
    if pitcher_boxscore is not None:
        # Select only the relevant columns from boxscore data
        boxscore_cols = ['Player', 'Prop Type', 'Prop Value', 'Start Time',
                         'DEC', 'TBF', 'ER', 'IP', 'SHO', 'ERA', 'GF', 'CG',
                         'GS', 'WP', 'SV', 'Pitches Thrown', 'Pitching Outs',
                         'Actual Stat', 'Hit']

        # Filter to only include columns that exist
        existing_cols = [col for col in boxscore_cols if col in pitcher_boxscore.columns]
        pitcher_boxscore_filtered = pitcher_boxscore[existing_cols]

        # Merge with master data
        merge_cols = ['Player', 'Prop Type', 'Prop Value']
        if 'Start Time' in pitcher_boxscore_filtered.columns and 'Start Time' in pitcher_training.columns:
            merge_cols.append('Start Time')

        print(f"Merging pitcher data on columns: {merge_cols}")
        pitcher_training = pitcher_training.merge(
            pitcher_boxscore_filtered,
            on=merge_cols,
            how='left',
            suffixes=('', '_y')
        )

    # 5. Ensure all required columns exist in hitter data
    print("\nEnsuring all required columns exist in hitter data...")

    # Add 'Actual Stat' and 'Hit' columns if they don't exist
    if 'Actual Stat' not in hitter_training.columns:
        hitter_training['Actual Stat'] = np.nan

    if 'Hit' not in hitter_training.columns:
        hitter_training['Hit'] = np.nan

    # 6. Ensure all required columns exist in pitcher data
    print("\nEnsuring all required columns exist in pitcher data...")

    # Add 'Actual Stat' and 'Hit' columns if they don't exist
    if 'Actual Stat' not in pitcher_training.columns:
        pitcher_training['Actual Stat'] = np.nan

    if 'Hit' not in pitcher_training.columns:
        pitcher_training['Hit'] = np.nan

    # 7. Save datasets
    print("\nSaving training datasets...")
    hitter_training.to_csv(HITTER_OUTPUT, index=False)
    pitcher_training.to_csv(PITCHER_OUTPUT, index=False)

    print(f"Hitter training data saved to: {HITTER_OUTPUT}")
    print(f"Pitcher training data saved to: {PITCHER_OUTPUT}")

    return True


if __name__ == "__main__":
    if create_training_datasets():
        print("\nTraining data creation completed successfully!")
    else:
        print("\nTraining data creation failed!")
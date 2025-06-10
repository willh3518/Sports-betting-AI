# Updated mlb_machine_learning.py
import pandas as pd
import numpy as np
import joblib
import os
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import tensorflow as tf
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mlb_ml.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Config
MLB_DATA_DIR = "MLB_Prop_Data_CSV"
MODEL_DIR = "MLB_Models"
RESULTS_DIR = "MLB_Results"
LOG_DIR = "MLB_Logs"

# Ensure directories exist
for directory in [MODEL_DIR, RESULTS_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# File paths
HITTER_TRAINING_PATH = os.path.join(MLB_DATA_DIR, "hitter_training_data.csv")
PITCHER_TRAINING_PATH = os.path.join(MLB_DATA_DIR, "pitcher_training_data.csv")
HITTER_MODEL_PATH = os.path.join(MODEL_DIR, "mlb_hitter_rf_model.pkl")
PITCHER_MODEL_PATH = os.path.join(MODEL_DIR, "mlb_pitcher_rf_model.pkl")
TODAY_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
PREDICTIONS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_predictions.csv")
TOP_PICKS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_top_picks.csv")

def load_data():
    """Load hitter and pitcher data directly from master datasets"""
    logger.info("Loading master datasets for prediction...")

    # File paths for master datasets
    HITTER_MASTER_PATH = os.path.join(MLB_DATA_DIR, "master_hitter_dataset.csv")
    PITCHER_MASTER_PATH = os.path.join(MLB_DATA_DIR, "master_pitcher_dataset.csv")

    # Load hitter data
    try:
        hitter_data = pd.read_csv(HITTER_MASTER_PATH)
        logger.info(f"Loaded hitter master data with shape: {hitter_data.shape}")

        # Add Hit column for predictions (will be NaN)
        if "Hit" not in hitter_data.columns:
            hitter_data["Hit"] = np.nan
            logger.info("Added Hit column to hitter data")
    except FileNotFoundError:
        logger.error(f"Hitter master data not found at {HITTER_MASTER_PATH}")
        hitter_data = None

    # Load pitcher data
    try:
        pitcher_data = pd.read_csv(PITCHER_MASTER_PATH)
        logger.info(f"Loaded pitcher master data with shape: {pitcher_data.shape}")

        # Add Hit column for predictions (will be NaN)
        if "Hit" not in pitcher_data.columns:
            pitcher_data["Hit"] = np.nan
            logger.info("Added Hit column to pitcher data")
    except FileNotFoundError:
        logger.error(f"Pitcher master data not found at {PITCHER_MASTER_PATH}")
        pitcher_data = None

    # If we have historical training data, load and combine it
    HITTER_TRAINING_PATH = os.path.join(MLB_DATA_DIR, "hitter_training_data.csv")
    PITCHER_TRAINING_PATH = os.path.join(MLB_DATA_DIR, "pitcher_training_data.csv")

    try:
        hitter_training = pd.read_csv(HITTER_TRAINING_PATH)
        logger.info(f"Loaded hitter training data with shape: {hitter_training.shape}")

        # Combine with master data if available
        if hitter_data is not None:
            # Keep track of which rows are for prediction
            hitter_data["is_prediction"] = True

            # Ensure training data has the same column
            hitter_training["is_prediction"] = False

            # Combine datasets
            hitter_data = pd.concat([hitter_training, hitter_data], ignore_index=True)
            logger.info(f"Combined hitter data shape: {hitter_data.shape}")
    except FileNotFoundError:
        logger.info(f"No hitter training data found at {HITTER_TRAINING_PATH}")
        if hitter_data is not None:
            hitter_data["is_prediction"] = True

    try:
        pitcher_training = pd.read_csv(PITCHER_TRAINING_PATH)
        logger.info(f"Loaded pitcher training data with shape: {pitcher_training.shape}")

        # Combine with master data if available
        if pitcher_data is not None:
            # Keep track of which rows are for prediction
            pitcher_data["is_prediction"] = True

            # Ensure training data has the same column
            pitcher_training["is_prediction"] = False

            # Combine datasets
            pitcher_data = pd.concat([pitcher_training, pitcher_data], ignore_index=True)
            logger.info(f"Combined pitcher data shape: {pitcher_data.shape}")
    except FileNotFoundError:
        logger.info(f"No pitcher training data found at {PITCHER_TRAINING_PATH}")
        if pitcher_data is not None:
            pitcher_data["is_prediction"] = True

    return hitter_data, pitcher_data

def preprocess_data(data, prop_type):
    """Preprocess data for model training"""
    logger.info(f"Preprocessing {prop_type} data...")

    if data is None:
        return None, None, None, None

    # Create a copy to avoid SettingWithCopyWarning
    data = data.copy()

    # Filter by prop type
    if prop_type == "hitter":
        hitter_props = [
            "Hits", "Runs", "RBIs", "Walks", "Hitter Strikeouts", "Total Bases",
            "Hits+Runs+RBIs", "Hits+Runs", "Runs+RBIs", "Hitter Fantasy Score"
        ]
        data = data[data["Prop Type"].isin(hitter_props)]
    else:  # pitcher
        pitcher_props = [
            "Pitcher Strikeouts", "Earned Runs Allowed", "Pitches Thrown",
            "Pitching Outs", "Pitcher Fantasy Score"
        ]
        data = data[data["Prop Type"].isin(pitcher_props)]

    # Setup Hit column if missing
    if "Hit" not in data.columns:
        logger.warning("'Hit' column missing. Assuming this is a prediction day.")
        data["Hit"] = np.nan

    # Convert Hit column to numeric if it's not already
    if data["Hit"].dtype == 'object':
        data.loc[:, "Hit"] = pd.to_numeric(data["Hit"], errors='coerce')

    # Feature engineering
    data = feature_engineering(data, prop_type)

    # Select features based on prop type
    if prop_type == "hitter":
        features = select_hitter_features(data)
    else:
        features = select_pitcher_features(data)

    # Handle missing values
    features = features.fillna(-999).infer_objects(copy=False)

    # Split data for training and prediction
    X = features
    y = data["Hit"]

    X_train = X[~y.isna()]
    y_train = y[~y.isna()]
    X_pred = X[y.isna()]

    # Get player info for predictions
    players_pred = data.loc[
        y.isna(), ["Player", "Prop Type", "Prop Value", "Start Time"]] if not y.isna().all() else pd.DataFrame()

    return X_train, y_train, X_pred, players_pred

def feature_engineering(data, prop_type):
    """Perform feature engineering based on prop type"""
    logger.info(f"Performing feature engineering for {prop_type} data...")

    if data is None or len(data) == 0:
        return data

    # Create a copy to avoid SettingWithCopyWarning
    data = data.copy()

    # Store new columns in dictionaries to add all at once (avoids fragmentation)
    new_columns = {}

    # Common feature engineering
    # Convert categorical variables to numeric
    if "Pitcher Handedness" in data.columns:
        new_columns["Pitcher_Handedness_Numeric"] = data["Pitcher Handedness"].map({"right": 0, "left": 1})

    if "Game-Time Effect on Hitters" in data.columns:
        effect_map = {
            "Tailwind: fly balls likely to carry → helps hitters.": 1,
            "Headwind: fly balls suppressed → hurts hitters.": -1,
            "Crosswind: minimal effect on hitters.": 0,
            "No wind: no effect on hitters.": 0
        }
        new_columns["Wind_Effect_Numeric"] = data["Game-Time Effect on Hitters"].map(effect_map).fillna(0)

    # Convert numeric columns that might be strings to float
    numeric_columns = [
        # Common metrics
        "Prop Value", "Game-Time Temp (°F)", "Game-Time Humidity (%)",
        "Game-Time Wind Speed (mph)", "Park_Factor_Basic", "Park_Factor_HR",

        # Hitter metrics
        "AVG_vs_rhp", "OBP_vs_rhp", "SLG_vs_rhp", "OPS_vs_rhp",
        "AVG_vs_lhp", "OBP_vs_lhp", "SLG_vs_lhp", "OPS_vs_lhp",
        "AVG_vs_rhp_15", "OPS_vs_rhp_15", "AVG_vs_lhp_15", "OPS_vs_lhp_15",
        "wOBA", "xwOBA", "Barrel%", "Hard Hit %", "EV", "wOBA_vs_rhp", "wOBA_vs_lhp",

        # Pitcher metrics
        "ERA", "WHIP", "K/9", "BB/9", "K/BB", "HR/9", "H/9",
        "K%", "BB%", "K-BB%", "AVG Against", "BABIP", "LOB%", "FIP",
        "15_day_fastball_velo", "15_day_hard_hit_pct", "15_day_barrel_pct",
        "30_day_fastball_velo", "30_day_hard_hit_pct", "30_day_barrel_pct"
    ]

    # Convert all potential numeric columns to float
    for col in data.columns:
        if col in numeric_columns or any(substr in col for substr in ["_vs_", "Factor", "wOBA", "xwOBA", "%"]):
            try:
                # Try to convert to numeric, coercing errors to NaN
                data.loc[:, col] = pd.to_numeric(data[col], errors='coerce')
            except Exception as e:
                logger.warning(f"Could not convert column {col} to numeric: {e}")

    # Hitter-specific feature engineering
    if prop_type == "hitter":
        # Create handedness advantage score
        if all(col in data.columns for col in ["Pitcher Handedness", "wOBA_vs_rhp", "wOBA_vs_lhp"]):
            # Make sure these are numeric
            data.loc[:, "wOBA_vs_rhp"] = pd.to_numeric(data["wOBA_vs_rhp"], errors='coerce')
            data.loc[:, "wOBA_vs_lhp"] = pd.to_numeric(data["wOBA_vs_lhp"], errors='coerce')

            new_columns["wOBA_split"] = np.where(
                data["Pitcher Handedness"].str.lower() == "right",
                data["wOBA_vs_rhp"],
                data["wOBA_vs_lhp"]
            )

            # Normalize metrics for comparison
            for col in ["wOBA_split", "xwOBA", "EV", "Barrel%"]:
                col_data = None

                # Get the column data (either from original data or new columns)
                if col in new_columns:
                    col_data = new_columns[col]
                elif col in data.columns:
                    col_data = data[col]

                if col_data is not None:
                    try:
                        # Only proceed if we have valid numeric data
                        if not pd.isna(col_data).all():
                            min_val = col_data.min()
                            max_val = col_data.max()
                            if max_val > min_val:
                                new_columns[f"{col}_norm"] = (col_data - min_val) / (max_val - min_val)
                    except Exception as e:
                        logger.warning(f"Error normalizing {col}: {e}")
                        new_columns[f"{col}_norm"] = np.nan

    # Pitcher-specific feature engineering
    if prop_type == "pitcher":
        # Create normalized metrics
        for col in ["ERA", "WHIP", "K/9", "BB/9", "HR/9"]:
            if col in data.columns:
                try:
                    # Only proceed if we have valid numeric data
                    if not pd.isna(data[col]).all():
                        min_val = data[col].min()
                        max_val = data[col].max()
                        if max_val > min_val:
                            # For ERA, WHIP, BB/9, HR/9 - lower is better
                            if col in ["ERA", "WHIP", "BB/9", "HR/9"]:
                                new_columns[f"{col}_norm"] = 1 - ((data[col] - min_val) / (max_val - min_val))
                            # For K/9 - higher is better
                            else:
                                new_columns[f"{col}_norm"] = (data[col] - min_val) / (max_val - min_val)
                except Exception as e:
                    logger.warning(f"Error normalizing {col}: {e}")
                    new_columns[f"{col}_norm"] = np.nan

    # Add all new columns at once to avoid fragmentation
    if new_columns:
        new_df = pd.DataFrame(new_columns, index=data.index)
        data = pd.concat([data, new_df], axis=1)

    return data

def select_hitter_features(data):
    """Select features for hitter model"""
    # Define core features for hitters
    core_features = [
        # Basic info
        "Prop Value",

        # Batter stats vs pitcher handedness
        "AVG_vs_rhp", "OBP_vs_rhp", "SLG_vs_rhp", "OPS_vs_rhp",
        "AVG_vs_lhp", "OBP_vs_lhp", "SLG_vs_lhp", "OPS_vs_lhp",

        # Recent performance
        "AVG_vs_rhp_15", "OPS_vs_rhp_15",
        "AVG_vs_lhp_15", "OPS_vs_lhp_15",

        # Advanced metrics
        "wOBA", "xwOBA", "Barrel%", "Hard Hit %", "EV",

        # Normalized metrics
        "wOBA_split_norm", "xwOBA_norm", "EV_norm", "Barrel%_norm",

        # Pitcher handedness
        "Pitcher_Handedness_Numeric",

        # Game conditions
        "Game-Time Temp (°F)", "Game-Time Humidity (%)",
        "Game-Time Wind Speed (mph)", "Wind_Effect_Numeric",

        # Park factors
        "Park_Factor_Basic", "Park_Factor_HR"
    ]

    # Filter to only include columns that exist in the data
    available_features = [f for f in core_features if f in data.columns]

    # Create a new DataFrame with only the selected features
    selected_data = data[available_features].copy()

    # Ensure all columns are numeric
    for col in selected_data.columns:
        selected_data.loc[:, col] = pd.to_numeric(selected_data[col], errors='coerce')

    # One-hot encode prop types
    if "Prop Type" in data.columns:
        prop_dummies = pd.get_dummies(data["Prop Type"], prefix="prop")
        features = pd.concat([selected_data, prop_dummies], axis=1)
    else:
        features = selected_data

    return features

def select_pitcher_features(data):
    """Select features for pitcher model"""
    # Define core features for pitchers
    core_features = [
        # Basic info
        "Prop Value",

        # Pitcher stats
        "ERA", "WHIP", "K/9", "BB/9", "K/BB", "HR/9", "H/9",
        "K%", "BB%", "K-BB%", "AVG Against", "BABIP", "LOB%", "FIP",

        # Normalized metrics
        "ERA_norm", "WHIP_norm", "K/9_norm", "BB/9_norm", "HR/9_norm",

        # Recent performance
        "15_day_fastball_velo", "15_day_hard_hit_pct", "15_day_barrel_pct",
        "30_day_fastball_velo", "30_day_hard_hit_pct", "30_day_barrel_pct",

        # Game conditions
        "Game-Time Temp (°F)", "Game-Time Humidity (%)",
        "Game-Time Wind Speed (mph)", "Wind_Effect_Numeric"
    ]

    # Filter to only include columns that exist in the data
    available_features = [f for f in core_features if f in data.columns]

    # Create a new DataFrame with only the selected features
    selected_data = data[available_features].copy()

    # Ensure all columns are numeric
    for col in selected_data.columns:
        selected_data.loc[:, col] = pd.to_numeric(selected_data[col], errors='coerce')

    # One-hot encode prop types
    if "Prop Type" in data.columns:
        prop_dummies = pd.get_dummies(data["Prop Type"], prefix="prop")
        features = pd.concat([selected_data, prop_dummies], axis=1)
    else:
        features = selected_data

    return features

def train_model(X_train, y_train, model_path):
    """Train and save Random Forest model"""
    if X_train is None or y_train is None or len(X_train) == 0:
        logger.warning("No training data available. Skipping model training.")
        return None

    logger.info(f"Training model on {len(X_train)} samples")

    # Split data for validation
    X_train_split, X_test_split, y_train_split, y_test_split = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42
    )

    # Train model
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        bootstrap=True,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train_split, y_train_split)

    # Evaluate model
    y_pred_test = model.predict(X_test_split)
    acc = accuracy_score(y_test_split, y_pred_test)

    logger.info(f"Model accuracy: {acc:.2f}")
    logger.info(f"Classification Report:\n{classification_report(y_test_split, y_pred_test)}")
    logger.info(f"Confusion Matrix:\n{confusion_matrix(y_test_split, y_pred_test)}")

    # Save model
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")

    # Log metrics with TensorBoard
    writer = tf.summary.create_file_writer(LOG_DIR)
    with writer.as_default():
        tf.summary.scalar("Accuracy", acc, step=0)

    return model

def make_predictions(X_pred, players_pred, model_path, prop_type):
    """Make predictions using trained model"""
    if X_pred is None or len(X_pred) == 0 or players_pred is None or len(players_pred) == 0:
        logger.warning(f"No prediction data available for {prop_type}. Skipping predictions.")
        return pd.DataFrame()

    # Check if model exists
    if not os.path.exists(model_path):
        logger.error(f"Model not found at {model_path}. Train it first.")
        return pd.DataFrame()

    logger.info(f"Making predictions for {len(X_pred)} {prop_type} props")

    # Load model
    model = joblib.load(model_path)

    # Ensure X_pred has all required columns
    missing_cols = set(model.feature_names_in_) - set(X_pred.columns)
    if missing_cols:
        logger.warning(f"Missing columns in prediction data: {missing_cols}")
        for col in missing_cols:
            X_pred.loc[:, col] = -999

    # Check for extra columns in X_pred
    extra_cols = set(X_pred.columns) - set(model.feature_names_in_)
    if extra_cols:
        logger.warning(f"Extra columns in prediction data: {extra_cols}")

    # Reorder columns to match model's expected order
    try:
        X_pred = X_pred[model.feature_names_in_]
    except KeyError as e:
        logger.error(f"KeyError when reordering columns: {e}")
        logger.info(f"X_pred columns: {X_pred.columns.tolist()}")
        logger.info(f"Model feature names: {model.feature_names_in_.tolist()}")
        return pd.DataFrame()

    # Make predictions
    try:
        preds = model.predict(X_pred)
        probs = model.predict_proba(X_pred)[:, 1]
    except Exception as e:
        logger.error(f"Error making predictions: {e}")
        return pd.DataFrame()

    # Create predictions DataFrame
    predictions_df = players_pred.copy()
    predictions_df["RF_Prediction"] = preds
    predictions_df["RF_Confidence"] = probs
    predictions_df["Model_Type"] = prop_type
    predictions_df["LLM_Prediction"] = None
    predictions_df["LLM_Justification"] = None
    predictions_df["Actual_Result"] = None
    predictions_df["Reflection"] = None

    return predictions_df

def main():
    """Main function to run the MLB machine learning pipeline"""
    logger.info("Starting MLB machine learning pipeline")

    # Load data
    hitter_data, pitcher_data = load_data()

    # Process hitter data
    hitter_X_train, hitter_y_train, hitter_X_pred, hitter_players_pred = preprocess_data(hitter_data, "hitter")

    # Process pitcher data
    pitcher_X_train, pitcher_y_train, pitcher_X_pred, pitcher_players_pred = preprocess_data(pitcher_data, "pitcher")

    # Train hitter model
    hitter_model = train_model(hitter_X_train, hitter_y_train, HITTER_MODEL_PATH)

    # Train pitcher model
    pitcher_model = train_model(pitcher_X_train, pitcher_y_train, PITCHER_MODEL_PATH)

    # Make hitter predictions
    hitter_predictions = make_predictions(hitter_X_pred, hitter_players_pred, HITTER_MODEL_PATH, "hitter")

    # Make pitcher predictions
    pitcher_predictions = make_predictions(pitcher_X_pred, pitcher_players_pred, PITCHER_MODEL_PATH, "pitcher")

    # Combine predictions
    all_predictions = pd.concat([hitter_predictions, pitcher_predictions], ignore_index=True)

    # Save predictions if we have any
    if not all_predictions.empty:
        all_predictions.to_csv(PREDICTIONS_PATH, index=False)
        logger.info(f"All predictions saved to {PREDICTIONS_PATH}")

        # Generate top picks
        top_picks = all_predictions.sort_values("RF_Confidence", ascending=False).head(10)
        top_picks.to_csv(TOP_PICKS_PATH, index=False)
        logger.info(f"Top picks saved to {TOP_PICKS_PATH}")

        # Log prediction metrics
        writer = tf.summary.create_file_writer(LOG_DIR)
        with writer.as_default():
            tf.summary.scalar("Predictions Made", len(all_predictions), step=0)
    else:
        logger.warning("No predictions were generated.")

    logger.info("MLB machine learning pipeline completed")

    return all_predictions

if __name__ == "__main__":
    main()
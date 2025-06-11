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
import argparse

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
TRAINING_DIR = os.path.join(MLB_DATA_DIR, "MLB_Training_Data")

# Ensure directories exist
for directory in [MODEL_DIR, RESULTS_DIR, LOG_DIR, TRAINING_DIR]:
    os.makedirs(directory, exist_ok=True)

# File paths
HITTER_TRAINING_PATH = os.path.join(TRAINING_DIR, "hitter_training_data.csv")
PITCHER_TRAINING_PATH = os.path.join(TRAINING_DIR, "pitcher_training_data.csv")
HITTER_MODEL_PATH = os.path.join(MODEL_DIR, "mlb_hitter_rf_model.pkl")
PITCHER_MODEL_PATH = os.path.join(MODEL_DIR, "mlb_pitcher_rf_model.pkl")
TODAY_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
PREDICTIONS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_predictions.csv")
TOP_PICKS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_top_picks.csv")


def load_prediction_data():
    """Load only master datasets for prediction"""
    logger.info("Loading master datasets for prediction...")

    # File paths
    HITTER_MASTER_PATH = os.path.join(MLB_DATA_DIR, "master_hitter_dataset.csv")
    PITCHER_MASTER_PATH = os.path.join(MLB_DATA_DIR, "master_pitcher_dataset.csv")

    try:
        hitter_data = pd.read_csv(HITTER_MASTER_PATH)
        logger.info(f"Loaded hitter master data with shape: {hitter_data.shape}")
    except FileNotFoundError:
        logger.error(f"Hitter master data not found at {HITTER_MASTER_PATH}")
        return None, None

    try:
        pitcher_data = pd.read_csv(PITCHER_MASTER_PATH)
        logger.info(f"Loaded pitcher master data with shape: {pitcher_data.shape}")
    except FileNotFoundError:
        logger.error(f"Pitcher master data not found at {PITCHER_MASTER_PATH}")
        return None, None

    return hitter_data, pitcher_data

def load_training_data():
    """Load and combine all training data files from MLB_Training_Data directory"""
    logger.info("Loading training datasets...")

    # Define training data directory
    TRAINING_DATA_DIR = os.path.join(MLB_DATA_DIR, "MLB_Training_Data")

    if not os.path.exists(TRAINING_DATA_DIR):
        logger.error(f"Training data directory not found at {TRAINING_DATA_DIR}")
        return None, None

    # Get all training files
    training_files = [f for f in os.listdir(TRAINING_DATA_DIR) if f.endswith('.csv')]

    # Initialize empty DataFrames
    hitter_data = pd.DataFrame()
    pitcher_data = pd.DataFrame()

    # Process hitter files
    hitter_files = [f for f in training_files if 'hitter' in f.lower()]
    for file in hitter_files:
        try:
            file_path = os.path.join(TRAINING_DATA_DIR, file)
            file_data = pd.read_csv(file_path)
            hitter_data = pd.concat([hitter_data, file_data], ignore_index=True)
            logger.info(f"Added hitter data from {file}. Current shape: {hitter_data.shape}")
        except Exception as e:
            logger.warning(f"Error loading hitter file {file}: {str(e)}")

    # Process pitcher files
    pitcher_files = [f for f in training_files if 'pitcher' in f.lower()]
    for file in pitcher_files:
        try:
            file_path = os.path.join(TRAINING_DATA_DIR, file)
            file_data = pd.read_csv(file_path)
            pitcher_data = pd.concat([pitcher_data, file_data], ignore_index=True)
            logger.info(f"Added pitcher data from {file}. Current shape: {pitcher_data.shape}")
        except Exception as e:
            logger.warning(f"Error loading pitcher file {file}: {str(e)}")

    # Remove duplicates
    if not hitter_data.empty:
        initial_shape = hitter_data.shape[0]
        hitter_data = hitter_data.drop_duplicates()
        if hitter_data.shape[0] < initial_shape:
            logger.info(f"Removed {initial_shape - hitter_data.shape[0]} duplicate hitter rows")

    if not pitcher_data.empty:
        initial_shape = pitcher_data.shape[0]
        pitcher_data = pitcher_data.drop_duplicates()
        if pitcher_data.shape[0] < initial_shape:
            logger.info(f"Removed {initial_shape - pitcher_data.shape[0]} duplicate pitcher rows")

    return hitter_data, pitcher_data

def update_training_data():
    """Update training data with new results"""
    logger.info("Updating training data with new results...")

    # Get yesterday's date
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # Check for results files from yesterday
    results_file = os.path.join(RESULTS_DIR, f"{yesterday}_mlb_results.csv")

    if not os.path.exists(results_file):
        logger.warning(f"No results file found for yesterday at {results_file}")
        return False

    try:
        # Load results
        results = pd.read_csv(results_file)
        logger.info(f"Loaded {len(results)} results from {results_file}")

        # Split into hitter and pitcher results
        hitter_results = results[results["Model_Type"] == "hitter"].copy()
        pitcher_results = results[results["Model_Type"] == "pitcher"].copy()

        # Update training data
        if len(hitter_results) > 0:
            try:
                existing_hitter = pd.read_csv(HITTER_TRAINING_PATH)
                updated_hitter = pd.concat([existing_hitter, hitter_results], ignore_index=True)
                updated_hitter.to_csv(HITTER_TRAINING_PATH, index=False)
                logger.info(f"Updated hitter training data with {len(hitter_results)} new records")
            except FileNotFoundError:
                hitter_results.to_csv(HITTER_TRAINING_PATH, index=False)
                logger.info(f"Created new hitter training data with {len(hitter_results)} records")

        if len(pitcher_results) > 0:
            try:
                existing_pitcher = pd.read_csv(PITCHER_TRAINING_PATH)
                updated_pitcher = pd.concat([existing_pitcher, pitcher_results], ignore_index=True)
                updated_pitcher.to_csv(PITCHER_TRAINING_PATH, index=False)
                logger.info(f"Updated pitcher training data with {len(pitcher_results)} new records")
            except FileNotFoundError:
                pitcher_results.to_csv(PITCHER_TRAINING_PATH, index=False)
                logger.info(f"Created new pitcher training data with {len(pitcher_results)} records")

        return True

    except Exception as e:
        logger.error(f"Error updating training data: {str(e)}")
        return False

def preprocess_data(data, prop_type, is_training=False):
    """Preprocess data for model training and prediction"""
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

    # Feature engineering
    data = feature_engineering(data, prop_type)

    # Select features based on prop type
    if prop_type == "hitter":
        features = select_hitter_features(data)
    else:
        features = select_pitcher_features(data)

    # Handle missing values and suppress FutureWarning
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter(action='ignore', category=FutureWarning)
        features = features.fillna(-999)
        features = features.infer_objects(copy=False)

    # All data will be used for prediction
    X_pred = features
    players_pred = data[["Player", "Prop Type", "Prop Value", "Start Time"]]

    return None, None, X_pred, players_pred

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
            "Tailwind: fly balls likely to carry  helps hitters.": 1,
            "Headwind: fly balls suppressed  hurts hitters.": -1,
            "Crosswind: minimal effect on hitters.": 0,
            "No wind: no effect on hitters.": 0
        }
        new_columns["Wind_Effect_Numeric"] = data["Game-Time Effect on Hitters"].map(effect_map).fillna(0)

    # First, convert percentage strings to numeric values
    for col in data.columns:
        if isinstance(data[col].dtype, object):  # Check if column is object type (string)
            # Check if this column contains percentage values
            if data[col].astype(str).str.contains('%').any():
                try:
                    # Convert percentage strings to float (remove % and divide by 100)
                    data.loc[:, col] = data[col].astype(str).str.rstrip('%').astype(float) / 100
                    logger.info(f"Converted percentage column {col} to float")
                except Exception as e:
                    logger.warning(f"Could not convert percentage column {col} to numeric: {e}")

    # Convert numeric columns that might be strings to float
    numeric_columns = [
        # Common metrics
        "Prop Value", "Game-Time Temp (F)", "Game-Time Humidity (%)",
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
        if col in numeric_columns or any(substr in col for substr in ["_vs_", "Factor", "wOBA", "xwOBA"]):
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
            metrics_to_normalize = ["wOBA_split", "xwOBA", "EV"]
            for col in metrics_to_normalize:
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
        # Always create these normalized metrics for pitchers, even if they're empty
        pitcher_metrics_to_normalize = ["ERA", "WHIP", "K/9", "BB/9", "HR/9"]

        for col in pitcher_metrics_to_normalize:
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

            # If the column doesn't exist or normalization failed, add a placeholder with default values
            if f"{col}_norm" not in new_columns:
                logger.warning(f"Adding placeholder for missing normalized column: {col}_norm")
                new_columns[f"{col}_norm"] = 0.5  # Use a neutral value as placeholder

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
    from sklearn.model_selection import GridSearchCV
    from sklearn.preprocessing import StandardScaler

    if X_train is None or y_train is None or len(X_train) == 0:
        logger.warning("No training data available. Skipping model training.")
        return None

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)

    # Define parameter grid
    param_grid = {
        'n_estimators': [100, 200, 300],
        'max_depth': [10, 20, 30],
        'min_samples_split': [5, 10],
        'min_samples_leaf': [2, 4],
        'max_features': ['sqrt', 'log2'],
        'class_weight': ['balanced', 'balanced_subsample']
    }

    # Initialize base model
    base_model = RandomForestClassifier(random_state=42, n_jobs=-1)

    # Perform grid search with cross-validation
    grid_search = GridSearchCV(
        estimator=base_model,
        param_grid=param_grid,
        cv=5,
        scoring='f1',
        n_jobs=-1,
        verbose=1
    )

    grid_search.fit(X_train_scaled, y_train)

    # Get best model
    best_model = grid_search.best_estimator_

    # Save model and scaler
    joblib.dump({'model': best_model, 'scaler': scaler}, model_path)

    # Log results
    logger.info(f"Best parameters: {grid_search.best_params_}")
    logger.info(f"Best cross-validation score: {grid_search.best_score_:.3f}")

    return best_model

def make_predictions(X_pred, players_pred, model_path, prop_type):
    """Make predictions using trained model"""
    if X_pred is None or len(X_pred) == 0:
        logger.warning(f"No prediction data available for {prop_type}")
        return pd.DataFrame()

    try:
        # Load model
        model_data = joblib.load(model_path)

        # Check if model is wrapped in a dict (new format) or direct model (old format)
        if isinstance(model_data, dict) and 'model' in model_data:
            model = model_data['model']
            scaler = model_data.get('scaler')

            # Apply scaling if scaler exists
            if scaler is not None:
                X_pred_scaled = scaler.transform(X_pred)
            else:
                X_pred_scaled = X_pred
        else:
            # Legacy format - direct model
            model = model_data
            X_pred_scaled = X_pred

        # Make predictions
        preds = model.predict(X_pred_scaled)
        probs = model.predict_proba(X_pred_scaled)[:, 1]  # Probability of class 1

        # Create predictions DataFrame
        predictions_df = players_pred.copy()
        predictions_df["RF_Prediction"] = preds
        predictions_df["RF_Confidence"] = probs
        predictions_df["Model_Type"] = prop_type

        # Add placeholder columns for LLM predictions and actual results
        predictions_df["LLM_Prediction"] = None
        predictions_df["LLM_RF_Agreement"] = None
        predictions_df["LLM_Confidence"] = None
        predictions_df["LLM_Justification"] = None
        predictions_df["Actual_Stat"] = None
        predictions_df["Actual_Result"] = None
        predictions_df["Reflection"] = None

        return predictions_df

    except Exception as e:
        logger.error(f"Error making predictions: {str(e)}")
        return pd.DataFrame()

def weekly_training():
    """Perform weekly model training using all accumulated training data"""
    logger.info("Starting weekly model training")

    # Load all training data from dated files
    hitter_training, pitcher_training = load_training_data()

    def prepare_training_data(data, model_type):
        """Helper function to prepare training data"""
        if 'Hit' not in data.columns:
            logger.error(f"No 'Hit' column found in {model_type} training data")
            return None, None

        # Remove rows with NaN in the target column
        initial_rows = len(data)
        data = data.dropna(subset=['Hit'])
        if len(data) < initial_rows:
            logger.info(f"Removed {initial_rows - len(data)} rows with NaN in 'Hit' column from {model_type} data")

        # Columns that should always be excluded
        exclude_columns = [
            'Player', 'Team', 'Opponent', 'Start Time', 'Game Date',
            'Stadium', 'Weather Condition', 'Model_Type', 'LLM_Justification',
            'Reflection', 'Date', 'Full Opposing Team', 'Opposing Pitcher'
        ]

        # Get target variable
        y_train = data['Hit'].astype(int)
        X_train = data.drop(columns=['Hit'])

        # Process each column
        for col in list(X_train.columns):
            if col in exclude_columns:
                X_train = X_train.drop(columns=[col])
                logger.info(f"Dropped identifier column: {col}")
                continue

            # Convert percentage strings to float
            if isinstance(X_train[col].dtype, object):
                try:
                    if X_train[col].astype(str).str.contains('%').any():
                        X_train[col] = X_train[col].astype(str).str.rstrip('%').astype(float) / 100
                        logger.info(f"Converted percentage column: {col}")
                    else:
                        # Try to convert to numeric
                        X_train[col] = pd.to_numeric(X_train[col], errors='coerce')
                except Exception as e:
                    logger.info(f"Dropped non-numeric column: {col} - {str(e)}")
                    X_train = X_train.drop(columns=[col])

        # Handle categorical columns that should be encoded
        categorical_columns = ['Prop Type', 'Pitcher Handedness', 'Game-Time Effect on Hitters', 'Odds Category']
        for col in categorical_columns:
            if col in X_train.columns:
                # Create dummy variables
                dummies = pd.get_dummies(X_train[col], prefix=col)
                X_train = pd.concat([X_train, dummies], axis=1)
                X_train = X_train.drop(columns=[col])
                logger.info(f"Encoded categorical column: {col} into {len(dummies.columns)} features")

        # Fill remaining NaN values
        X_train = X_train.fillna(-999)

        logger.info(f"Final {model_type} training data shape: {X_train.shape}")
        return X_train, y_train

    # Process hitter data
    if hitter_training is not None and len(hitter_training) > 0:
        logger.info(f"Training hitter model with {len(hitter_training)} samples from {len([f for f in os.listdir(os.path.join(MLB_DATA_DIR, 'MLB_Training_Data')) if 'hitter' in f.lower() and f.endswith('.csv')])} files")
        X_train, y_train = prepare_training_data(hitter_training, "hitter")
        if X_train is not None:
            train_model(X_train, y_train, HITTER_MODEL_PATH)
    else:
        logger.warning("No hitter training data available for weekly training")

    # Process pitcher data
    if pitcher_training is not None and len(pitcher_training) > 0:
        logger.info(f"Training pitcher model with {len(pitcher_training)} samples from {len([f for f in os.listdir(os.path.join(MLB_DATA_DIR, 'MLB_Training_Data')) if 'pitcher' in f.lower() and f.endswith('.csv')])} files")
        X_train, y_train = prepare_training_data(pitcher_training, "pitcher")
        if X_train is not None:
            train_model(X_train, y_train, PITCHER_MODEL_PATH)
    else:
        logger.warning("No pitcher training data available for weekly training")

    logger.info("Weekly model training completed")

def daily_predictions():
    """Make daily predictions using existing models"""
    logger.info("Starting daily prediction pipeline")

    # Load prediction data
    hitter_data, pitcher_data = load_prediction_data()

    if hitter_data is None or pitcher_data is None:
        logger.error("Failed to load master datasets")
        return None

    # Process data for predictions only
    _, _, hitter_X_pred, hitter_players_pred = preprocess_data(hitter_data, "hitter", is_training=False)
    _, _, pitcher_X_pred, pitcher_players_pred = preprocess_data(pitcher_data, "pitcher", is_training=False)

    # Initialize prediction dataframes
    hitter_predictions = pd.DataFrame()
    pitcher_predictions = pd.DataFrame()

    # Make hitter predictions if model exists
    if os.path.exists(HITTER_MODEL_PATH):
        try:
            hitter_predictions = make_predictions(hitter_X_pred, hitter_players_pred, HITTER_MODEL_PATH, "hitter")
            logger.info(f"Generated {len(hitter_predictions)} hitter predictions")
        except Exception as e:
            logger.error(f"Error making hitter predictions: {str(e)}")
    else:
        logger.error(f"Hitter model not found at {HITTER_MODEL_PATH}")

    # Make pitcher predictions if model exists
    if os.path.exists(PITCHER_MODEL_PATH):
        try:
            pitcher_predictions = make_predictions(pitcher_X_pred, pitcher_players_pred, PITCHER_MODEL_PATH, "pitcher")
            logger.info(f"Generated {len(pitcher_predictions)} pitcher predictions")
        except Exception as e:
            logger.error(f"Error making pitcher predictions: {str(e)}")
    else:
        logger.error(f"Pitcher model not found at {PITCHER_MODEL_PATH}")

    # Combine predictions
    all_predictions = pd.concat([hitter_predictions, pitcher_predictions], ignore_index=True)

    # Ensure all required columns are present
    required_columns = [
        "Player", "Prop Type", "Prop Value", "Start Time",
        "RF_Prediction", "RF_Confidence", "Model_Type",
        "LLM_Prediction", "LLM_RF_Agreement", "LLM_Confidence",
        "LLM_Justification", "Actual_Stat", "Actual_Result", "Reflection"
    ]

    for col in required_columns:
        if col not in all_predictions.columns:
            all_predictions[col] = None

    # Save predictions if we have any
    if not all_predictions.empty:
        # Save all predictions
        all_predictions.to_csv(PREDICTIONS_PATH, index=False)
        logger.info(f"All predictions saved to {PREDICTIONS_PATH}")

        # Save top picks (sorted by confidence)
        top_picks = all_predictions.sort_values("RF_Confidence", ascending=False).head(10)
        top_picks.to_csv(TOP_PICKS_PATH, index=False)
        logger.info(f"Top picks saved to {TOP_PICKS_PATH}")

        # Print summary
        print(f"\nGenerated {len(all_predictions)} predictions:")
        print(f"- Hitter props: {len(hitter_predictions)}")
        print(f"- Pitcher props: {len(pitcher_predictions)}")
        print(f"\nTop 3 highest confidence picks:")
        for i, row in top_picks.head(3).iterrows():
            print(f"- {row['Player']}: {row['Prop Type']} {row['Prop Value']} ({row['RF_Confidence']:.2f} confidence)")
    else:
        logger.warning("No predictions were generated.")

    logger.info("Daily prediction pipeline completed")
    return all_predictions

def main():
    """Main function to run the MLB machine learning pipeline"""
    while True:
        print("\nMLB Machine Learning Pipeline")
        print("----------------------------")
        print("1. Make Daily Predictions")
        print("2. Train Models (Weekly)")
        print("3. Exit")

        choice = input("\nWhat would you like to do? (1/2/3): ").strip()

        if choice == "1":
            print("\nStarting daily predictions...")
            predictions = daily_predictions()
            if predictions is not None:
                print(f"\nPredictions saved to: {PREDICTIONS_PATH}")
                print(f"Top picks saved to: {TOP_PICKS_PATH}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            confirm = input(
                "\nAre you sure you want to train the models? This should only be done weekly. (y/n): ").strip().lower()
            if confirm == 'y':
                print("\nStarting weekly training...")
                weekly_training()
                print("\nTraining completed!")
            input("\nPress Enter to continue...")

        elif choice == "3":
            print("\nExiting program...")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()

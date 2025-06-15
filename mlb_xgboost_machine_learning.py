# mlb_xgboost_machine_learning.py - Updated version with fixes for the prediction bias
import pandas as pd
import numpy as np
import joblib
import os
import datetime
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import tensorflow as tf
import logging
import argparse
from sklearn.utils.class_weight import compute_class_weight

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mlb_xgb.log"),
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

# File paths - use different paths for XGBoost models
HITTER_TRAINING_PATH = os.path.join(TRAINING_DIR, "hitter_training_data.csv")
PITCHER_TRAINING_PATH = os.path.join(TRAINING_DIR, "pitcher_training_data.csv")
HITTER_MODEL_PATH = os.path.join(MODEL_DIR, "mlb_hitter_xgb_model.pkl")
PITCHER_MODEL_PATH = os.path.join(MODEL_DIR, "mlb_pitcher_xgb_model.pkl")
TODAY_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
PREDICTIONS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_xgb_predictions.csv")
TOP_PICKS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_xgb_top_picks.csv")


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

def get_model_features(data, prop_type):
    """Get consistent feature set for both training and prediction"""
    # Core features that should always be present
    core_features = [
        "Prop Value",
        "Game-Time Temp (F)",
        "Game-Time Humidity (%)",
        "Game-Time Wind Speed (mph)"
    ]

    if prop_type == "hitter":
        core_features.extend([
            "AVG_vs_rhp", "OBP_vs_rhp", "SLG_vs_rhp", "OPS_vs_rhp",
            "AVG_vs_lhp", "OBP_vs_lhp", "SLG_vs_lhp", "OPS_vs_lhp",
            "wOBA", "xwOBA", "Barrel%", "Hard Hit %"
        ])
    else:  # pitcher
        core_features.extend([
            "ERA", "WHIP", "K/9", "BB/9", "K/BB", "HR/9",
            "K%", "BB%", "K-BB%", "LOB%"
        ])

    # Get available features
    features = pd.DataFrame()

    # Add core numeric features that exist
    numeric_features = [f for f in core_features if f in data.columns]
    if numeric_features:
        features = data[numeric_features].copy()

    # Add prop type dummies consistently
    if "Prop Type" in data.columns:
        prop_dummies = pd.get_dummies(data["Prop Type"], prefix="prop")
        features = pd.concat([features, prop_dummies], axis=1)

    return features

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
        features = features.fillna(0)
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

    data = data.copy()

    # Convert percentage columns
    percentage_columns = [col for col in data.columns if '%' in col]
    for col in percentage_columns:
        try:
            data[col] = data[col].astype(str).str.rstrip('%').astype(float) / 100
            logger.info(f"Converted percentage column {col} to float")
        except Exception as e:
            logger.warning(f"Could not convert percentage column {col}: {e}")

    # Handle categorical columns
    categorical_columns = ['Prop Type', 'Pitcher Handedness',
                           'Game-Time Effect on Hitters', 'Odds Category']
    for col in categorical_columns:
        if col in data.columns:
            dummies = pd.get_dummies(data[col], prefix=col)
            data = pd.concat([data, dummies], axis=1)
            logger.info(f"Encoded categorical column {col} into {len(dummies.columns)} features")

    # Convert remaining numeric columns
    numeric_columns = [
        'Prop Value', 'Game-Time Temp (F)', 'Game-Time Humidity (%)',
        'Game-Time Wind Speed (mph)', 'Park_Factor_Basic', 'Park_Factor_HR',
        'AVG_vs_rhp', 'OBP_vs_rhp', 'SLG_vs_rhp', 'OPS_vs_rhp',
        'AVG_vs_lhp', 'OBP_vs_lhp', 'SLG_vs_lhp', 'OPS_vs_lhp',
        'wOBA', 'xwOBA', 'EV', 'ERA', 'WHIP', 'K/9', 'BB/9', 'HR/9'
    ]

    for col in data.columns:
        if col in numeric_columns or any(x in col.lower() for x in ['avg', 'ops', 'woba', 'era', 'whip']):
            try:
                data[col] = pd.to_numeric(data[col], errors='coerce')
            except Exception as e:
                logger.warning(f"Could not convert column {col} to numeric: {e}")

    # Fill NaN values
    data = data.fillna(0)

    return data

def select_hitter_features(data):
    """Select features for hitter model"""
    # Define core features for hitters
    core_features = [
        # Basic info
        "Prop Value",

        # Stats vs handedness
        "AVG_vs_rhp", "OBP_vs_rhp", "SLG_vs_rhp", "OPS_vs_rhp",
        "AVG_vs_lhp", "OBP_vs_lhp", "SLG_vs_lhp", "OPS_vs_lhp",

        # Advanced metrics
        "wOBA", "xwOBA", "Barrel%", "Hard Hit %",

        # Game conditions
        "Game-Time Temp (F)", "Game-Time Humidity (%)",
        "Game-Time Wind Speed (mph)",

        # Park factors
        "Park_Factor_Basic", "Park_Factor_HR"
    ]

    # Get available features
    features = pd.DataFrame()

    # Add core numeric features that exist
    numeric_features = [f for f in core_features if f in data.columns]
    if numeric_features:
        features = data[numeric_features].copy()

    # Add prop type dummies consistently
    if "Prop Type" in data.columns:
        prop_dummies = pd.get_dummies(data["Prop Type"], prefix="prop")
        features = pd.concat([features, prop_dummies], axis=1)

    # Add pitcher handedness dummy
    if "Pitcher Handedness" in data.columns:
        features["Pitcher_Right"] = (data["Pitcher Handedness"] == "right").astype(int)

    # Add game effect dummies
    if "Game-Time Effect on Hitters" in data.columns:
        effect_map = {
            "Tailwind: fly balls likely to carry  helps hitters.": 1,
            "Headwind: fly balls suppressed  hurts hitters.": -1,
            "Crosswind: minimal effect on hitters.": 0,
            "No wind: no effect on hitters.": 0
        }
        features["Wind_Effect"] = data["Game-Time Effect on Hitters"].map(effect_map).fillna(0)

    return features

def select_pitcher_features(data):
    """Select features for pitcher model"""
    # Define core features for pitchers
    core_features = [
        # Basic info
        "Prop Value",

        # Basic stats
        "ERA", "WHIP", "K/9", "BB/9", "K/BB", "HR/9",
        "K%", "BB%", "K-BB%", "AVG Against", "BABIP", "LOB%",

        # Game conditions
        "Game-Time Temp (F)", "Game-Time Humidity (%)",
        "Game-Time Wind Speed (mph)"
    ]

    # Get available features
    features = pd.DataFrame()

    # Add core numeric features that exist
    numeric_features = [f for f in core_features if f in data.columns]
    if numeric_features:
        features = data[numeric_features].copy()

    # Add prop type dummies consistently
    if "Prop Type" in data.columns:
        prop_dummies = pd.get_dummies(data["Prop Type"], prefix="prop")
        features = pd.concat([features, prop_dummies], axis=1)

    # Add wind effect
    if "Game-Time Effect on Hitters" in data.columns:
        effect_map = {
            "Tailwind: fly balls likely to carry  helps hitters.": 1,
            "Headwind: fly balls suppressed  hurts hitters.": -1,
            "Crosswind: minimal effect on hitters.": 0,
            "No wind: no effect on hitters.": 0
        }
        features["Wind_Effect"] = data["Game-Time Effect on Hitters"].map(effect_map).fillna(0)

    return features

def train_model(X, y, model_path, prop_type):
    """Train XGBoost model with grid search CV"""
    if X is None or len(X) == 0:
        logger.warning(f"No training data available for {prop_type}")
        return None

    # Clean target variable - ensure it only contains 0 and 1
    y = y.replace(-999, 0)  # Replace any -999 values with 0

    # Check for any other values that are not 0 or 1
    unique_values = np.unique(y)
    if not all(val in [0, 1] for val in unique_values):
        logger.warning(f"Target variable contains values other than 0 and 1: {unique_values}")
        # Convert to binary (0 or 1)
        y = (y > 0).astype(int)
        logger.info(f"Converted target to binary. New unique values: {np.unique(y)}")

    # Log class distribution
    class_counts = np.bincount(y)
    logger.info(f"Class distribution - 0: {class_counts[0]}, 1: {class_counts[1]}")

    # Calculate class weights
    class_weights = compute_class_weight('balanced', classes=np.unique(y), y=y)
    class_weight_dict = {i: weight for i, weight in enumerate(class_weights)}
    logger.info(f"Class weights: {class_weight_dict}")

    # Split data for evaluation
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Define parameter grid for XGBoost
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [3, 6, 10],
        'learning_rate': [0.01, 0.1, 0.3],
        'subsample': [0.8, 1.0],
        'colsample_bytree': [0.8, 1.0],
        'scale_pos_weight': [1, 3, 5]  # Increased options for handling class imbalance
    }

    # Initialize XGBoost model
    xgb = XGBClassifier(
        random_state=42,
        use_label_encoder=False,
        eval_metric='auc',  # Changed to AUC for better handling of imbalanced data
        objective='binary:logistic'
    )

    # Grid search with cross validation
    grid_search = GridSearchCV(
        estimator=xgb,
        param_grid=param_grid,
        cv=5,
        n_jobs=-1,
        verbose=0,
        scoring='roc_auc'  # Changed to AUC for better handling of imbalanced data
    )

    # Fit model
    grid_search.fit(X_train, y_train)

    # Get best model
    best_model = grid_search.best_estimator_

    # Log results
    logger.info(f"Best parameters: {grid_search.best_params_}")
    logger.info(f"Best cross-validation score: {grid_search.best_score_:.3f}")

    # Evaluate on validation set
    y_pred = best_model.predict(X_val)
    y_prob = best_model.predict_proba(X_val)[:, 1]

    # Calculate metrics
    accuracy = accuracy_score(y_val, y_pred)
    auc = roc_auc_score(y_val, y_prob)

    logger.info(f"Validation accuracy: {accuracy:.3f}")
    logger.info(f"Validation AUC: {auc:.3f}")
    logger.info(f"Validation confusion matrix:\n{confusion_matrix(y_val, y_pred)}")
    logger.info(f"Validation classification report:\n{classification_report(y_val, y_pred)}")

    # Check prediction distribution
    pred_counts = np.bincount(y_pred)
    logger.info(f"Prediction distribution - 0: {pred_counts[0]}, 1: {pred_counts[1]}")

    # If model is heavily biased, try to adjust the threshold
    if pred_counts[0] < 0.1 * len(y_pred) or pred_counts[1] < 0.1 * len(y_pred):
        logger.warning(f"Model predictions are heavily biased ({pred_counts}). Adjusting threshold...")

        # Find optimal threshold
        thresholds = np.linspace(0.1, 0.9, 9)
        best_threshold = 0.5
        best_balanced_acc = 0

        for threshold in thresholds:
            y_pred_threshold = (y_prob >= threshold).astype(int)
            tn, fp, fn, tp = confusion_matrix(y_val, y_pred_threshold).ravel()
            sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            balanced_acc = (sensitivity + specificity) / 2

            logger.info(f"Threshold {threshold:.1f}: Balanced Acc {balanced_acc:.3f}, "
                        f"Sensitivity {sensitivity:.3f}, Specificity {specificity:.3f}")

            if balanced_acc > best_balanced_acc:
                best_balanced_acc = balanced_acc
                best_threshold = threshold

        logger.info(f"Selected optimal threshold: {best_threshold:.3f} with balanced accuracy: {best_balanced_acc:.3f}")

        # Save threshold with model
        model_data = {
            'model': best_model,
            'feature_names': X.columns.tolist(),
            'threshold': best_threshold
        }
    else:
        # Save model with default threshold
        model_data = {
            'model': best_model,
            'feature_names': X.columns.tolist(),
            'threshold': 0.5
        }

    # Save model data
    try:
        joblib.dump(model_data, model_path)
        logger.info(f"Model saved to {model_path}")
    except Exception as e:
        logger.error(f"Error saving model: {e}")
        return None

    return best_model

def make_predictions(X_pred, players_pred, model_path, prop_type):
    """Make predictions using saved model"""
    if X_pred is None or len(X_pred) == 0:
        logger.warning(f"No prediction data available for {prop_type}")
        return pd.DataFrame()

    try:
        # Load the model data
        model_data = joblib.load(model_path)
        model = model_data['model']
        feature_names = model_data['feature_names']
        threshold = model_data.get('threshold', 0.5)  # Get custom threshold if available

        # Log feature names for debugging
        logger.info(f"Model features: {feature_names}")
        logger.info(f"Prediction features: {X_pred.columns.tolist()}")
        logger.info(f"Using prediction threshold: {threshold}")

        # Ensure features match
        X_pred = X_pred.reindex(columns=feature_names, fill_value=0)

        # Make predictions
        probs = model.predict_proba(X_pred)[:, 1]
        preds = (probs >= threshold).astype(int)  # Apply threshold

        # Log prediction distribution
        pred_counts = np.bincount(preds)
        logger.info(f"Prediction distribution - 0: {pred_counts[0]}, 1: {pred_counts[1]}")

        logger.info(f"Generated {len(preds)} {prop_type} predictions")

    except Exception as e:
        logger.error(f"Error making predictions: {e}")
        return pd.DataFrame()

    # Create predictions DataFrame
    predictions_df = players_pred.copy()
    predictions_df["XGB_Prediction"] = preds
    predictions_df["XGB_Confidence"] = probs
    predictions_df["Model_Type"] = prop_type

    return predictions_df

def weekly_training():
    """Perform weekly model training using all accumulated training data"""
    logger.info("Starting weekly model training")

    # Load all training data
    hitter_training, pitcher_training = load_training_data()

    # Train hitter model
    if hitter_training is not None and len(hitter_training) > 0:
        logger.info(f"Training hitter model with {len(hitter_training)} samples")

        # Feature engineering
        hitter_training = feature_engineering(hitter_training, "hitter")

        # Get features and target
        X = get_model_features(hitter_training, "hitter")

        # Ensure Hit column exists and is properly formatted
        if "Hit" not in hitter_training.columns:
            logger.error("Hit column not found in hitter training data")
            return

        # Clean target variable - ensure it's binary
        y = hitter_training["Hit"].fillna(0)  # Fill NaN with 0
        y = y.replace(-999, 0)  # Replace -999 with 0
        y = y.astype(int)  # Convert to integer

        # Check unique values
        unique_values = np.unique(y)
        logger.info(f"Hitter target unique values: {unique_values}")

        # Ensure binary classification
        if not all(val in [0, 1] for val in unique_values):
            logger.warning(f"Converting non-binary values to binary classification")
            y = (y > 0).astype(int)

        # Log class distribution
        class_counts = np.bincount(y)
        logger.info(f"Hitter class distribution - 0: {class_counts[0]}, 1: {class_counts[1]}")

        # Train model
        train_model(X, y, HITTER_MODEL_PATH, "hitter")
    else:
        logger.warning("No hitter training data available")

    # Train pitcher model
    if pitcher_training is not None and len(pitcher_training) > 0:
        logger.info(f"Training pitcher model with {len(pitcher_training)} samples")

        # Feature engineering
        pitcher_training = feature_engineering(pitcher_training, "pitcher")

        # Get features and target
        X = get_model_features(pitcher_training, "pitcher")

        # Ensure Hit column exists and is properly formatted
        if "Hit" not in pitcher_training.columns:
            logger.error("Hit column not found in pitcher training data")
            return

        # Clean target variable - ensure it's binary
        y = pitcher_training["Hit"].fillna(0)  # Fill NaN with 0
        y = y.replace(-999, 0)  # Replace -999 with 0
        y = y.astype(int)  # Convert to integer

        # Check unique values
        unique_values = np.unique(y)
        logger.info(f"Pitcher target unique values: {unique_values}")

        # Ensure binary classification
        if not all(val in [0, 1] for val in unique_values):
            logger.warning(f"Converting non-binary values to binary classification")
            y = (y > 0).astype(int)

        # Log class distribution
        class_counts = np.bincount(y)
        logger.info(f"Pitcher class distribution - 0: {class_counts[0]}, 1: {class_counts[1]}")

        # Train model
        train_model(X, y, PITCHER_MODEL_PATH, "pitcher")
    else:
        logger.warning("No pitcher training data available")

    logger.info("Weekly model training completed")

def daily_predictions():
    """Make daily predictions using existing models"""
    logger.info("Starting daily prediction pipeline")

    # Load prediction data
    hitter_data, pitcher_data = load_prediction_data()

    # Process hitter data
    hitter_predictions = None
    if hitter_data is not None and len(hitter_data) > 0:
        logger.info("Preprocessing hitter data...")

        # Feature engineering
        hitter_data = feature_engineering(hitter_data, "hitter")

        # Select features
        X_hitter = get_model_features(hitter_data, "hitter")

        # Make predictions
        hitter_predictions = make_predictions(X_hitter,
                                              hitter_data[["Player", "Prop Type", "Prop Value", "Start Time"]],
                                              HITTER_MODEL_PATH, "hitter")

    # Process pitcher data
    pitcher_predictions = None
    if pitcher_data is not None and len(pitcher_data) > 0:
        logger.info("Preprocessing pitcher data...")

        # Feature engineering
        pitcher_data = feature_engineering(pitcher_data, "pitcher")

        # Select features
        X_pitcher = get_model_features(pitcher_data, "pitcher")

        # Make predictions
        pitcher_predictions = make_predictions(X_pitcher,
                                               pitcher_data[["Player", "Prop Type", "Prop Value", "Start Time"]],
                                               PITCHER_MODEL_PATH, "pitcher")

    # Combine predictions
    all_predictions = pd.concat([
        hitter_predictions if hitter_predictions is not None else pd.DataFrame(),
        pitcher_predictions if pitcher_predictions is not None else pd.DataFrame()
    ], ignore_index=True)

    # Ensure all required columns are present
    required_columns = [
        "Player", "Prop Type", "Prop Value", "Start Time",
        "XGB_Prediction", "XGB_Confidence", "Model_Type",
        "LLM_Prediction", "LLM_XGB_Agreement", "LLM_Confidence",
        "LLM_Justification", "Actual_Stat", "Actual_Result", "Reflection"
    ]

    for col in required_columns:
        if col not in all_predictions.columns:
            all_predictions[col] = None

    # Save predictions if we have any
    if not all_predictions.empty:
        # Save all predictions
        all_predictions.to_csv(PREDICTIONS_PATH, index=False)
        logger.info(f"Predictions saved to {PREDICTIONS_PATH}")

        # Save top 10 picks (sorted by confidence)
        top_picks = all_predictions.sort_values("XGB_Confidence", ascending=False).head(10)
        top_picks.to_csv(TOP_PICKS_PATH, index=False)
        logger.info(f"Top 10 picks saved to {TOP_PICKS_PATH}")

        # Print summary
        print(f"\nGenerated {len(all_predictions)} predictions:")
        print(f"- Hitter props: {len(hitter_predictions) if hitter_predictions is not None else 0}")
        print(f"- Pitcher props: {len(pitcher_predictions) if pitcher_predictions is not None else 0}")
        print(f"\nTop 3 highest confidence picks:")
        for i, row in all_predictions.sort_values("XGB_Confidence", ascending=False).head(3).iterrows():
            print(f"- {row['Player']}: {row['Prop Type']} {row['Prop Value']} ({row['XGB_Confidence']:.2f} confidence)")
    else:
        logger.warning("No predictions were generated.")

    logger.info("Daily prediction pipeline completed")
    return all_predictions

def main():
    """Main function to run the MLB XGBoost machine learning pipeline"""
    while True:
        print("\nMLB XGBoost Machine Learning Pipeline")
        print("-----------------------------------")
        print("1. Make Daily Predictions with XGBoost")
        print("2. Train XGBoost Models (Weekly)")
        print("3. Exit")

        choice = input("\nWhat would you like to do? (1/2/3): ").strip()

        if choice == "1":
            print("\nStarting daily predictions with XGBoost...")
            predictions = daily_predictions()
            if predictions is not None:
                print(f"\nPredictions saved to: {PREDICTIONS_PATH}")
                print(f"Top picks saved to: {TOP_PICKS_PATH}")
            input("\nPress Enter to continue...")

        elif choice == "2":
            confirm = input(
                "\nAre you sure you want to train the XGBoost models? This should only be done weekly. (y/n): ").strip().lower()
            if confirm == 'y':
                print("\nStarting weekly XGBoost training...")
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
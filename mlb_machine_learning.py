import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import os
import datetime

# STEP 1: Configuration
MLB_DATA_DIR = "../MLB_Prop_Data_CSV"
MODEL_DIR = "../MLB_Models"
RESULTS_DIR = "../MLB_Results"
LOG_DIR = "../MLB_Logs"

# Create directories if they don't exist
for directory in [MLB_DATA_DIR, MODEL_DIR, RESULTS_DIR, LOG_DIR]:
    os.makedirs(directory, exist_ok=True)

# File paths
MERGED_DATA_PATH = os.path.join(MLB_DATA_DIR, "merged_hitter_pitcher_dataset.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "mlb_rf_model.pkl")
TODAY_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
PREDICTIONS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_predictions.csv")
TOP_PICKS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_top_picks.csv")

# STEP 2: Load Merged Data
print(f"Loading data from {MERGED_DATA_PATH}")
try:
    data = pd.read_csv(MERGED_DATA_PATH)
    print(f"Loaded data with shape: {data.shape}")
except FileNotFoundError:
    print(f"Error: File not found at {MERGED_DATA_PATH}")
    print("Make sure to run the data merging scripts first.")
    exit(1)

# STEP 3: Check if "Hit" column exists
if "Hit" not in data.columns:
    print("'Hit' column missing. Assuming this is a prediction day.")
    data["Hit"] = np.nan  # Create an empty column for later

# STEP 4: Define the expected features for MLB data
# These should match the columns in your merged dataset
expected_features = [
    # Player and Team Info
    'Team_hitter', 'Position', 'Opposing Team',

    # Game Conditions
    'Stadium', 'Game-Time Temp (F)', 'Game-Time Humidity (%)',
    'Game-Time Wind Speed (mph)', 'Game-Time Wind Dir ()',
    'Game-Time Effect on Hitters',

    # Park Factors
    'Park_Factor_Basic', 'Park_Factor_1B', 'Park_Factor_2B',
    'Park_Factor_3B', 'Park_Factor_HR', 'Park_Factor_SO',
    'Park_Factor_BB', 'Park_Factor_GB', 'Park_Factor_FB',
    'Park_Factor_LD', 'Park_Factor_IFFB', 'Park_Factor_FIP',

    # Prop Info
    'Prop Type', 'Prop Value',

    # Hitter Stats vs RHP/LHP
    'AVG_vs_rhp', 'OBP_vs_rhp', 'SLG_vs_rhp', 'OPS_vs_rhp',
    'AVG_vs_lhp', 'OBP_vs_lhp', 'SLG_vs_lhp', 'OPS_vs_lhp',

    # Hitter Recent Performance
    'AVG_vs_rhp_5', 'OBP_vs_rhp_5', 'SLG_vs_rhp_5', 'OPS_vs_rhp_5',
    'AVG_vs_rhp_10', 'OBP_vs_rhp_10', 'SLG_vs_rhp_10', 'OPS_vs_rhp_10',
    'AVG_vs_rhp_15', 'OBP_vs_rhp_15', 'SLG_vs_rhp_15', 'OPS_vs_rhp_15',
    'AVG_vs_lhp_5', 'OBP_vs_lhp_5', 'SLG_vs_lhp_5', 'OPS_vs_lhp_5',
    'AVG_vs_lhp_10', 'OBP_vs_lhp_10', 'SLG_vs_lhp_10', 'OPS_vs_lhp_10',
    'AVG_vs_lhp_15', 'OBP_vs_lhp_15', 'SLG_vs_lhp_15', 'OPS_vs_lhp_15',

    # Hitter Advanced Metrics
    'wOBA', 'xwOBA', 'Barrel%', 'Hard Hit %', 'EV',

    # Hitter Hot Zones
    'heart_swing_pct', 'shadow_swing_pct', 'chase_swing_pct', 'waste_swing_pct',

    # Pitcher Stats
    'ERA_pitcher', 'WHIP_pitcher', 'K/9_pitcher', 'BB/9_pitcher', 'HR/9_pitcher',

    # Pitcher Advanced Metrics
    'K%', 'BB%', 'K-BB%', 'AVG Against', 'BABIP', 'LOB%', 'ERA-', 'FIP', 'FIP-',

    # Pitcher Recent Performance
    '15_day_ERA', '15_day_WHIP', '15_day_K/9', '15_day_BB/9',
    '30_day_ERA', '30_day_WHIP', '30_day_K/9', '30_day_BB/9',

    # Pitcher Hot Zones
    'heart_pitch_pct_pitcher', 'shadow_pitch_pct_pitcher',
    'chase_pitch_pct_pitcher', 'waste_pitch_pct_pitcher',

    # Pitcher Pitch Usage
    'Fastball%', 'Sinker%', 'Cutter%', 'Slider%', 'Changeup%', 'Curveball%', 'Splitter%'
]

# STEP 4.5: Feature Engineering
print("Performing feature engineering...")

# 1. Pitcher vs Hitter Advantage Score
# This creates a composite score based on pitcher and hitter strengths
if all(col in data.columns for col in ['wOBA', 'xwOBA', 'ERA_pitcher', 'FIP']):
    # Normalize metrics to 0-1 scale for comparison
    data['wOBA_norm'] = (data['wOBA'] - data['wOBA'].min()) / (data['wOBA'].max() - data['wOBA'].min())
    data['xwOBA_norm'] = (data['xwOBA'] - data['xwOBA'].min()) / (data['xwOBA'].max() - data['xwOBA'].min())

    # Invert pitcher metrics so higher is better for pitcher (worse for hitter)
    data['ERA_norm'] = 1 - (data['ERA_pitcher'] - data['ERA_pitcher'].min()) / (
                data['ERA_pitcher'].max() - data['ERA_pitcher'].min())
    data['FIP_norm'] = 1 - (data['FIP'] - data['FIP'].min()) / (data['FIP'].max() - data['FIP'].min())

    # Create advantage scores (positive favors hitter, negative favors pitcher)
    data['Hitter_Advantage_Score'] = (data['wOBA_norm'] + data['xwOBA_norm']) - (data['ERA_norm'] + data['FIP_norm'])

    # Add to expected features
    expected_features.append('Hitter_Advantage_Score')
    print("Added Hitter Advantage Score feature")

# 2. Weather-Performance Interaction Terms
if all(col in data.columns for col in ['Game-Time Temp (F)', 'Game-Time Wind Speed (mph)', 'Game-Time Humidity (%)']):
    # Temperature interactions
    data['Temp_x_SLG'] = data['Game-Time Temp (F)'] * data['SLG_vs_rhp'] if 'SLG_vs_rhp' in data.columns else 0
    data['Temp_x_HR/9'] = data['Game-Time Temp (F)'] * data['HR/9_pitcher'] if 'HR/9_pitcher' in data.columns else 0

    # Wind interactions - higher wind can affect power hitting
    data['Wind_x_SLG'] = data['Game-Time Wind Speed (mph)'] * data['SLG_vs_rhp'] if 'SLG_vs_rhp' in data.columns else 0
    data['Wind_x_Barrel%'] = data['Game-Time Wind Speed (mph)'] * data['Barrel%'] if 'Barrel%' in data.columns else 0

    # Humidity interactions
    data['Humidity_x_EV'] = data['Game-Time Humidity (%)'] * data['EV'] if 'EV' in data.columns else 0

    # Add to expected features
    new_weather_features = ['Temp_x_SLG', 'Temp_x_HR/9', 'Wind_x_SLG', 'Wind_x_Barrel%', 'Humidity_x_EV']
    expected_features.extend(new_weather_features)
    print(f"Added {len(new_weather_features)} weather interaction features")

# 3. Hot/Cold Streaks (comparing recent to season performance)
if all(col in data.columns for col in ['AVG_vs_rhp', 'AVG_vs_rhp_5']):
    # Hitting streak indicators
    data['AVG_Trend'] = data['AVG_vs_rhp_5'] - data['AVG_vs_rhp']
    data['OPS_Trend'] = data['OPS_vs_rhp_5'] - data['OPS_vs_rhp'] if all(
        col in data.columns for col in ['OPS_vs_rhp_5', 'OPS_vs_rhp']) else 0

    # Pitcher trend indicators
    data['ERA_Trend'] = data['ERA_pitcher'] - data['15_day_ERA'] if all(
        col in data.columns for col in ['ERA_pitcher', '15_day_ERA']) else 0
    data['WHIP_Trend'] = data['WHIP_pitcher'] - data['15_day_WHIP'] if all(
        col in data.columns for col in ['WHIP_pitcher', '15_day_WHIP']) else 0

    # Add to expected features
    trend_features = ['AVG_Trend', 'OPS_Trend', 'ERA_Trend', 'WHIP_Trend']
    expected_features.extend(trend_features)
    print(f"Added {len(trend_features)} trend features")

print(f"Feature engineering complete. Total features: {len(expected_features)}")

# STEP 5: Ensure Consistent Features for Training/Prediction
missing_value_marker = -999

# Check which expected features are actually in the data
available_features = [feature for feature in expected_features if feature in data.columns]
missing_features = [feature for feature in expected_features if feature not in data.columns]

if missing_features:
    print(f"Warning: {len(missing_features)} expected features are missing from the dataset:")
    print(", ".join(missing_features[:10]) + ("..." if len(missing_features) > 10 else ""))

    # Add missing features with placeholder values
    for feature in missing_features:
        data[feature] = missing_value_marker

# STEP 6: Separate Features and Target Variable
X = data[available_features]  # Only use available features
y = data["Hit"] if "Hit" in data.columns else pd.Series([np.nan] * len(data))

# STEP 7: Handle Missing Target Values
X_train = X[~y.isna()]
y_train = y[~y.isna()]
X_pred = X[y.isna()]  # Data where we need predictions
players_pred = data.loc[
    y.isna(), ["Player_hitter", "Prop Type", "Prop Value"]] if "Player_hitter" in data.columns else pd.DataFrame()

# STEP 8: Setup TensorBoard Logging
writer = tf.summary.create_file_writer(LOG_DIR)
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=LOG_DIR, histogram_freq=1)

# STEP 9: Train the Model (if we have past labeled data)
if not X_train.empty:
    print(f"Training model on {len(X_train)} samples with {len(available_features)} features")

    # Split data for training and validation
    X_train_split, X_test_split, y_train_split, y_test_split = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42)

    # Train Random Forest model with improved parameters
    model = RandomForestClassifier(
        n_estimators=200,  # More trees for better performance
        max_depth=20,  # Control depth to prevent overfitting
        min_samples_split=5,
        min_samples_leaf=2,
        bootstrap=True,
        random_state=42,
        n_jobs=-1  # Use all available cores
    )
    model.fit(X_train_split, y_train_split)

    # Evaluate model
    y_pred_test = model.predict(X_test_split)
    acc = accuracy_score(y_test_split, y_pred_test)
    print(f"Model Trained. Accuracy on test set: {acc:.2f}")

    # Print detailed metrics
    print("\nClassification Report:")
    print(classification_report(y_test_split, y_pred_test))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test_split, y_pred_test))

    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': available_features,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)

    print("\nTop 10 Most Important Features:")
    print(feature_importance.head(10))

    # Save top features to CSV for reference
    feature_importance.to_csv(os.path.join(MODEL_DIR, "feature_importance.csv"), index=False)

    # Log accuracy to TensorBoard
    with writer.as_default():
        tf.summary.scalar("Accuracy", acc, step=0)

        # Log top 10 feature importances
        for i, (feature, importance) in enumerate(zip(feature_importance['Feature'].head(10),
                                                      feature_importance['Importance'].head(10))):
            tf.summary.scalar(f"feature_importance/{feature}", importance, step=0)

    # Save the model
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved as '{MODEL_PATH}'")

else:
    print("No past outcomes available to train the model.")

# STEP 10: Make Predictions for Today's Props
if not X_pred.empty:
    # 10a) Ensure we have a trained model
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"No trained model found at {MODEL_PATH}. Train the model first by uploading data with 'Hit' column."
        )

    # 10b) Load model
    print(f"Loading model from {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)

    # 10c) Ensure X_pred has the same features as the model was trained on
    missing_cols = set(model.feature_names_in_) - set(X_pred.columns)
    for col in missing_cols:
        X_pred[col] = missing_value_marker

    # Reorder columns to match training order
    X_pred = X_pred[model.feature_names_in_]

    # 10d) Predict and get probabilities
    print(f"Making predictions for {len(X_pred)} props")
    predictions = model.predict(X_pred)
    probabilities = model.predict_proba(X_pred)[:, 1]  # Probability of class 1 (Hit)

    # 10e) Assemble output DataFrame
    predictions_df = players_pred.copy()
    predictions_df["RF_Prediction"] = predictions
    predictions_df["RF_Confidence"] = probabilities
    predictions_df["LLM_Prediction"] = None
    predictions_df["LLM_Justification"] = None
    predictions_df["Actual_Result"] = None
    predictions_df["Reflection"] = None

    # 10f) De-duplicate exact repeats
    predictions_df = predictions_df.drop_duplicates(
        subset=["Player_hitter", "Prop Value", "Prop Type"],
        keep="first"
    )

    # 10g) Filter out any rows with missing values
    predictions_df = predictions_df[predictions_df["RF_Prediction"] != missing_value_marker]

    # 10h) Write to CSV files
    predictions_df.to_csv(PREDICTIONS_PATH, index=False)
    print(f"Predictions saved as '{PREDICTIONS_PATH}'")

    # Get top picks (highest confidence)
    top_picks = predictions_df.sort_values("RF_Confidence", ascending=False).head(10)
    top_picks.to_csv(TOP_PICKS_PATH, index=False)
    print(f"Top 10 picks saved as '{TOP_PICKS_PATH}'")

    # 10i) Log to TensorBoard
    with writer.as_default():
        tf.summary.scalar("Predictions Made", len(predictions_df), step=0)

        # Log confidence distribution
        confidence_bins = np.linspace(0, 1, 11)  # 0.0, 0.1, 0.2, ..., 1.0
        hist, _ = np.histogram(predictions_df["RF_Confidence"], bins=confidence_bins)
        for i, count in enumerate(hist):
            bin_name = f"{confidence_bins[i]:.1f}-{confidence_bins[i + 1]:.1f}"
            tf.summary.scalar(f"confidence_distribution/{bin_name}", count, step=0)

else:
    print("No new props to predict today.")

print("MLB Machine Learning process completed.")
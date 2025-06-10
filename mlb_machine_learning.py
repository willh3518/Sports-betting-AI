# Updated mlb_machine_learning.py
import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
import os
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Config
MLB_DATA_DIR = "MLB_Prop_Data_CSV"
MODEL_DIR = "MLB_Models"
RESULTS_DIR = "MLB_Results"
LOG_DIR = "MLB_Logs"

MERGED_DATA_PATH = os.path.join(MLB_DATA_DIR, "merged_hitter_pitcher_dataset.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "mlb_rf_model.pkl")
TODAY_DATE = datetime.datetime.now().strftime("%Y-%m-%d")
PREDICTIONS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_predictions.csv")
TOP_PICKS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_top_picks.csv")

# Load Data
print(f"Loading data from {MERGED_DATA_PATH}")
try:
    data = pd.read_csv(MERGED_DATA_PATH)
    print(f"Loaded data with shape: {data.shape}")
except FileNotFoundError:
    print(f"File not found at {MERGED_DATA_PATH}. Run merge script first.")
    exit(1)

# Setup Hit Column
if "Hit" not in data.columns:
    print("'Hit' column missing. Assuming this is a prediction day.")
    data["Hit"] = np.nan

# Define expected features (synced with cleaned dataset)
expected_features = [
    'Position', 'Opposing Team_hitter', 'Game-Time Temp (°F)', 'Game-Time Humidity (%)',
    'Game-Time Wind Speed (mph)', 'Game-Time Wind Dir (°)', 'Game-Time Effect on Hitters',
    'Prop Type', 'Prop Value', 'wOBA', 'xwOBA', 'Barrel%', 'Hard Hit %', 'EV',
    'heart_swing_pct', 'shadow_swing_pct', 'chase_swing_pct', 'waste_swing_pct',
    'ERA', 'WHIP', 'K/9', 'BB/9', 'HR/9', 'K%', 'BB%', 'K-BB%', 'AVG Against',
    'BABIP', 'LOB%', 'ERA-', 'FIP', 'FIP-',
    '15_day_fastball_velo', '15_day_fastball_spin', '15_day_hard_hit_pct',
    '15_day_barrel_pct', '15_day_gb_pct', '15_day_fb_pct', '15_day_ld_pct',
    '30_day_fastball_velo', '30_day_fastball_spin', '30_day_hard_hit_pct',
    '30_day_barrel_pct', '30_day_gb_pct', '30_day_fb_pct', '30_day_ld_pct'
]

print("Performing feature engineering...")

# Handle pitcher handedness and select correct wOBA splits
if all(col in data.columns for col in ["Opposing Pitcher", "Pitcher Handedness", "xwOBA", "ERA", "FIP"]):
    data["wOBA_split"] = np.where(
        data["Pitcher Handedness"].str.lower() == "right",
        data.get("wOBA_vs_rhp", np.nan),
        data.get("wOBA_vs_lhp", np.nan)
    )

    if data["wOBA_split"].isna().all():
        print("⚠️ No valid wOBA split data found — skipping Hitter_Advantage_Score.")
    else:
        data["wOBA_norm"] = (data["wOBA_split"] - data["wOBA_split"].min()) / (data["wOBA_split"].max() - data["wOBA_split"].min())
        data["xwOBA_norm"] = (data["xwOBA"] - data["xwOBA"].min()) / (data["xwOBA"].max() - data["xwOBA"].min())
        data["ERA_norm"] = 1 - (data["ERA"] - data["ERA"].min()) / (data["ERA"].max() - data["ERA"].min())
        data["FIP_norm"] = 1 - (data["FIP"] - data["FIP"].min()) / (data["FIP"].max() - data["FIP"].min())

        data["Hitter_Advantage_Score"] = (
            data["wOBA_norm"].fillna(0) +
            data["xwOBA_norm"].fillna(0)
            - data["ERA_norm"].fillna(0)
            - data["FIP_norm"].fillna(0)
        )

        expected_features.append("Hitter_Advantage_Score")
        print("✅ Added Hitter_Advantage_Score based on pitcher handedness.")
else:
    print("⚠️ Skipping Hitter_Advantage_Score — missing required columns.")



print("Feature engineering complete.")

# Prepare Data
missing_value_marker = -999
available_features = [f for f in expected_features if f in data.columns]
missing_features = [f for f in expected_features if f not in data.columns]

for f in missing_features:
    data[f] = missing_value_marker

X = data[expected_features]
y = data["Hit"]

X_train = X[~y.isna()]
y_train = y[~y.isna()]
X_pred = X[y.isna()]

players_pred = data.loc[
    y.isna(), ["Player_hitter", "Prop Type", "Prop Value"]] if "Player_hitter" in data.columns else pd.DataFrame()

# Logging
writer = tf.summary.create_file_writer(LOG_DIR)

# Train Model
if not X_train.empty:
    print(f"Training model on {len(X_train)} samples")
    X_train_split, X_test_split, y_train_split, y_test_split = train_test_split(X_train, y_train, test_size=0.2,
                                                                                random_state=42)

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
    y_pred_test = model.predict(X_test_split)
    acc = accuracy_score(y_test_split, y_pred_test)

    print(f"Model accuracy: {acc:.2f}")
    print("Classification Report:\n", classification_report(y_test_split, y_pred_test))
    print("Confusion Matrix:\n", confusion_matrix(y_test_split, y_pred_test))

    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

    with writer.as_default():
        tf.summary.scalar("Accuracy", acc, step=0)

# Predict Props
if not X_pred.empty:
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}. Train it first.")

    print("Predicting...")
    model = joblib.load(MODEL_PATH)

    for col in model.feature_names_in_:
        if col not in X_pred.columns:
            X_pred[col] = missing_value_marker
    X_pred = X_pred[model.feature_names_in_]

    preds = model.predict(X_pred)
    probs = model.predict_proba(X_pred)[:, 1]

    predictions_df = players_pred.copy()
    predictions_df["RF_Prediction"] = preds
    predictions_df["RF_Confidence"] = probs
    predictions_df["LLM_Prediction"] = None
    predictions_df["LLM_Justification"] = None
    predictions_df["Actual_Result"] = None
    predictions_df["Reflection"] = None

    predictions_df = predictions_df.drop_duplicates(subset=["Player_hitter", "Prop Type", "Prop Value"])
    predictions_df.to_csv(PREDICTIONS_PATH, index=False)
    print(f"Predictions saved to {PREDICTIONS_PATH}")

    top_picks = predictions_df.sort_values("RF_Confidence", ascending=False).head(10)
    top_picks.to_csv(TOP_PICKS_PATH, index=False)
    print(f"Top picks saved to {TOP_PICKS_PATH}")

    with writer.as_default():
        tf.summary.scalar("Predictions Made", len(predictions_df), step=0)

print("✅ MLB Machine Learning script finished.")

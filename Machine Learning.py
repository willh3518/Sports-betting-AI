import pandas as pd
import numpy as np
import tensorflow as tf
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import os

# 📌 STEP 1: Load Processed Data
file_path = "../Sports-betting-AI/Prop_Data_CSV/processed_data.csv"  # Adjust if needed
data = pd.read_csv(file_path)

# 📌 STEP 2: Check if "Hit" column exists
if "Hit" not in data.columns:
    print("⚠️ 'Hit' column missing. Assuming this is a prediction day.")
    data["Hit"] = np.nan  # Create an empty column for later

# 📌 STEP 3: Define the expected features (based on your trained data)
expected_features = [
    # TEAM + OPPONENT
    'Team', 'Opposing Team', 'Opponent Defensive Rating', 'Home',

    # PROP TYPES (One-Hot Encoded)
    'Prop Type_3-pt attempted',
    'Prop Type_3-pt made',
    'Prop Type_assists',
    'Prop Type_blks+stls',
    'Prop Type_blocked shots',
    'Prop Type_defensive rebounds',
    'Prop Type_fg attempted',
    'Prop Type_fg made',
    'Prop Type_free throws made',
    'Prop Type_offensive rebounds',
    'Prop Type_points',
    'Prop Type_pts+asts',
    'Prop Type_pts+rebs',
    'Prop Type_pts+rebs+asts',
    'Prop Type_rebounds',
    'Prop Type_rebs+asts',
    'Prop Type_steals',
    'Prop Type_turnovers',

    # PROP VALUE
    'Prop Value',

    # SEASON / LAST 5 / LAST 10 / H2H STATS (add your full list here)
    'Season Hit %', 'Last 10 Hit Percentage',
    'GP (Season Stats)', 'PPG (Season Stats)', 'RPG (Season Stats)',
    'APG (Season Stats)', 'SPG (Season Stats)', 'BPG (Season Stats)',
    'FGM (Season Stats)', 'FGA (Season Stats)', '3PM (Season Stats)',
    '3PA (Season Stats)', 'FTM (Season Stats)', 'FTA (Season Stats)',
    'OREB (Season Stats)', 'DREB (Season Stats)', 'TPG (Season Stats)',
    # Add the rest of your stats columns here!
]

# 📌 STEP 4: Ensure Consistent Features for Training/Prediction
missing_value_marker = -999

for feature in expected_features:
    if feature not in data.columns:
        data[feature] = 0  # or missing_value_marker for numerical features

# Enforce column order to match the trained model
# We'll also keep Player, Prop Value, and Hit for later (not as model features)
extra_columns = [col for col in ['Player', 'Hit'] if col in data.columns]
data = data[expected_features + extra_columns]

# 📌 STEP 5: Separate Features and Target Variable
X = data[expected_features]  # Only model features
y = data["Hit"] if "Hit" in data.columns else pd.Series([np.nan] * len(data))

# 📌 STEP 6: Handle Missing Target Values
X_train = X[~y.isna()]
y_train = y[~y.isna()]
X_pred = X[y.isna()]  # Data where we need predictions
players_pred = data.loc[y.isna(), ["Player", "Prop Value"]] if "Player" in data.columns else pd.DataFrame()

# 📌 STEP 7: Setup TensorBoard Logging
log_dir = "logs/"
writer = tf.summary.create_file_writer(log_dir)
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

# 📌 STEP 8: Train the Model (if we have past labeled data)
if not X_train.empty:
    X_train_split, X_test_split, y_train_split, y_test_split = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_split, y_train_split)

    y_pred_test = model.predict(X_test_split)
    acc = accuracy_score(y_test_split, y_pred_test)
    print(f"✅ Model Trained. Accuracy on test set: {acc:.2f}")

    # Log accuracy to TensorBoard
    with writer.as_default():
        tf.summary.scalar("Accuracy", acc, step=0)

    joblib.dump(model, "model.pkl")
    print("✅ Model saved as 'model.pkl'.")

else:
    print("⚠️ No past outcomes available to train the model. Upload processed_data.csv with 'Hit' column filled.")

# 📌 STEP 9: Make Predictions for Today's Props
if not X_pred.empty:
    # 9a) Ensure we have a trained model
    if not os.path.exists("model.pkl"):
        raise FileNotFoundError(
            "❌ No trained model found. Train the model first by uploading processed_data.csv with 'Hit' column."
        )

    # 9b) Load model
    model = joblib.load("model.pkl")

    # 9c) Reorder columns exactly as during training
    X_pred = X_pred[model.feature_names_in_]

    # 9d) Predict and get probabilities
    predictions = model.predict(X_pred)
    probabilities = model.predict_proba(X_pred)[:, 1]

    # 9e) Recover the “Prop Type” text from one-hot columns
    prop_type_columns = [col for col in expected_features if col.startswith("Prop Type")]
    prop_types = X_pred[prop_type_columns].idxmax(axis=1).str.replace("Prop Type_", "")

    # 9f) Assemble output DataFrame
    predictions_df = players_pred.copy()
    predictions_df["Prop Type"] = prop_types
    predictions_df["Prediction"] = predictions
    predictions_df["Confidence Score"] = probabilities

    # 9g) De-duplicate exact repeats
    predictions_df = predictions_df.drop_duplicates(
        subset=["Player", "Prop Value", "Prop Type"],
        keep="first"
    )

    # 9h) Filter out any rows where Prediction == missing_value_marker
    predictions_df = predictions_df[predictions_df["Prediction"] != missing_value_marker]

    # 9i) Write to CSV files
    predictions_df.to_csv("predictions.csv", index=False)
    print("✅ Predictions saved as 'predictions.csv'.")

    top5_rf = predictions_df.sort_values("Confidence Score", ascending=False).head(5)
    top5_rf.to_csv("top5_picks_rf.csv", index=False)
    print("✅ Top 5 RF picks saved as 'top5_picks_rf.csv'.")

    # 9j) Log to TensorBoard
    with writer.as_default():
        tf.summary.scalar("Predictions Made", len(predictions_df), step=0)

else:
    print("⚠️ No new props to predict today.")

import pandas as pd
import os

# 👉 Step 1: Load the latest processed data (with actual outcomes)
processed_data = pd.read_csv("../Sports-betting-AI/Prop_Data_CSV/processed_data.csv")

# 👉 Step 2: Load the model's predictions
predictions = pd.read_csv("predictions.csv")

# 👉 Step 3: Ensure uniqueness by dropping duplicates (just in case)
processed_data_unique = processed_data.drop_duplicates(subset=['Player', 'Prop Value'])
predictions_unique = predictions.drop_duplicates(subset=['Player', 'Prop Value'])

# 👉 Step 4: Merge predictions with actual outcomes on Player and Prop Value
merged = predictions_unique.merge(
    processed_data_unique[['Player', 'Prop Value', 'Hit']],
    on=['Player', 'Prop Value'],
    how='left'
)

# 👉 Step 5: Drop any rows where 'Hit' is missing (no results available yet)
merged = merged.dropna(subset=['Hit'])

# 👉 Step 6: Calculate Accuracy
correct_predictions = (merged['Prediction'] == merged['Hit']).sum()
total_predictions = len(merged)
accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0

# 👉 Step 7: Prompt user for date (or use today's date)
user_date = input("Enter the date for this log (YYYY-MM-DD), or press Enter to use today: ").strip()

if not user_date:
    log_date = pd.Timestamp.today().strftime('%Y-%m-%d')
else:
    log_date = user_date

# 👉 Step 8: Prepare performance log entry
performance_log = pd.DataFrame([{
    'Date': log_date,
    'Total Predictions': total_predictions,
    'Correct Predictions': correct_predictions,
    'Accuracy (%)': round(accuracy * 100, 2)
}])

print("\n🔹 Performance Log:")
print(performance_log)

# 👉 Step 9: Append to tracking CSV (create file if it doesn't exist)
tracking_file = "model_tracking.csv"
file_exists = os.path.exists(tracking_file)

performance_log.to_csv(tracking_file, mode='a', index=False, header=not file_exists)

print(f"\n✅ Model Accuracy: {accuracy:.2%} ({correct_predictions}/{total_predictions} correct)")
print(f"✅ Logged in {tracking_file}")

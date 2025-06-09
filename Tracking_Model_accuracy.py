import pandas as pd
import os

# 👉 Step 1: Load the latest processed data (with actual outcomes)
processed_data = pd.read_csv("../Sports-betting-AI/Prop_Data_CSV/processed_data.csv")

# 👉 Step 2: Load the random forest model's predictions
predictions = pd.read_csv("predictions.csv")

# 👉 Step 3: Ensure uniqueness by dropping duplicates on Player & Prop Value
processed_unique = processed_data.drop_duplicates(subset=['Player', 'Prop Value'])
pred_unique      = predictions.drop_duplicates(subset=['Player', 'Prop Value'])

# 👉 Step 4: Merge predictions with actual outcomes
merged = pred_unique.merge(
    processed_unique[['Player', 'Prop Value', 'Hit']],
    on=['Player', 'Prop Value'],
    how='left'
).dropna(subset=['Hit'])

# 👉 Step 5: Calculate metrics for the random forest model
total_preds   = len(merged)
correct_preds = (merged['Prediction'] == merged['Hit']).sum()
accuracy      = correct_preds / total_preds if total_preds > 0 else 0

# 👉 Step 6: Prompt user for date (or use today's date)
user_date = input("Enter the date for this log (YYYY-MM-DD), or press Enter to use today: ").strip()
log_date  = user_date if user_date else pd.Timestamp.today().strftime('%Y-%m-%d')

# 👉 Step 7: Prepare performance log entry
performance_log = pd.DataFrame([{
    'Date': log_date,
    'Total Predictions': total_preds,
    'Correct Predictions': correct_preds,
    'Accuracy (%)': round(accuracy * 100, 2),
}])

print("\n🔹 Performance Log:")
print(performance_log)

# 👉 Step 8: Append to tracking CSV (create if needed)
tracking_file = "model_tracking.csv"
file_exists   = os.path.exists(tracking_file)

csv_str = performance_log.to_csv(index=False, header=not file_exists)

with open(tracking_file, 'a') as f:
    if file_exists:
        f.write('\n')
    f.write(csv_str)

# 👉 Step 9: Summary output
print(f"\n✅ Random Forest Model: {accuracy:.2%} ({correct_preds}/{total_preds})")
print(f"✅ Logged to {tracking_file}")

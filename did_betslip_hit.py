import pandas as pd
import json
import os

RESULTS_DIR = "MLB_Results"

def load_predictions(pred_csv_path):
    df = pd.read_csv(pred_csv_path)
    df['Player'] = df['Player'].astype(str).str.strip().str.lower()
    df['Prop Type'] = df['Prop Type'].astype(str).str.strip().str.lower()
    return df

def score_betslips(betslips_path, pred_df):
    with open(betslips_path, 'r') as f:
        slips = json.load(f)

    for slip in slips:
        all_legs_hit = True
        for leg in slip.get('legs', []):
            player = str(leg['Player']).strip().lower()
            prop = str(leg['Prop Type']).strip().lower()
            pick = leg.get('Pick', leg.get('Prediction', 'Over')).strip().capitalize()

            # Find the prediction row
            match = pred_df[(pred_df['Player'] == player) & (pred_df['Prop Type'] == prop)]
            if match.empty:
                all_legs_hit = False
                continue
            actual_result = str(match.iloc[0]['Actual_Result']).strip().capitalize()
            if actual_result != pick:
                all_legs_hit = False
        slip['hit'] = all_legs_hit

    with open(betslips_path, 'w') as f:
        json.dump(slips, f, indent=2)
    print(f"Scored {len(slips)} slips in {betslips_path}")

def main():
    date = input("Enter date to score (YYYY-MM-DD): ").strip()
    betslips_path = os.path.join(RESULTS_DIR, f"{date}_generated_betslips.json")
    pred_csv_path = os.path.join(RESULTS_DIR, f"{date}_mlb_predictions.csv")
    if not os.path.exists(betslips_path):
        print(f"Betslips file not found: {betslips_path}")
        return
    if not os.path.exists(pred_csv_path):
        print(f"Predictions file not found: {pred_csv_path}")
        return

    pred_df = load_predictions(pred_csv_path)
    score_betslips(betslips_path, pred_df)

if __name__ == "__main__":
    main()
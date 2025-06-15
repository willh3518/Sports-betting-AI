import glob
import os
import sys
import math
import json
import pandas as pd
from flask import Flask, render_template, jsonify

app = Flask(__name__)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
MLB_RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'MLB_Results')

def find_latest_predictions_file():
    pattern = os.path.join(MLB_RESULTS_DIR, "*_mlb_predictions.csv")
    files = glob.glob(pattern)
    return max(files) if files else None

def _sanitize_records(records):
    """
    Replace any NaN/Inf in a list of dicts with None so JSON stays valid.
    """
    clean_list = []
    for rec in records:
        clean = {}
        for k, v in rec.items():
            if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
                clean[k] = None
            else:
                clean[k] = v
        clean_list.append(clean)
    return clean_list

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
def dashboard_data():
    # ── Load accuracy summary CSV ───────────────────────────────
    acc_path = os.path.join(MLB_RESULTS_DIR, "MLB_Prop_Accuracy.csv")
    if not os.path.exists(acc_path):
        return jsonify(success=False, error="MLB_Prop_Accuracy.csv not found"), 500
    acc_df = pd.read_csv(acc_path)

    # ── 1) Historical performance (one row per date) ────────────
    history = [
        {
            'date': row['Date'],
            'total': int(row['Total_Predictions']),
            'rf_accuracy': float(row['RF_Accuracy']),
            'llm_accuracy': float(row['LLM_Accuracy']),
            'agreement_accuracy': float(row['Agreement_Accuracy'])
        }
        for _, row in acc_df.iterrows()
    ]

    # ── 2) Overall metrics from the latest date ─────────────────
    latest_acc = acc_df.iloc[-1]
    latest_date = latest_acc['Date']
    overall = {
        'total': int(latest_acc['Total_Predictions']),
        'rf_accuracy': float(latest_acc['RF_Accuracy']),
        'llm_accuracy': float(latest_acc['LLM_Accuracy']),
        'agreement_accuracy': float(latest_acc['Agreement_Accuracy']),
        'agreement_count': int(latest_acc['Agreement_Count'])
    }

    # ── 3) Prop-Type summary from accuracy CSV ──────────────────
    prop_types = {}
    for col in acc_df.columns:
        if col.endswith('_Count') and col != 'Total_Predictions':
            prop = col[:-6]  # trim "_Count"
            if prop == 'Agreement':
                continue
            prop_types[prop] = {
                'count': int(latest_acc[f'{prop}_Count']),
                'rf_accuracy': float(latest_acc.get(f'{prop}_RF_Accuracy', 0)),
                'llm_accuracy': float(latest_acc.get(f'{prop}_LLM_Accuracy', 0))
            }

    # ── 4) Recent High-Confidence Predictions (from ALL top-picks files) ──
    recent_predictions = []
    top_pattern = os.path.join(MLB_RESULTS_DIR, "*_mlb_top_picks.csv")
    top_files = sorted(glob.glob(top_pattern))
    if top_files:
        # read and tag every file with its date
        df_list = []
        for fpath in top_files:
            try:
                tmp = pd.read_csv(fpath)
            except Exception as e:
                app.logger.warning(f"Skipping top-picks file {fpath}: {e}")
                continue

            # derive date from filename and add as a column so we can sort/display
            date_tag = os.path.basename(fpath).split('_')[0]  # e.g. "2025-06-13"
            tmp['Date'] = date_tag
            df_list.append(tmp)

        if df_list:
            all_tops = pd.concat(df_list, ignore_index=True)

            # drop any rows without a real result
            if 'Actual_Result' in all_tops.columns:
                all_tops = all_tops[all_tops['Actual_Result'].notnull()]
            else:
                all_tops['Actual_Result'] = None

            # keep only the columns your UI expects
            desired = [
                'Date',
                'Player', 'Prop Type', 'Prop Value', 'Start Time',
                'RF_Prediction', 'RF_Confidence',
                'Model_Type',
                'LLM_Prediction', 'LLM_RF_Agreement', 'LLM_Confidence', 'LLM_Justification',
                'Actual_Stat', 'Actual_Result', 'Reflection'
            ]
            available = [c for c in desired if c in all_tops.columns]
            all_tops = all_tops[available]

            # sort by Date (ascending) then take the last 20 entries
            all_tops = all_tops.sort_values('Date').tail(20)

            recent_predictions = _sanitize_records(all_tops.to_dict(orient='records'))

    # ── 5) Today's Betslips ───────────────────────────────────────
    betslips = []
    if top_files:
        try:
            slips = pd.read_csv(top_files[-1]).to_dict(orient='records')
            betslips = _sanitize_records(slips)
        except:
            pass

    return jsonify(success=True, data={
        'latest_date': latest_date,
        'overall': overall,
        'prop_types': prop_types,
        'recent_predictions': recent_predictions,
        'historical_data': history,
        'betslips': betslips
    })\

@app.route('/api/mlb-insights')
def mlb_insights():
    INSIGHTS_JSON = os.path.join(MLB_RESULTS_DIR, "mlb_insights_db.json")
    try:
        with open(INSIGHTS_JSON, 'r') as f:
            db = json.load(f)
        return jsonify(success=True, insights=db.get('prop_types', {}))
    except Exception as e:
        app.logger.error(f"Error loading insights: {e}")
        return jsonify(success=False, error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
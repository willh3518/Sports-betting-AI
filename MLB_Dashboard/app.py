# MLB_Dashboard/app.py
from flask import Flask, render_template, jsonify
import pandas as pd
import os
import glob
import math
import re
from datetime import datetime, timedelta
import sys
import json

app = Flask(__name__)

# Add parent directory to path to access project files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define paths relative to the project root
PROJECT_ROOT       = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MLB_RESULTS_DIR    = os.path.join(PROJECT_ROOT, 'MLB_Results')
PROP_ACCURACY_FILE = os.path.join(MLB_RESULTS_DIR, 'MLB_Prop_Accuracy.csv')


def _safe_int(v):
    try:
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return None
        return int(v)
    except Exception:
        return None


def _safe_float(v):
    try:
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return None
        return float(v)
    except Exception:
        return None

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/mlb-insights')
def mlb_insights():
    """
    Return just the 'prop_types' section of your mlb_insights_db.json
    so the front end can populate the dropdown.
    """
    INSIGHTS_FILE = os.path.join(MLB_RESULTS_DIR, 'mlb_insights_db.json')
    try:
        with open(INSIGHTS_FILE, 'r') as f:
            data = json.load(f)
        prop_types = data.get('prop_types', {})
        return jsonify(success=True, insights=prop_types)
    except Exception as e:
        app.logger.error(f"Error loading MLB insights: {e}")
        return jsonify(success=False, error=str(e)), 500

@app.route('/api/dashboard-data')
def dashboard_data():
    try:
        # ── Load accuracy CSV ───────────────────────────────
        if not os.path.exists(PROP_ACCURACY_FILE):
            return jsonify(success=False,
                           error=f'Accuracy file not found: {PROP_ACCURACY_FILE}')

        acc_df = pd.read_csv(PROP_ACCURACY_FILE)
        acc_df['Date'] = pd.to_datetime(acc_df['Date'])
        acc_df = acc_df.sort_values('Date', ascending=False)

        # Always use the most recent completed day < today for "Last Night's Performance"
        today = datetime.now().date()
        completed_days = acc_df[acc_df['Date'].dt.date < today]
        if not completed_days.empty:
            row = completed_days.iloc[0]
        else:
            row = acc_df.iloc[0]  # fallback: latest row if all dates are in the future (shouldn't happen)

        # Build "latest" payload (the "last night's" box on dashboard)
        latest = {
            'latest_date': row['Date'].strftime('%Y-%m-%d'),
            'overall': {
                'total':              _safe_int(row.get('Total_Predictions')),
                'rf_accuracy':        _safe_float(row.get('RF_Accuracy')),
                'llm_accuracy':       _safe_float(row.get('LLM_Accuracy')),
                'agreement_accuracy': _safe_float(row.get('Agreement_Accuracy')),
                'agreement_count':    _safe_int(row.get('Agreement_Count')),
            },
            'prop_types': {},
            'historical_data': []
        }

        # Fill prop_types (accuracy breakdown by prop)
        prop_list = [
            'Hits+Runs+RBIs','Hitter_Strikeouts','Total_Bases',
            'Hitter_Fantasy_Score','Hits','Walks','Runs',
            'Pitcher_Strikeouts','Pitches_Thrown','Pitching_Outs',
            'Pitcher_Fantasy_Score','Earned_Runs_Allowed'
        ]
        for p in prop_list:
            cnt = row.get(f'{p}_Count')
            if _safe_int(cnt) and _safe_int(cnt) > 0:
                latest['prop_types'][p] = {
                    'count':        _safe_int(cnt),
                    'rf_accuracy':  _safe_float(row.get(f'{p}_RF_Accuracy')),
                    'llm_accuracy': _safe_float(row.get(f'{p}_LLM_Accuracy')),
                }

        # Last 30 days of history for the bar chart
        for _, r in acc_df.head(30).iterrows():
            latest['historical_data'].append({
                'date':               r['Date'].strftime('%Y-%m-%d'),
                'total':              _safe_int(r.get('Total_Predictions')),
                'rf_accuracy':        _safe_float(r.get('RF_Accuracy')),
                'llm_accuracy':       _safe_float(r.get('LLM_Accuracy')),
                'agreement_accuracy': _safe_float(r.get('Agreement_Accuracy')),
            })

        # ── Load today's generated betslips ───────────────────────
        bets_file = os.path.join(
            MLB_RESULTS_DIR,
            f"{today}_generated_betslips.json"
        )
        if os.path.exists(bets_file):
            try:
                with open(bets_file, 'r') as bf:
                    latest['betslips'] = json.load(bf)
            except Exception as e:
                app.logger.error(f"Error loading betslips {bets_file}: {e}")
                latest['betslips'] = []
        else:
            latest['betslips'] = []

        # ── Gather all prior prediction files ─────────────────
        pred_files = glob.glob(os.path.join(MLB_RESULTS_DIR, "*_mlb_predictions.csv"))
        dfs = []
        for path in pred_files:
            m = re.match(r"(\d{4}-\d{2}-\d{2})_mlb_predictions\.csv$", os.path.basename(path))
            if not m:
                continue
            file_date = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            if file_date < today:
                try:
                    dfs.append(pd.read_csv(path))
                except Exception:
                    pass

        # ── Filter & sample recent high confidence predictions ──
        preds = []
        if dfs:
            all_preds = pd.concat(dfs, ignore_index=True)
            completed = all_preds[all_preds['Actual_Result'].notna()].copy()
            completed['RF_Confidence']  = pd.to_numeric(completed['RF_Confidence'],  errors='coerce')
            completed['LLM_Confidence'] = completed['LLM_Confidence'].astype(str).str.lower()

            ap = completed[
                (completed['RF_Confidence'] >= 0.75) &
                (completed['LLM_RF_Agreement'] == True) &
                (completed['LLM_Confidence'].isin(['medium', 'high']))
            ]
            if not ap.empty:
                preds = (
                    ap[[
                        'Player', 'Prop Type', 'Prop Value',
                        'RF_Prediction', 'RF_Confidence', 'Actual_Result'
                    ]]
                    .rename(columns={
                        'RF_Prediction': 'Prediction',
                        'RF_Confidence': 'Confidence',
                        'Actual_Result': 'Result'
                    })
                    .to_dict(orient='records')
                )

        latest['recent_predictions'] = preds
        total = len(preds)
        correct = sum(1 for p in preds if p.get('Result') is True)
        latest['recent_summary'] = {'correct': correct, 'total': total}

        # bump `latest_date` to newest prediction-file date (if any, for info/display)
        pred_dates = []
        for path in pred_files:
            m = re.match(r"(\d{4}-\d{2}-\d{2})_mlb_predictions\.csv$", os.path.basename(path))
            if m:
                try:
                    pred_dates.append(datetime.strptime(m.group(1), "%Y-%m-%d").date())
                except:
                    pass
        if pred_dates:
            latest['latest_date'] = max(pred_dates).strftime("%Y-%m-%d")

        return jsonify(success=True, data=latest)

    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    if not os.path.exists(MLB_RESULTS_DIR):
        print(f"Warning: MLB_Results directory not found at {MLB_RESULTS_DIR}")
    elif not os.path.exists(PROP_ACCURACY_FILE):
        print(f"Warning: MLB_Prop_Accuracy.csv not found at {PROP_ACCURACY_FILE}")
    else:
        print("Found MLB_Prop_Accuracy.csv with data")

    app.run(debug=True, port=5001)

# MLB_Dashboard/app.py
from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import glob
import math
from datetime import datetime, timedelta
import sys

app = Flask(__name__)

# Add parent directory to path to access project files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define paths relative to the project root
PROJECT_ROOT      = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MLB_RESULTS_DIR   = os.path.join(PROJECT_ROOT, 'MLB_Results')
PROP_ACCURACY_FILE = os.path.join(MLB_RESULTS_DIR, 'MLB_Prop_Accuracy.csv')


def _safe_int(v):
    """Return int(v) or None if v is NaN or None."""
    try:
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return None
        return int(v)
    except Exception:
        return None

def _safe_float(v):
    """Return float(v) or None if v is NaN or None."""
    try:
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return None
        return float(v)
    except Exception:
        return None

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/dashboard-data')
def dashboard_data():
    try:
        # accuracy file must exist
        if not os.path.exists(PROP_ACCURACY_FILE):
            return jsonify(success=False,
                           error=f'Accuracy file not found: {PROP_ACCURACY_FILE}')

        # load and sort accuracy
        df = pd.read_csv(PROP_ACCURACY_FILE)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date', ascending=False)

        # pick yesterday or latest
        today     = datetime.now().date()
        yesterday = today - timedelta(days=1)
        ydf       = df[df['Date'].dt.date == yesterday]
        row       = ydf.iloc[0] if not ydf.empty else df.iloc[0]

        # build payload
        latest = {
            'latest_date': row['Date'].strftime('%Y-%m-%d'),
            'overall': {
                'total':            _safe_int(row.get('Total_Predictions')),
                'rf_accuracy':      _safe_float(row.get('RF_Accuracy')),
                'llm_accuracy':     _safe_float(row.get('LLM_Accuracy')),
                'agreement_accuracy':_safe_float(row.get('Agreement_Accuracy')),
                'agreement_count':  _safe_int(row.get('Agreement_Count'))
            },
            'prop_types': {},
            'historical_data': []
        }

        # prop types
        props = [
            'Hits+Runs+RBIs','Hitter_Strikeouts','Total_Bases',
            'Hitter_Fantasy_Score','Hits','Walks','Runs',
            'Pitcher_Strikeouts','Pitches_Thrown','Pitching_Outs',
            'Pitcher_Fantasy_Score','Earned_Runs_Allowed'
        ]
        for p in props:
            cnt = row.get(f'{p}_Count')
            if _safe_int(cnt) and _safe_int(cnt) > 0:
                latest['prop_types'][p] = {
                    'count':       _safe_int(cnt),
                    'rf_accuracy': _safe_float(row.get(f'{p}_RF_Accuracy')),
                    'llm_accuracy':_safe_float(row.get(f'{p}_LLM_Accuracy'))
                }

        # last 30 days history
        for _, r in df.head(30).iterrows():
            latest['historical_data'].append({
                'date':              r['Date'].strftime('%Y-%m-%d'),
                'total':             _safe_int(r.get('Total_Predictions')),
                'rf_accuracy':       _safe_float(r.get('RF_Accuracy')),
                'llm_accuracy':      _safe_float(r.get('LLM_Accuracy')),
                'agreement_accuracy':_safe_float(r.get('Agreement_Accuracy'))
            })

        # high-confidence correct picks from newest predictions file
        picks = []
        pred_files = glob.glob(os.path.join(MLB_RESULTS_DIR, '*_mlb_predictions.csv'))
        if pred_files:
            latest_file = sorted(pred_files, reverse=True)[0]
            pdf = pd.read_csv(latest_file)
            required = {'RF_Prediction','RF_Confidence','Actual_Result'}
            if required.issubset(pdf.columns):
                pdf = pdf[pdf['Actual_Result'].notna()]
                pdf['RF_Correct'] = (
                    ((pdf['RF_Prediction']==1)&(pdf['Actual_Result']=='Over')) |
                    ((pdf['RF_Prediction']==0)&(pdf['Actual_Result']=='Under'))
                )
                hc = pdf[(pdf['RF_Correct']) & (pdf['RF_Confidence']>=0.8)]
                top = hc.sort_values('RF_Confidence', ascending=False).head(10)
                top = top.where(pd.notnull(top), None)
                cols = [
                    'Player','Prop Type','Prop Value',
                    'RF_Prediction','RF_Confidence',
                    'Actual_Stat','Actual_Result','RF_Correct'
                ]
                picks = top[cols].to_dict(orient='records')

        latest['recent_predictions'] = picks

        # ── override latest_date to match the newest predictions file date ──
        pred_dates = []
        for path in pred_files:
            fn = os.path.basename(path)
            try:
                dt = datetime.strptime(fn.split('_')[0], "%Y-%m-%d").date()
                pred_dates.append(dt)
            except:
                continue
        if pred_dates:
            latest_pred_date = max(pred_dates)
            latest['latest_date'] = latest_pred_date.strftime("%Y-%m-%d")
        # ──────────────────────────────────────────────────────────────────

        return jsonify(success=True, data=latest)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify(success=False, error=str(e))

if __name__ == '__main__':
    if not os.path.exists(MLB_RESULTS_DIR):
        print(f"Warning: MLB_Results directory not found at {MLB_RESULTS_DIR}")
    elif not os.path.exists(PROP_ACCURACY_FILE):
        print(f"Warning: MLB_Prop_Accuracy.csv not found at {PROP_ACCURACY_FILE}")
    else:
        print("Found MLB_Prop_Accuracy.csv with data")
    app.run(debug=True, port=5001)

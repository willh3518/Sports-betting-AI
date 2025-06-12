# MLB_Dashboard/app.py
from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import glob
import json
from datetime import datetime, timedelta
import sys

app = Flask(__name__)

# Add parent directory to path to access project files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define paths relative to the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MLB_RESULTS_DIR = os.path.join(PROJECT_ROOT, 'MLB_Results')
PROP_ACCURACY_FILE = os.path.join(MLB_RESULTS_DIR, 'MLB_Prop_Accuracy.csv')


@app.route('/')
def dashboard():
    """Main dashboard view"""
    return render_template('dashboard.html')


@app.route('/api/dashboard-data')
def dashboard_data():
    """API endpoint to get all dashboard data in one request"""
    try:
        # Check if the accuracy file exists
        if not os.path.exists(PROP_ACCURACY_FILE):
            return jsonify({
                'success': False,
                'error': f'Accuracy file not found: {PROP_ACCURACY_FILE}'
            })

        # Load the accuracy data
        accuracy_df = pd.read_csv(PROP_ACCURACY_FILE)

        # Sort by date (newest first)
        accuracy_df['Date'] = pd.to_datetime(accuracy_df['Date'])
        accuracy_df = accuracy_df.sort_values('Date', ascending=False)

        # Get the most recent data
        latest_data = accuracy_df.iloc[0].to_dict()

        # Format the response data
        response_data = {
            'latest_date': latest_data['Date'].strftime('%Y-%m-%d'),
            'overall': {
                'total': int(latest_data['Total_Predictions']),
                'rf_accuracy': float(latest_data['RF_Accuracy']),
                'llm_accuracy': float(latest_data['LLM_Accuracy']),
                'agreement_accuracy': float(latest_data['Agreement_Accuracy']),
                'agreement_count': int(latest_data['Agreement_Count'])
            },
            'prop_types': {},
            'historical_data': []
        }

        # Extract prop type data
        prop_types = [
            'Hits+Runs+RBIs', 'Hitter_Strikeouts', 'Total_Bases',
            'Hitter_Fantasy_Score', 'Hits', 'Walks', 'Runs',
            'Pitcher_Strikeouts', 'Pitches_Thrown', 'Pitching_Outs',
            'Pitcher_Fantasy_Score', 'Earned_Runs_Allowed'
        ]

        for prop_type in prop_types:
            count_key = f'{prop_type}_Count'
            rf_key = f'{prop_type}_RF_Accuracy'
            llm_key = f'{prop_type}_LLM_Accuracy'

            if count_key in latest_data and rf_key in latest_data and llm_key in latest_data:
                count = latest_data[count_key]
                # Only include prop types with data
                if count > 0:
                    response_data['prop_types'][prop_type] = {
                        'count': int(count),
                        'rf_accuracy': float(latest_data[rf_key]),
                        'llm_accuracy': float(latest_data[llm_key])
                    }

        # Get historical data (last 30 days)
        for _, row in accuracy_df.head(30).iterrows():
            historical_data = {
                'date': row['Date'].strftime('%Y-%m-%d'),
                'total': int(row['Total_Predictions']),
                'rf_accuracy': float(row['RF_Accuracy']),
                'llm_accuracy': float(row['LLM_Accuracy']),
                'agreement_accuracy': float(row['Agreement_Accuracy'])
            }
            response_data['historical_data'].append(historical_data)

        # Get recent predictions (if available)
        recent_predictions = []
        prediction_files = glob.glob(os.path.join(MLB_RESULTS_DIR, "*_mlb_predictions.csv"))
        if prediction_files:
            # Sort by date (newest first)
            prediction_files.sort(reverse=True)
            recent_file = prediction_files[0]

            try:
                pred_df = pd.read_csv(recent_file)
                if 'RF_Prediction' in pred_df.columns and 'Actual_Result' in pred_df.columns:
                    # Filter to rows with actual results
                    pred_df = pred_df[pred_df['Actual_Result'].notna()]

                    # Calculate correctness
                    pred_df['RF_Correct'] = ((pred_df['RF_Prediction'] == 1) & (pred_df['Actual_Result'] == 'Over')) | \
                                            ((pred_df['RF_Prediction'] == 0) & (pred_df['Actual_Result'] == 'Under'))

                    # Sort by confidence and get top 10
                    top_preds = pred_df.sort_values('RF_Confidence', ascending=False).head(10)

                    # Convert to list of dicts
                    if not top_preds.empty:
                        recent_predictions = top_preds[['Player', 'Prop Type', 'Prop Value',
                                                        'RF_Prediction', 'RF_Confidence',
                                                        'Actual_Stat', 'Actual_Result', 'RF_Correct']].to_dict(
                            orient='records')
            except Exception as e:
                print(f"Error processing prediction file: {e}")

        response_data['recent_predictions'] = recent_predictions

        return jsonify({
            'success': True,
            'data': response_data
        })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': str(e)
        })


if __name__ == '__main__':
    # Check if MLB_Results directory and accuracy file exist
    if not os.path.exists(MLB_RESULTS_DIR):
        print(f"Warning: MLB_Results directory not found at {MLB_RESULTS_DIR}")
    elif not os.path.exists(PROP_ACCURACY_FILE):
        print(f"Warning: MLB_Prop_Accuracy.csv not found at {PROP_ACCURACY_FILE}")
    else:
        print(f"Found MLB_Prop_Accuracy.csv with data")

    app.run(debug=True, port=5001)
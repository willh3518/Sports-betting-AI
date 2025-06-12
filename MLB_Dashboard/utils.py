# MLB_Dashboard/utils.py
import pandas as pd
import os
import glob
from datetime import datetime
import sys

# Add parent directory to path to access project modules if needed
sys.path.append('..')


def load_model_tracking():
    """Load model tracking data from CSV file"""
    tracking_file = "../model_tracking.csv"  # Path relative to MLB_Dashboard directory
    if os.path.exists(tracking_file):
        df = pd.read_csv(tracking_file)
        return df.to_dict(orient='records')
    return None


def load_prediction_results(date_str=None):
    """Load prediction results from CSV file"""
    results_dir = "../MLB_Results"  # Path relative to MLB_Dashboard directory
    if not os.path.exists(results_dir):
        return None

    if date_str:
        # Load specific date
        file_path = os.path.join(results_dir, f"{date_str}_mlb_predictions.csv")
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
    else:
        # Load most recent file
        prediction_files = glob.glob(os.path.join(results_dir, "*_mlb_predictions.csv"))
        if prediction_files:
            # Sort by date (newest first)
            prediction_files.sort(reverse=True)
            return pd.read_csv(prediction_files[0])

    return None


def calculate_metrics(df):
    """Calculate metrics from prediction results"""
    metrics = {
        'file_date': None,
        'overall': {'total': 0, 'correct': 0, 'accuracy': 0},
        'by_prop_type': {},
        'by_model_type': {},
        'recent_results': []
    }

    if df is None or df.empty:
        return metrics

    # Extract date from filename if available
    if 'file_path' in df.attrs:
        metrics['file_date'] = os.path.basename(df.attrs['file_path']).split('_')[0]

    # Calculate overall metrics
    if 'RF_Prediction' in df.columns and 'Actual_Result' in df.columns:
        df['RF_Correct'] = ((df['RF_Prediction'] == 1) & (df['Actual_Result'] == 'Over')) | \
                           ((df['RF_Prediction'] == 0) & (df['Actual_Result'] == 'Under'))

        total_with_results = df['Actual_Result'].notna().sum()
        correct_predictions = df['RF_Correct'].sum()
        accuracy = correct_predictions / total_with_results if total_with_results > 0 else 0

        metrics['overall'] = {
            'total': int(total_with_results),
            'correct': int(correct_predictions),
            'accuracy': float(accuracy)
        }

        # Calculate metrics by prop type
        for prop_type, group in df.groupby('Prop Type'):
            total = group['Actual_Result'].notna().sum()
            correct = group['RF_Correct'].sum()
            accuracy = correct / total if total > 0 else 0

            metrics['by_prop_type'][prop_type] = {
                'total': int(total),
                'correct': int(correct),
                'accuracy': float(accuracy)
            }

        # Calculate metrics by model type
        if 'Model_Type' in df.columns:
            for model_type, group in df.groupby('Model_Type'):
                total = group['Actual_Result'].notna().sum()
                correct = group['RF_Correct'].sum()
                accuracy = correct / total if total > 0 else 0

                metrics['by_model_type'][model_type] = {
                    'total': int(total),
                    'correct': int(correct),
                    'accuracy': float(accuracy)
                }

        # Get recent results
        recent_results = df[df['Actual_Result'].notna()].sort_values('RF_Confidence', ascending=False).head(10)
        if not recent_results.empty:
            metrics['recent_results'] = recent_results[['Player', 'Prop Type', 'Prop Value',
                                                        'RF_Prediction', 'RF_Confidence',
                                                        'Actual_Stat', 'Actual_Result']].to_dict(orient='records')

    return metrics
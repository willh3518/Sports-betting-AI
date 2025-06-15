import pandas as pd
import json
import os
import logging
from datetime import datetime
import subprocess
import re
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mlb_reflection.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Config
RESULTS_DIR = "MLB_Results"
INSIGHTS_DB_PATH = os.path.join(RESULTS_DIR, "mlb_insights_db.json")
ACCURACY_CSV_PATH = os.path.join(RESULTS_DIR, "MLB_Prop_Accuracy.csv")

def load_predictions_with_results(date):
    """Load predictions with actual results for a specific date"""
    file_path = os.path.join(RESULTS_DIR, f"{date}_mlb_predictions.csv")

    try:
        df = pd.read_csv(file_path)
        logger.info(f"Loaded {len(df)} predictions from {file_path}")

        # Check if actual results are available
        if 'Actual_Result' not in df.columns or df['Actual_Result'].isna().all():
            logger.error(f"No actual results found in {file_path}")
            return None

        # Filter to only include predictions with actual results
        completed_df = df[df['Actual_Result'].notna()].copy()
        logger.info(f"Found {len(completed_df)} completed predictions with actual results")

        return completed_df
    except FileNotFoundError:
        logger.error(f"Predictions file not found at {file_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading predictions: {e}")
        return None

def group_by_prop_type(df):
    """Group predictions by prop type"""
    if 'Prop Type' not in df.columns:
        logger.error("No 'Prop Type' column found in predictions")
        return {}

    prop_groups = {}
    for prop_type in df['Prop Type'].unique():
        prop_df = df[df['Prop Type'] == prop_type].copy()
        prop_groups[prop_type] = prop_df
        logger.info(f"Found {len(prop_df)} predictions for prop type: {prop_type}")

    return prop_groups

def build_reflection_prompt(prop_type, prop_df):
    """Build a prompt for the LLM to reflect on predictions for a specific prop type"""
    correct_count = sum((prop_df['LLM_Prediction'] == prop_df['Actual_Result']).astype(int))
    total_count = len(prop_df)
    accuracy = correct_count / total_count if total_count > 0 else 0

    prompt = f"""<s>[INST] System: You are an AI system designed to reflect on and learn from MLB prop betting predictions. Your goal is to analyze what went right or wrong with predictions for {prop_type} props and identify patterns that can improve future predictions.

User: I need you to analyze {total_count} predictions for {prop_type} props. Your accuracy was {accuracy:.1%} ({correct_count}/{total_count} correct).

Here are the predictions:

"""

    # Add examples of both correct and incorrect predictions
    correct_examples = prop_df[prop_df['LLM_Prediction'] == prop_df['Actual_Result']].head(3)
    incorrect_examples = prop_df[prop_df['LLM_Prediction'] != prop_df['Actual_Result']].head(3)

    # Add correct examples
    prompt += "\n**CORRECT PREDICTIONS:**\n"
    for _, row in correct_examples.iterrows():
        player = row.get('Player', 'Unknown')
        prop_value = row.get('Prop Value', 'Unknown')
        prediction = row.get('LLM_Prediction', 'Unknown')
        justification = row.get('LLM_Justification', 'No justification provided')

        prompt += f"\nPlayer: {player}\n"
        prompt += f"Prop: {prop_type} {prop_value}\n"
        prompt += f"Prediction: {prediction}\n"
        prompt += f"Justification: {justification}\n"

        # Add key stats that were available for the prediction
        prompt += "Key Stats:\n"
        for col in row.index:
            if col not in ['Player', 'Prop Type', 'Prop Value', 'LLM_Prediction', 'LLM_Justification', 'Actual_Result',
                           'RF_Prediction', 'RF_Confidence']:
                if not pd.isna(row[col]) and str(row[col]) != 'nan':
                    prompt += f"- {col}: {row[col]}\n"

        prompt += "---\n"

    # Add incorrect examples
    prompt += "\n**INCORRECT PREDICTIONS:**\n"
    for _, row in incorrect_examples.iterrows():
        player = row.get('Player', 'Unknown')
        prop_value = row.get('Prop Value', 'Unknown')
        prediction = row.get('LLM_Prediction', 'Unknown')
        actual = row.get('Actual_Result', 'Unknown')
        justification = row.get('LLM_Justification', 'No justification provided')

        prompt += f"\nPlayer: {player}\n"
        prompt += f"Prop: {prop_type} {prop_value}\n"
        prompt += f"Prediction: {prediction} (Actual: {actual})\n"
        prompt += f"Justification: {justification}\n"

        # Add key stats that were available for the prediction
        prompt += "Key Stats:\n"
        for col in row.index:
            if col not in ['Player', 'Prop Type', 'Prop Value', 'LLM_Prediction', 'LLM_Justification', 'Actual_Result',
                           'RF_Prediction', 'RF_Confidence']:
                if not pd.isna(row[col]) and str(row[col]) != 'nan':
                    prompt += f"- {col}: {row[col]}\n"

        prompt += "---\n"

    prompt += f"""
Based on these examples and the overall performance for {prop_type} props, please provide:

1. **Pattern Analysis**: What patterns do you observe in correct vs. incorrect predictions?
2. **Key Factors**: Which statistics or factors appear most predictive for {prop_type} props?
3. **Flawed Logic**: What reasoning errors or biases appeared in incorrect predictions?
4. **Strongest Insight**: What is the single most valuable insight for improving future {prop_type} prop predictions?

Respond in this format:
PATTERN_ANALYSIS: [Your analysis of patterns in correct vs. incorrect predictions]
KEY_FACTORS: [The statistics or factors that appear most predictive]
FLAWED_LOGIC: [Common reasoning errors or biases in incorrect predictions]
STRONGEST_INSIGHT: [The single most valuable insight for improving future predictions]
[/INST]
""".strip()

    return prompt

def query_llm(prompt):
    """Query the LLM using Ollama"""
    logger.info("Querying LLM...")
    try:
        # Use mistral:latest
        result = subprocess.run(
            ["ollama", "run", "mistral:latest"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120  # Longer timeout for reflection
        )

        # Log stderr if there's any error output
        if result.stderr:
            stderr_output = result.stderr.decode("utf-8")
            if stderr_output.strip():
                logger.warning(f"LLM stderr output: {stderr_output}")

        response = result.stdout.decode("utf-8")

        # Check if response is empty
        if not response.strip():
            logger.error("Empty response received from LLM")
            return "Error: Empty response from LLM"

        logger.info("LLM response received")
        return response
    except subprocess.TimeoutExpired:
        logger.error("LLM query timed out")
        return "Error: LLM query timed out"
    except Exception as e:
        logger.error(f"Error querying LLM: {e}")
        return f"Error: {str(e)}"

def parse_reflection_response(response):
    """Parse the LLM reflection response"""
    try:
        # Use regex to extract the fields
        pattern_analysis = re.search(r"PATTERN_ANALYSIS:\s*(.*?)(?=KEY_FACTORS:|$)", response, re.DOTALL)
        key_factors = re.search(r"KEY_FACTORS:\s*(.*?)(?=FLAWED_LOGIC:|$)", response, re.DOTALL)
        flawed_logic = re.search(r"FLAWED_LOGIC:\s*(.*?)(?=STRONGEST_INSIGHT:|$)", response, re.DOTALL)
        strongest_insight = re.search(r"STRONGEST_INSIGHT:\s*(.*?)(?=\n|$)", response, re.DOTALL)

        result = {
            "pattern_analysis": pattern_analysis.group(
                1).strip() if pattern_analysis else "No pattern analysis provided",
            "key_factors": key_factors.group(1).strip() if key_factors else "No key factors provided",
            "flawed_logic": flawed_logic.group(1).strip() if flawed_logic else "No flawed logic analysis provided",
            "strongest_insight": strongest_insight.group(
                1).strip() if strongest_insight else "No strongest insight provided"
        }

        return result
    except Exception as e:
        logger.error(f"Error parsing reflection response: {e}")
        logger.error(f"Problematic response: {response}")
        return {
            "pattern_analysis": f"Error parsing response: {str(e)}",
            "key_factors": "Error",
            "flawed_logic": "Error",
            "strongest_insight": "Error"
        }

def update_insights_database(prop_type, reflection_result, date):
    """Update the insights database with new reflection results"""
    # Load existing insights database
    if os.path.exists(INSIGHTS_DB_PATH):
        with open(INSIGHTS_DB_PATH, 'r') as f:
            insights_db = json.load(f)
    else:
        insights_db = {"prop_types": {}}

    # Initialize prop type if it doesn't exist
    if prop_type not in insights_db["prop_types"]:
        insights_db["prop_types"][prop_type] = []

    # Add new insight
    new_insight = {
        "date": date,
        "strongest_insight": reflection_result["strongest_insight"],
        "key_factors": reflection_result["key_factors"],
        "pattern_analysis": reflection_result["pattern_analysis"]
    }

    insights_db["prop_types"][prop_type].append(new_insight)

    # Save updated database
    with open(INSIGHTS_DB_PATH, 'w') as f:
        json.dump(insights_db, f, indent=2)

    logger.info(f"Updated insights database for {prop_type}")

def calculate_accuracy_metrics(df):
    """Calculate accuracy metrics for RF model, LLM, and when they agree"""
    if df.empty:
        return {}

    # Calculate RF accuracy
    rf_correct = (df['RF_Prediction'] == 1) & (df['Actual_Result'] == 'Over') | \
                 (df['RF_Prediction'] == 0) & (df['Actual_Result'] == 'Under')
    rf_accuracy = rf_correct.mean()

    # Calculate LLM accuracy
    llm_correct = (df['LLM_Prediction'] == df['Actual_Result'])
    llm_accuracy = llm_correct.mean()

    # Calculate agreement accuracy
    agreement_mask = ((df['RF_Prediction'] == 1) & (df['LLM_Prediction'] == 'Over')) | \
                     ((df['RF_Prediction'] == 0) & (df['LLM_Prediction'] == 'Under'))

    if agreement_mask.sum() > 0:
        agreement_df = df[agreement_mask]
        agreement_correct = (agreement_df['LLM_Prediction'] == agreement_df['Actual_Result'])
        agreement_accuracy = agreement_correct.mean()
        agreement_count = len(agreement_df)
    else:
        agreement_accuracy = 0
        agreement_count = 0

    return {
        "rf_accuracy": rf_accuracy,
        "llm_accuracy": llm_accuracy,
        "agreement_accuracy": agreement_accuracy,
        "total_predictions": len(df),
        "agreement_count": agreement_count,
        "rf_correct": rf_correct.sum(),
        "llm_correct": llm_correct.sum()
    }

def update_accuracy_csv(date, overall_metrics, prop_type_metrics):
    """Update the accuracy CSV with new metrics"""
    # Create new row for this date
    new_row = {
        "Date": date,
        "Total_Predictions": overall_metrics["total_predictions"],
        "RF_Accuracy": overall_metrics["rf_accuracy"],
        "LLM_Accuracy": overall_metrics["llm_accuracy"],
        "Agreement_Accuracy": overall_metrics["agreement_accuracy"],
        "Agreement_Count": overall_metrics["agreement_count"]
    }

    # Add prop-type specific metrics
    for prop_type, metrics in prop_type_metrics.items():
        safe_prop_type = prop_type.replace(" ", "_")
        new_row[f"{safe_prop_type}_Count"] = metrics["total_predictions"]
        new_row[f"{safe_prop_type}_RF_Accuracy"] = metrics["rf_accuracy"]
        new_row[f"{safe_prop_type}_LLM_Accuracy"] = metrics["llm_accuracy"]

    # Load existing CSV or create new one
    if os.path.exists(ACCURACY_CSV_PATH):
        accuracy_df = pd.read_csv(ACCURACY_CSV_PATH)

        # Check if this date already exists
        if date in accuracy_df["Date"].values:
            # Update existing row
            accuracy_df.loc[accuracy_df["Date"] == date] = pd.Series(new_row)
        else:
            # Append new row
            accuracy_df = pd.concat([accuracy_df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        # Create new DataFrame
        accuracy_df = pd.DataFrame([new_row])

    # Save updated CSV
    # Add this line right before accuracy_df.to_csv(ACCURACY_CSV_PATH, index=False):
    accuracy_df = accuracy_df.round(3)  # This will round all numeric columns to 3 decimal places
    accuracy_df.to_csv(ACCURACY_CSV_PATH, index=False)
    logger.info(f"Updated accuracy metrics in {ACCURACY_CSV_PATH}")

def compare_rf_xgboost(date=None):
    """Compare Random Forest and XGBoost model predictions and save results to CSV"""
    logger.info("Starting RF vs XGBoost comparison")

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    # Define file paths
    rf_predictions_path = os.path.join(RESULTS_DIR, f"{date}_mlb_predictions.csv")
    xgb_predictions_path = os.path.join(RESULTS_DIR, f"{date}_mlb_xgb_predictions.csv")
    comparison_csv_path = os.path.join(RESULTS_DIR, "rf_vs_xgboost_accuracy.csv")

    # Load predictions
    try:
        rf_df = pd.read_csv(rf_predictions_path)
        logger.info(f"Loaded {len(rf_df)} RF predictions from {rf_predictions_path}")
    except FileNotFoundError:
        logger.error(f"RF predictions file not found at {rf_predictions_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading RF predictions: {e}")
        return None

    try:
        xgb_df = pd.read_csv(xgb_predictions_path)
        logger.info(f"Loaded {len(xgb_df)} XGBoost predictions from {xgb_predictions_path}")
    except FileNotFoundError:
        logger.error(f"XGBoost predictions file not found at {xgb_predictions_path}")
        return None
    except Exception as e:
        logger.error(f"Error loading XGBoost predictions: {e}")
        return None

    # Check if actual results are available in RF predictions
    if 'Actual_Result' not in rf_df.columns or rf_df['Actual_Result'].isna().all():
        logger.warning(f"No actual results found in {rf_predictions_path}. Will only compare predictions.")
        has_results = False
    else:
        has_results = True
        # Filter to only include predictions with actual results
        rf_df = rf_df[rf_df['Actual_Result'].notna()].copy()
        logger.info(f"Found {len(rf_df)} completed RF predictions with actual results")

        # Update XGBoost predictions with actual results from RF predictions
        logger.info("Updating XGBoost predictions with actual results")

        # Create a mapping of player+prop_type+prop_value to actual results
        result_map = {}
        for _, row in rf_df.iterrows():
            key = (row['Player'], row['Prop Type'], row['Prop Value'])
            result_map[key] = {
                'Actual_Stat': row.get('Actual_Stat', None),
                'Actual_Result': row.get('Actual_Result', None)
            }

        # Update XGBoost predictions with actual results
        updated_rows = 0
        for idx, row in xgb_df.iterrows():
            key = (row['Player'], row['Prop Type'], row['Prop Value'])
            if key in result_map:
                xgb_df.at[idx, 'Actual_Stat'] = result_map[key]['Actual_Stat']
                xgb_df.at[idx, 'Actual_Result'] = result_map[key]['Actual_Result']
                updated_rows += 1

        logger.info(f"Updated {updated_rows} rows in XGBoost predictions with actual results")

        # Save updated XGBoost predictions
        xgb_df.to_csv(xgb_predictions_path, index=False)
        logger.info(f"Saved updated XGBoost predictions to {xgb_predictions_path}")

    # Merge datasets on common keys
    # We'll use Player, Prop Type, and Prop Value as the keys
    merged_df = pd.merge(
        rf_df,
        xgb_df[['Player', 'Prop Type', 'Prop Value', 'XGB_Prediction', 'XGB_Confidence']],
        on=['Player', 'Prop Type', 'Prop Value'],
        how='inner',
        suffixes=('', '_xgb')
    )

    logger.info(f"Merged dataset contains {len(merged_df)} props with both RF and XGBoost predictions")

    # Convert XGBoost binary predictions to Over/Under format
    merged_df['XGB_Prediction_Text'] = merged_df['XGB_Prediction'].map({1: 'Over', 0: 'Under'})

    # Convert RF binary predictions to Over/Under format
    merged_df['RF_Prediction_Text'] = merged_df['RF_Prediction'].map({1: 'Over', 0: 'Under'})

    # Calculate overall metrics
    overall_metrics = {
        "Date": date,
        "Total_Predictions": len(merged_df),
        "RF_Over_Percentage": (merged_df['RF_Prediction'] == 1).mean(),
        "XGB_Over_Percentage": (merged_df['XGB_Prediction'] == 1).mean()
    }

    # Add accuracy metrics if we have actual results
    if has_results:
        rf_correct = (merged_df['RF_Prediction_Text'] == merged_df['Actual_Result'])
        xgb_correct = (merged_df['XGB_Prediction_Text'] == merged_df['Actual_Result'])

        overall_metrics["RF_Accuracy"] = rf_correct.mean()
        overall_metrics["XGB_Accuracy"] = xgb_correct.mean()
        overall_metrics["RF_Correct"] = rf_correct.sum()
        overall_metrics["XGB_Correct"] = xgb_correct.sum()

    # Calculate prop-type specific metrics
    prop_type_metrics = {}
    for prop_type in merged_df['Prop Type'].unique():
        prop_df = merged_df[merged_df['Prop Type'] == prop_type]

        safe_prop_type = prop_type.replace(" ", "_")
        prop_type_metrics[safe_prop_type] = {
            "Count": len(prop_df),
            "RF_Over_Percentage": (prop_df['RF_Prediction'] == 1).mean(),
            "XGB_Over_Percentage": (prop_df['XGB_Prediction'] == 1).mean()
        }

        if has_results:
            prop_rf_correct = (prop_df['RF_Prediction_Text'] == prop_df['Actual_Result'])
            prop_xgb_correct = (prop_df['XGB_Prediction_Text'] == prop_df['Actual_Result'])

            prop_type_metrics[safe_prop_type]["RF_Accuracy"] = prop_rf_correct.mean()
            prop_type_metrics[safe_prop_type]["XGB_Accuracy"] = prop_xgb_correct.mean()

    # Create a row for the accuracy CSV
    new_row = overall_metrics.copy()

    # Add prop-type specific metrics to the row
    for prop_type, metrics in prop_type_metrics.items():
        for metric_name, metric_value in metrics.items():
            new_row[f"{prop_type}_{metric_name}"] = metric_value

    # Load existing CSV or create new one
    if os.path.exists(comparison_csv_path):
        accuracy_df = pd.read_csv(comparison_csv_path)

        # Check if this date already exists
        if date in accuracy_df["Date"].values:
            # Update existing row
            accuracy_df.loc[accuracy_df["Date"] == date] = pd.Series(new_row)
        else:
            # Append new row
            accuracy_df = pd.concat([accuracy_df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        # Create new DataFrame
        accuracy_df = pd.DataFrame([new_row])

    # Save updated CSV
    accuracy_df = accuracy_df.round(3)  # Round to 3 decimal places
    accuracy_df.to_csv(comparison_csv_path, index=False)
    logger.info(f"Updated model comparison metrics in {comparison_csv_path}")

    # Print summary
    print("\nRF vs XGBoost Comparison Summary:")
    print(f"Total props analyzed: {overall_metrics['Total_Predictions']}")
    print(f"RF over percentage: {overall_metrics['RF_Over_Percentage']:.1%}")
    print(f"XGB over percentage: {overall_metrics['XGB_Over_Percentage']:.1%}")

    if has_results:
        print(
            f"RF accuracy: {overall_metrics['RF_Accuracy']:.1%} ({overall_metrics['RF_Correct']}/{overall_metrics['Total_Predictions']})")
        print(
            f"XGB accuracy: {overall_metrics['XGB_Accuracy']:.1%} ({overall_metrics['XGB_Correct']}/{overall_metrics['Total_Predictions']})")

    print("\nBy Prop Type:")
    for prop_type, metrics in prop_type_metrics.items():
        readable_prop_type = prop_type.replace("_", " ")
        print(f"\n{readable_prop_type} ({metrics['Count']} props):")
        print(f"  RF over percentage: {metrics['RF_Over_Percentage']:.1%}")
        print(f"  XGB over percentage: {metrics['XGB_Over_Percentage']:.1%}")

        if has_results:
            print(f"  RF accuracy: {metrics['RF_Accuracy']:.1%}")
            print(f"  XGB accuracy: {metrics['XGB_Accuracy']:.1%}")

    return merged_df

def main(date=None):
    """Main function to run the reflection pipeline"""
    if date is None:
        date = input("Enter date (YYYY-MM-DD) for reflection: ")

    logger.info(f"Starting reflection pipeline for {date}")

    # Load predictions with results
    df = load_predictions_with_results(date)
    if df is None or df.empty:
        logger.error("No predictions with results found. Exiting.")
        return

    # Group by prop type
    prop_groups = group_by_prop_type(df)
    if not prop_groups:
        logger.error("Failed to group predictions by prop type. Exiting.")
        return

    # Calculate overall accuracy metrics
    overall_metrics = calculate_accuracy_metrics(df)
    prop_type_metrics = {}

    # Process each prop type
    for prop_type, prop_df in prop_groups.items():
        logger.info(f"Processing reflections for {prop_type} props")

        # Calculate accuracy metrics for this prop type
        prop_type_metrics[prop_type] = calculate_accuracy_metrics(prop_df)

        # Build reflection prompt
        prompt = build_reflection_prompt(prop_type, prop_df)

        # Query LLM
        response = query_llm(prompt)

        # Parse response
        if response.startswith("Error:"):
            logger.error(f"LLM error for {prop_type}: {response}")
            continue

        reflection_result = parse_reflection_response(response)

        # Update insights database
        update_insights_database(prop_type, reflection_result, date)

        logger.info(f"Completed reflection for {prop_type} props")

    # Update accuracy CSV
    update_accuracy_csv(date, overall_metrics, prop_type_metrics)

    # Compare RF and XGBoost models
    compare_rf_xgboost(date)

    logger.info(f"Reflection pipeline completed for {date}")
    return df, prop_groups

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
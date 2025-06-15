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
    new_row = {
        "Date": date,
        "Total_Predictions": overall_metrics["total_predictions"],
        "RF_Accuracy": overall_metrics["rf_accuracy"],
        "LLM_Accuracy": overall_metrics["llm_accuracy"],
        "Agreement_Accuracy": overall_metrics["agreement_accuracy"],
        "Agreement_Count": overall_metrics["agreement_count"]
    }
    for prop_type, metrics in prop_type_metrics.items():
        safe_prop_type = prop_type.replace(" ", "_")
        new_row[f"{safe_prop_type}_Count"] = metrics["total_predictions"]
        new_row[f"{safe_prop_type}_RF_Accuracy"] = metrics["rf_accuracy"]
        new_row[f"{safe_prop_type}_LLM_Accuracy"] = metrics["llm_accuracy"]

    if os.path.exists(ACCURACY_CSV_PATH):
        accuracy_df = pd.read_csv(ACCURACY_CSV_PATH)
        if date in accuracy_df["Date"].values:
            idx = accuracy_df.index[accuracy_df["Date"] == date][0]
            for k, v in new_row.items():
                accuracy_df.at[idx, k] = v
        else:
            accuracy_df = pd.concat([accuracy_df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        accuracy_df = pd.DataFrame([new_row])

    accuracy_df = accuracy_df.round(3)
    accuracy_df.to_csv(ACCURACY_CSV_PATH, index=False)
    logger.info(f"Updated accuracy metrics in {ACCURACY_CSV_PATH}")

def calculate_xgboost_accuracy(date=None):
    """
    For a given date, computes:
      - XGB overall accuracy (all predictions with result)
      - By prop type: accuracy and counts
    Writes one row per date to xgboost_accuracy.csv, all columns.
    """
    logger.info("Starting XGBoost accuracy summary")

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    xgb_path = os.path.join(RESULTS_DIR, f"{date}_mlb_xgb_predictions.csv")
    summary_path = os.path.join(RESULTS_DIR, "xgboost_accuracy.csv")

    key_cols = ["Player", "Prop Type", "Prop Value"]

    # --- Load and filter ---
    xgb_df = pd.read_csv(xgb_path)
    xgb_df = xgb_df[xgb_df['Actual_Result'].notna()].drop_duplicates(subset=key_cols)
    xgb_df["XGB_Prediction_Text"] = xgb_df["XGB_Prediction"].map({1: "Over", 0: "Under"})
    xgb_df["XGB_Correct"] = (xgb_df["XGB_Prediction_Text"] == xgb_df["Actual_Result"])

    # --- Overall stats ---
    summary_row = {
        "Date": date,
        "XGB_Total": len(xgb_df),
        "XGB_Correct": xgb_df["XGB_Correct"].sum(),
        "XGB_Accuracy": round(xgb_df["XGB_Correct"].mean(), 3) if len(xgb_df) else None,
    }

    # --- By prop type ---
    all_prop_types = sorted(xgb_df["Prop Type"].unique())
    for prop in all_prop_types:
        xgb_sub = xgb_df[xgb_df["Prop Type"] == prop]
        safe = prop.replace(" ", "_")

        summary_row[f"{safe}_XGB_Total"] = len(xgb_sub)
        summary_row[f"{safe}_XGB_Correct"] = xgb_sub["XGB_Correct"].sum()
        summary_row[f"{safe}_XGB_Accuracy"] = round(xgb_sub["XGB_Correct"].mean(), 3) if len(xgb_sub) else None

    # --- Save: append or update ---
    if os.path.exists(summary_path):
        df = pd.read_csv(summary_path)
        if date in df["Date"].values:
            for col, val in summary_row.items():
                df.loc[df["Date"] == date, col] = val
        else:
            df = pd.concat([df, pd.DataFrame([summary_row])], ignore_index=True)
    else:
        df = pd.DataFrame([summary_row])

    df.to_csv(summary_path, index=False)
    logger.info(f"Saved XGBoost summary to {summary_path}")

    return summary_row


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
    calculate_xgboost_accuracy(date)

    logger.info(f"Reflection pipeline completed for {date}")
    return df, prop_groups

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
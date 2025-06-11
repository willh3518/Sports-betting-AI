import pandas as pd
import subprocess
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("llm_inference.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Config
RESULTS_DIR = "MLB_Results"
MLB_DATA_DIR = "MLB_Prop_Data_CSV"
TODAY_DATE = datetime.now().strftime("%Y-%m-%d")
PREDICTIONS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_predictions.csv")
TOP_PICKS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_top_picks_with_llm.csv")
BETSLIPS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_betslips.json")

# Master data paths
MASTER_HITTER_PATH = os.path.join(MLB_DATA_DIR, "master_hitter_dataset.csv")
MASTER_PITCHER_PATH = os.path.join(MLB_DATA_DIR, "master_pitcher_dataset.csv")

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)


def load_master_data():
    """Load master hitter and pitcher data"""
    master_hitter = pd.DataFrame()
    master_pitcher = pd.DataFrame()

    try:
        if os.path.exists(MASTER_HITTER_PATH):
            master_hitter = pd.read_csv(MASTER_HITTER_PATH)
            logger.info(f"Loaded master hitter data with {len(master_hitter)} rows")
        else:
            logger.warning(f"Master hitter data not found at {MASTER_HITTER_PATH}")
    except Exception as e:
        logger.error(f"Error loading master hitter data: {e}")

    try:
        if os.path.exists(MASTER_PITCHER_PATH):
            master_pitcher = pd.read_csv(MASTER_PITCHER_PATH)
            logger.info(f"Loaded master pitcher data with {len(master_pitcher)} rows")
        else:
            logger.warning(f"Master pitcher data not found at {MASTER_PITCHER_PATH}")
    except Exception as e:
        logger.error(f"Error loading master pitcher data: {e}")

    return master_hitter, master_pitcher

def load_predictions():
    """Load the predictions CSV file"""
    logger.info(f"Loading predictions from {PREDICTIONS_PATH}")
    try:
        df = pd.read_csv(PREDICTIONS_PATH)
        logger.info(f"Loaded {len(df)} predictions")
        return df
    except FileNotFoundError:
        logger.error(f"Predictions file not found at {PREDICTIONS_PATH}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"Error loading predictions: {e}")
        return pd.DataFrame()

def enrich_predictions_with_master_data(predictions_df, master_hitter, master_pitcher):
    """Enrich predictions with additional data from master files"""
    if predictions_df.empty:
        return predictions_df

    # Check if we have the necessary columns
    if 'Player' not in predictions_df.columns:
        logger.warning("No 'Player' column in predictions, skipping enrichment")
        return predictions_df

    enriched_df = predictions_df.copy()

    # Create a unique identifier for each row before merging
    enriched_df['row_id'] = range(len(enriched_df))

    # Enrich with hitter data
    if not master_hitter.empty and 'Player' in master_hitter.columns:
        logger.info("Enriching with hitter data")

        # Get unique players from master_hitter
        unique_hitter_data = master_hitter.drop_duplicates(subset=['Player'])

        # Merge on Player column
        enriched_df = pd.merge(
            enriched_df,
            unique_hitter_data,
            left_on='Player',
            right_on='Player',
            how='left',
            suffixes=('', '_hitter_master')
        )

    # Enrich with pitcher data
    if not master_pitcher.empty and 'Player' in master_pitcher.columns:
        logger.info("Enriching with pitcher data")

        # Get unique players from master_pitcher
        unique_pitcher_data = master_pitcher.drop_duplicates(subset=['Player'])

        # For pitcher props, merge on Player
        pitcher_props = enriched_df[enriched_df['Model_Type'] == 'pitcher'].copy()
        if not pitcher_props.empty:
            pitcher_props = pd.merge(
                pitcher_props,
                unique_pitcher_data,
                left_on='Player',
                right_on='Player',
                how='left',
                suffixes=('', '_pitcher_master')
            )

            # Update the enriched dataframe with pitcher data
            enriched_df.update(pitcher_props)

    # Sort by the original row order and remove the row_id column
    enriched_df = enriched_df.sort_values('row_id').drop('row_id', axis=1)

    logger.info(f"Enrichment complete. DataFrame now has {len(enriched_df.columns)} columns")
    return enriched_df

def build_prompt(row):
    """Build a prompt for the LLM based on the row data"""
    # Get player name from the Player column
    player_name = row.get('Player', 'Unknown Player')

    # Get prop type and value
    prop_type = row.get('Prop Type', 'Unknown Prop')
    prop_value = row.get('Prop Value', 'Unknown Value')

    # Get RF prediction and confidence
    rf_pred = 'Over' if row.get('RF_Prediction', 0) == 1 else 'Under'
    rf_conf = round(row.get('RF_Confidence', 0) * 100, 1)

    # Get model type (hitter or pitcher)
    model_type = row.get('Model_Type', 'unknown')

    # Build the full prompt with the new format
    prompt = f"""<s>[INST] System: You are a world-class MLB prop betting analyst working alongside an AI model. Your job is to critically evaluate the model's prediction for a player prop bet using detailed statistics and game context.

User: I need your expert analysis on the following MLB prop bet:

You will be given:
1. A specific prop bet (e.g. Hits+Runs+RBIs, Total Bases, Fantasy Score, Strikeouts)
2. The model's Over/Under prediction and confidence level
3. A complete statistical profile of the player, opponent, and game environment

---

🎯 **Your Tasks**:
1. Decide whether **you predict Over or Under**
2. Decide if the model's prediction is **reasonable** based on the data
3. Give a **short justification (1–3 sentences)** using relevant stats, trends, or conditions
4. Provide your confidence level in your prediction

🛠️ **Important Note**:  
The Random Forest (RF) model you are reviewing is in its **early development stage** with limited training data. It may make poor or unreliable predictions, especially on edge cases or new players. Use your own judgment and **do not trust the model blindly**.

---

📌 **Prop Details**
- **Player**: {player_name}
- **Prop Line**: {prop_type} at {prop_value}
- **Model Prediction**: {rf_pred} (Confidence: {rf_conf}%)
- **Player Type**: {model_type.capitalize()}

---

📊 **Player Stats**
**Season Averages:**
- AVG: {row.get('AVG', 'N/A')} | OBP: {row.get('OBP', 'N/A')} | SLG: {row.get('SLG', 'N/A')} | OPS: {row.get('OPS', 'N/A')}
- wOBA: {row.get('wOBA', 'N/A')} | xwOBA: {row.get('xwOBA', 'N/A')}
- Barrel %: {row.get('Barrel%', 'N/A')} | Hard Hit %: {row.get('Hard Hit %', 'N/A')}

**Splits:**
- vs RHP — AVG: {row.get('AVG_vs_rhp', 'N/A')} | OPS: {row.get('OPS_vs_rhp', 'N/A')}
- vs LHP — AVG: {row.get('AVG_vs_lhp', 'N/A')} | OPS: {row.get('OPS_vs_lhp', 'N/A')}

**Recent Form:**
- Last 15 Games: {row.get('Last_15_Performance', 'N/A')}
- Last 30 Games: {row.get('Last_30_Performance', 'N/A')}
- Home/Away Split: {row.get('Home_Away_Split', 'N/A')}

**Plate Discipline:**
- K%: {row.get('k_pct_season', 'N/A')} | BB%: {row.get('bb_pct_season', 'N/A')}

---

🧠 **Opponent Info**
**Pitcher Matchup:**
- Name: {row.get('Opposing Pitcher', 'N/A')} | Hand: {row.get('Pitcher Handedness', 'N/A')}
- ERA: {row.get('ERA_pitcher', 'N/A')} | WHIP: {row.get('WHIP_pitcher', 'N/A')} | K/9: {row.get('K/9_pitcher', 'N/A')}
- BB/9: {row.get('BB/9_pitcher', 'N/A')} | HR/9: {row.get('HR/9_pitcher', 'N/A')}
- 15-day Hard Hit %: {row.get('15_day_hard_hit_pct_pitcher', 'N/A')}

**If Pitcher Prop: Opposing Team Stats**
- Team wOBA: {row.get('Team_wOBA', 'N/A')} | Team K%: {row.get('Team_K%', 'N/A')}

---

🌦️ **Game Conditions**
- Park Factor (Basic): {row.get('Park_Factor_Basic', 'N/A')}
- Park Factor (HR): {row.get('Park_Factor_HR', 'N/A')}
- Temperature: {row.get('Game-Time Temp (°F)', 'N/A')}°F
- Wind: {row.get('Game-Time Wind Speed (mph)', 'N/A')} mph
- Wind Effect: {row.get('Game-Time Effect on Hitters', 'N/A')}

---

⚠️ **Guidelines**
- **Skeptical?** If the model has < 55% confidence, treat its prediction as weak unless the data strongly supports it.
- If any data is missing, clearly state your assumptions or fallback logic.
- Don't generalize. Use **specific numbers** to support your call.
- Critically evaluate ALL relevant factors before making your prediction. Don't fixate on just one stat or trend.
- Assume the reader is sharp — avoid fluff or filler.

---

Example Response:
LLM_Prediction: Over
LLM_RF_Agreement: False
LLM_Confidence: High
LLM_Justification: Player has a .420 OBP vs LHP and faces a lefty starter with 5.2 BB/9. The 15mph winds blowing out to center also favor hitting conditions.

---

✏️ **Respond ONLY in this exact format**:
LLM_Prediction: Over or Under  
LLM_RF_Agreement: True or False  
LLM_Confidence: High/Medium/Low
LLM_Justification: [Short reasoning using stats, matchup info, or game conditions]
[/INST]
""".strip()

    return prompt

def query_llm(prompt):
    """Query the LLM using Ollama"""
    logger.info("Querying LLM...")
    try:
        # Add debug logging to see the prompt being sent
        logger.debug(f"Sending prompt: {prompt[:100]}...")

        # Use mistral:7b-instruct-v0.2 instead of phi3:mini
        result = subprocess.run(
            ["ollama", "run", "mistral:latest"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )

        # Log stderr if there's any error output
        if result.stderr:
            stderr_output = result.stderr.decode("utf-8")
            if stderr_output.strip():
                logger.warning(f"LLM stderr output: {stderr_output}")

        response = result.stdout.decode("utf-8")

        # Add debug logging to see the response
        logger.debug(f"Raw response: {response[:100]}...")

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

def parse_llm_response(response, rf_prediction):
    """Parse LLM response and derive agreement with RF prediction"""
    try:
        # Extract prediction
        pred_line = [line for line in response.splitlines() if "LLM_Prediction:" in line]
        prediction = "Unknown"
        if pred_line:
            pred_text = pred_line[0].split("LLM_Prediction:")[-1].strip().lower()
            if "over" in pred_text:
                prediction = "Over"
            elif "under" in pred_text:
                prediction = "Under"

        # Derive agreement based on match with RF
        rf_pred_text = "Over" if rf_prediction == 1 else "Under"
        agreement = "True" if prediction == rf_pred_text else "False"

        # Extract justification
        just_line = [line for line in response.splitlines() if "LLM_Justification:" in line]
        justification = just_line[0].split("LLM_Justification:")[-1].strip() if just_line else "No justification provided"

        # Extract confidence (optional — if you're using it)
        conf_line = [line for line in response.splitlines() if "LLM_Confidence:" in line]
        confidence = conf_line[0].split("LLM_Confidence:")[-1].strip() if conf_line else "Unknown"

        return prediction, agreement, justification, confidence

    except Exception as e:
        return "Unknown", "Unknown", f"Error parsing response: {str(e)}", "Unknown"

def generate_betslips(df, num_betslips=5, props_per_betslip=2):
    """Generate betslips from the predictions"""
    logger.info(f"Generating {num_betslips} betslips with {props_per_betslip} props each")

    # Filter to only include rows where LLM agrees with RF
    agreed_df = df[df['LLM_RF_Agreement'] == 'True'].copy()

    if len(agreed_df) < props_per_betslip:
        logger.warning(
            f"Not enough agreed predictions to generate betslips. Found {len(agreed_df)}, need at least {props_per_betslip}.")
        return []

    # Sort by RF confidence
    agreed_df = agreed_df.sort_values('RF_Confidence', ascending=False)

    # Generate betslips
    betslips = []

    # First betslip: top confidence picks
    top_picks = agreed_df.head(props_per_betslip)
    betslips.append({
        "name": "Top Confidence Picks",
        "props": top_picks[['Player', 'Prop Type', 'Prop Value', 'RF_Prediction', 'RF_Confidence', 'LLM_Prediction',
                            'LLM_Justification']].to_dict('records')
    })

    # Try to generate diverse betslips
    # We'll use different strategies:

    # 1. Mix of hitter and pitcher props
    if 'Model_Type' in agreed_df.columns:
        hitter_props = agreed_df[agreed_df['Model_Type'] == 'hitter'].head(props_per_betslip // 2)
        pitcher_props = agreed_df[agreed_df['Model_Type'] == 'pitcher'].head(props_per_betslip // 2)

        if len(hitter_props) >= 1 and len(pitcher_props) >= 1:
            mixed_props = pd.concat([hitter_props, pitcher_props]).head(props_per_betslip)
            betslips.append({
                "name": "Mixed Hitter/Pitcher Props",
                "props": mixed_props[
                    ['Player', 'Prop Type', 'Prop Value', 'RF_Prediction', 'RF_Confidence', 'LLM_Prediction',
                     'LLM_Justification']].to_dict('records')
            })

    # 2. All Over picks
    over_picks = agreed_df[agreed_df['RF_Prediction'] == 1].head(props_per_betslip)
    if len(over_picks) >= props_per_betslip:
        betslips.append({
            "name": "All Overs",
            "props": over_picks[
                ['Player', 'Prop Type', 'Prop Value', 'RF_Prediction', 'RF_Confidence', 'LLM_Prediction',
                 'LLM_Justification']].to_dict('records')
        })

    # 3. All Under picks
    under_picks = agreed_df[agreed_df['RF_Prediction'] == 0].head(props_per_betslip)
    if len(under_picks) >= props_per_betslip:
        betslips.append({
            "name": "All Unders",
            "props": under_picks[
                ['Player', 'Prop Type', 'Prop Value', 'RF_Prediction', 'RF_Confidence', 'LLM_Prediction',
                 'LLM_Justification']].to_dict('records')
        })

    # 4. Highest confidence over and under
    if len(over_picks) >= 1 and len(under_picks) >= 1:
        balanced_picks = pd.concat([over_picks.head(1), under_picks.head(1)])
        betslips.append({
            "name": "Balanced Over/Under",
            "props": balanced_picks[
                ['Player', 'Prop Type', 'Prop Value', 'RF_Prediction', 'RF_Confidence', 'LLM_Prediction',
                 'LLM_Justification']].to_dict('records')
        })

    # Limit to requested number of betslips
    betslips = betslips[:num_betslips]

    return betslips

def main():
    """Main function to run the LLM inference pipeline"""
    logger.info("Starting LLM inference pipeline")

    # Load predictions
    df = load_predictions()

    if df.empty:
        logger.error("No predictions to process. Exiting.")
        return

    # Log the initial shape of the DataFrame
    initial_row_count = len(df)
    logger.info(f"Initial DataFrame shape: {df.shape}")

    # Load master data
    master_hitter, master_pitcher = load_master_data()

    # Enrich predictions with master data
    if not master_hitter.empty or not master_pitcher.empty:
        df = enrich_predictions_with_master_data(df, master_hitter, master_pitcher)

    # Verify row count hasn't changed
    if len(df) != initial_row_count:
        logger.warning(f"Row count changed during enrichment: {initial_row_count} -> {len(df)}")
        logger.warning("Resetting to original row count")
        # If row count changed, we need to fix it
        df = df.drop_duplicates(subset=['Player', 'Prop Type', 'Prop Value', 'Start Time'])
        if len(df) > initial_row_count:
            # If still too many rows, take the first initial_row_count rows
            df = df.head(initial_row_count)
        elif len(df) < initial_row_count:
            logger.error(f"Lost rows during enrichment and deduplication. Expected {initial_row_count}, got {len(df)}")

    # Reset index to ensure correct counting
    df = df.reset_index(drop=True)

    # Log the shape after enrichment
    logger.info(f"DataFrame shape after enrichment: {df.shape}")

    # Log the actual number of predictions to process
    logger.info(f"Processing {len(df)} predictions after enrichment")

    # Run inference row-by-row with logging
    llm_preds, llm_justifications, llm_agreements, llm_confidences = [], [], [], []

    for idx, row in df.iterrows():
        player_name = row.get("Player", "Unknown")
        logger.info(f"Processing prediction {idx + 1}/{len(df)} for {player_name}")

        # Build prompt
        prompt = build_prompt(row)

        # Query LLM
        response = query_llm(prompt)

        # Parse response
        prediction, agreement, justification, confidence = parse_llm_response(response, row.get("RF_Prediction", 0))

        # Store results
        llm_preds.append(prediction)
        llm_agreements.append(agreement)
        llm_justifications.append(justification)
        llm_confidences.append(confidence)

        logger.info(f"LLM prediction for {player_name}: {prediction}, Agreement: {agreement}")

    # Add results to DataFrame
    df["LLM_Prediction"] = llm_preds
    df["LLM_RF_Agreement"] = llm_agreements
    df["LLM_Justification"] = llm_justifications
    df["LLM_Confidence"] = llm_confidences

    # Overwrite the original predictions CSV with added LLM columns
    df.to_csv(PREDICTIONS_PATH, index=False)
    logger.info(f"LLM-enhanced predictions added to original file: {PREDICTIONS_PATH}")

    # Load existing top picks CSV and update it with LLM outputs
    if os.path.exists(TOP_PICKS_PATH):
        top_picks_df = pd.read_csv(TOP_PICKS_PATH)
        logger.info(f"Loaded top picks from {TOP_PICKS_PATH}")

        llm_preds, llm_justifications, llm_agreements, llm_confidences = [], [], [], []

        for idx, row in top_picks_df.iterrows():
            player_name = row.get("Player", "Unknown")
            logger.info(f"Processing top pick {idx + 1}/{len(top_picks_df)} for {player_name}")

            prompt = build_prompt(row)
            response = query_llm(prompt)
            prediction, agreement, justification = parse_llm_response(response)

            llm_preds.append(prediction)
            llm_agreements.append(agreement)
            llm_justifications.append(justification)

        top_picks_df["LLM_Prediction"] = llm_preds
        top_picks_df["LLM_RF_Agreement"] = llm_agreements
        top_picks_df["LLM_Justification"] = llm_justifications

        top_picks_df.to_csv(TOP_PICKS_PATH, index=False)
        logger.info(f"Updated LLM-enhanced top picks written to: {TOP_PICKS_PATH}")
    else:
        logger.error(f"Top picks file not found at {TOP_PICKS_PATH}")

    # Generate betslips
    betslips = generate_betslips(df)

    # Save betslips
    with open(BETSLIPS_PATH, 'w') as f:
        json.dump(betslips, f, indent=2)
    logger.info(f"Betslips saved to {BETSLIPS_PATH}")

    logger.info("LLM inference pipeline completed")

    return df

if __name__ == "__main__":
    main()
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
TODAY_DATE = datetime.now().strftime("%Y-%m-%d")
PREDICTIONS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_predictions.csv")
OUTPUT_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_predictions_with_llm.csv")
TOP_PICKS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_top_picks_with_llm.csv")
BETSLIPS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_betslips.json")

# Ensure results directory exists
os.makedirs(RESULTS_DIR, exist_ok=True)


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

    # Build the stats section based on model type
    stats_section = ""
    if model_type == 'hitter':
        stats_section = f"""
Key Hitter Stats:
- AVG vs RHP: {row.get('AVG_vs_rhp', 'N/A')}
- OBP vs RHP: {row.get('OBP_vs_rhp', 'N/A')}
- SLG vs RHP: {row.get('SLG_vs_rhp', 'N/A')}
- OPS vs RHP: {row.get('OPS_vs_rhp', 'N/A')}
- AVG vs LHP: {row.get('AVG_vs_lhp', 'N/A')}
- OBP vs LHP: {row.get('OBP_vs_lhp', 'N/A')}
- SLG vs LHP: {row.get('SLG_vs_lhp', 'N/A')}
- OPS vs LHP: {row.get('OPS_vs_lhp', 'N/A')}
- wOBA: {row.get('wOBA', 'N/A')}
- xwOBA: {row.get('xwOBA', 'N/A')}
- Barrel%: {row.get('Barrel%', 'N/A')}
- Hard Hit %: {row.get('Hard Hit %', 'N/A')}
- EV: {row.get('EV', 'N/A')}
"""
    elif model_type == 'pitcher':
        stats_section = f"""
Key Pitcher Stats:
- ERA: {row.get('ERA', 'N/A')}
- WHIP: {row.get('WHIP', 'N/A')}
- K/9: {row.get('K/9', 'N/A')}
- BB/9: {row.get('BB/9', 'N/A')}
- K/BB: {row.get('K/BB', 'N/A')}
- HR/9: {row.get('HR/9', 'N/A')}
- K%: {row.get('K%', 'N/A')}
- BB%: {row.get('BB%', 'N/A')}
- AVG Against: {row.get('AVG Against', 'N/A')}
- 15-day Fastball Velo: {row.get('15_day_fastball_velo', 'N/A')}
- 15-day Hard Hit %: {row.get('15_day_hard_hit_pct', 'N/A')}
- 15-day Barrel %: {row.get('15_day_barrel_pct', 'N/A')}
"""

    # Game conditions section
    game_conditions = f"""
Game Conditions:
- Park Factor Basic: {row.get('Park_Factor_Basic', 'N/A')}
- Park Factor HR: {row.get('Park_Factor_HR', 'N/A')}
- Game-Time Temp: {row.get('Game-Time Temp (°F)', 'N/A')}°F
- Game-Time Humidity: {row.get('Game-Time Humidity (%)', 'N/A')}%
- Game-Time Wind Speed: {row.get('Game-Time Wind Speed (mph)', 'N/A')} mph
- Wind Effect: {row.get('Game-Time Effect on Hitters', 'N/A')}
"""

    # Build the full prompt
    prompt = f"""
You are an expert MLB betting analyst. You will be given:
1. A player prop (e.g., Hits+Runs+RBIs 0.5)
2. A summary of stats for the player
3. A prediction made by a Random Forest model

Your job is to:
- Determine if the RF prediction is valid (yes/no)
- Provide your own Over/Under prediction
- Justify your reasoning clearly

---

Player: {player_name}
Prop: {prop_type} at {prop_value}
RF Prediction: {rf_pred} with confidence {rf_conf}%

{stats_section}
{game_conditions}

---

Respond in this exact format:
LLM_Prediction: Over or Under
LLM_RF_Agreement: True or False
LLM_Justification: [brief explanation]
""".strip()

    return prompt


def query_llm(prompt):
    """Query the LLM using Ollama"""
    logger.info("Querying LLM...")
    try:
        result = subprocess.run(
            ["ollama", "run", "phi3:mini"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        response = result.stdout.decode("utf-8")
        logger.info("LLM response received")
        return response
    except subprocess.TimeoutExpired:
        logger.error("LLM query timed out")
        return "Error: LLM query timed out"
    except Exception as e:
        logger.error(f"Error querying LLM: {e}")
        return f"Error: {str(e)}"

def parse_llm_response(response):
    """Parse the LLM response to extract prediction, agreement, and justification"""
    try:
        # Extract prediction
        pred_line = [line for line in response.splitlines() if "LLM_Prediction:" in line]
        prediction = "Unknown"
        if pred_line:
            pred_text = pred_line[0].split("LLM_Prediction:")[-1].strip()
            prediction = "Over" if "over" in pred_text.lower() else "Under" if "under" in pred_text.lower() else "Unknown"

        # Extract agreement
        agree_line = [line for line in response.splitlines() if "LLM_RF_Agreement:" in line]
        agreement = "Unknown"
        if agree_line:
            agree_text = agree_line[0].split("LLM_RF_Agreement:")[-1].strip()
            agreement = "True" if "true" in agree_text.lower() else "False" if "false" in agree_text.lower() else "Unknown"

        # Extract justification
        just_line = [line for line in response.splitlines() if "LLM_Justification:" in line]
        justification = "No justification provided"
        if just_line:
            justification = just_line[0].split("LLM_Justification:")[-1].strip()

        return prediction, agreement, justification
    except Exception as e:
        logger.error(f"Error parsing LLM response: {e}")
        return "Unknown", "Unknown", f"Error parsing response: {str(e)}"

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

    # Run inference row-by-row with logging
    llm_preds, llm_justifications, llm_agreements = [], [], []

    for idx, row in df.iterrows():
        player_name = row.get("Player", "Unknown")
        logger.info(f"Processing prediction {idx + 1}/{len(df)} for {player_name}")

        # Build prompt
        prompt = build_prompt(row)

        # Query LLM
        response = query_llm(prompt)

        # Parse response
        prediction, agreement, justification = parse_llm_response(response)

        # Store results
        llm_preds.append(prediction)
        llm_agreements.append(agreement)
        llm_justifications.append(justification)

        logger.info(f"LLM prediction for {player_name}: {prediction}, Agreement: {agreement}")

    # Add results to DataFrame
    df["LLM_Prediction"] = llm_preds
    df["LLM_RF_Agreement"] = llm_agreements
    df["LLM_Justification"] = llm_justifications

    # Save enhanced predictions
    df.to_csv(OUTPUT_PATH, index=False)
    logger.info(f"LLM-enhanced predictions saved to {OUTPUT_PATH}")

    # Generate top picks (where LLM agrees with RF)
    top_picks = df[df["LLM_RF_Agreement"] == "True"].sort_values("RF_Confidence", ascending=False).head(10)
    top_picks.to_csv(TOP_PICKS_PATH, index=False)
    logger.info(f"Top picks saved to {TOP_PICKS_PATH}")

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
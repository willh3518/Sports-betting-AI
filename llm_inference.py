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
TOP_PICKS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_top_picks.csv")
BETSLIPS_PATH = os.path.join(RESULTS_DIR, f"{TODAY_DATE}_mlb_betslips.json")
INSIGHTS_DB_PATH = os.path.join(RESULTS_DIR, "mlb_insights_db.json")

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

def load_insights_database():
    """Load the MLB insights database"""
    logger.info("Loading MLB insights database...")
    try:
        if os.path.exists(INSIGHTS_DB_PATH):
            with open(INSIGHTS_DB_PATH, 'r') as f:
                insights_db = json.load(f)
            logger.info("Successfully loaded MLB insights database")
            return insights_db
        else:
            logger.warning(f"No insights database found at {INSIGHTS_DB_PATH}")
            return {"hitter": [], "pitcher": []}
    except Exception as e:
        logger.error(f"Error loading insights database: {e}")
        return {"hitter": [], "pitcher": []}

def enrich_predictions_with_master_data(predictions_df, master_hitter, master_pitcher):
    """Enrich predictions with additional data from master files"""
    if predictions_df.empty:
        return predictions_df

    # Ensure we have the necessary column
    if 'Player' not in predictions_df.columns:
        logger.warning("No 'Player' column in predictions, skipping enrichment")
        return predictions_df

    enriched_df = predictions_df.copy()

    # Create unique row ID for ordering
    enriched_df['row_id'] = range(len(enriched_df))

    # 1) Enrich with hitter data
    if not master_hitter.empty and 'Player' in master_hitter.columns:
        logger.info("Enriching with hitter data")
        unique_hitter_data = master_hitter.drop_duplicates(subset=['Player'])
        enriched_df = pd.merge(
            enriched_df,
            unique_hitter_data,
            on='Player',
            how='left',
            suffixes=('', '_hitter_master')
        )

    # 2) Enrich with pitcher data for pitcher props
    if not master_pitcher.empty and 'Player' in master_pitcher.columns:
        logger.info("Enriching with pitcher data for pitcher props")
        unique_pitcher_data = master_pitcher.drop_duplicates(subset=['Player'])
        pitcher_props = enriched_df[enriched_df['Model_Type'] == 'pitcher'].copy()
        if not pitcher_props.empty:
            pitcher_props = pd.merge(
                pitcher_props,
                unique_pitcher_data,
                on='Player',
                how='left',
                suffixes=('', '_pitcher_master')
            )
            enriched_df.update(pitcher_props)

    # 3) Restore original order and drop helper column
    enriched_df = enriched_df.sort_values('row_id').drop('row_id', axis=1)

    # 4) Merge opposing-pitcher stats onto every row
    if not master_pitcher.empty and 'Player' in master_pitcher.columns:
        logger.info("Merging opposing-pitcher stats onto every row")
        opp = (
            master_pitcher
            .drop_duplicates(subset=['Player'])
            .rename(columns={col: f"Opp_{col}" for col in master_pitcher.columns})
            .set_index('Opp_Player')
        )
        enriched_df = enriched_df.join(
            opp,
            on='Opposing Pitcher',
            how='left'
        )

    logger.info(f"Enrichment complete. DataFrame now has {len(enriched_df.columns)} columns")
    return enriched_df

def build_prompt(row, insights_db=None, pitcher_df=None):
    """Build a prompt for the LLM based on the row data and insights"""
    # Get player name from the Player column
    player_name = row.get('Player', 'Unknown Player')

    # Get opponent pitcher name
    opponent_pitcher = row.get('Opposing Pitcher', 'Unknown Pitcher')

    # Get prop type and value
    prop_type = row.get('Prop Type', 'Unknown Prop')
    prop_value = row.get('Prop Value', 'Unknown Value')

    # Get RF prediction and confidence
    rf_pred = 'Over' if row.get('RF_Prediction', 0) == 1 else 'Under'
    rf_conf = round(row.get('RF_Confidence', 0) * 100, 1)

    # Get model type (hitter or pitcher)
    model_type = row.get('Model_Type', 'unknown').lower()

    # Helper function to handle potentially missing values
    def get_value(key, default='No data'):
        value = row.get(key)
        if value is None or value == 'N/A' or value == '' or pd.isna(value):
            return default
        return value

    # Helper function to get pitcher stats from the pitcher DataFrame
    def get_pitcher_stat(stat, default='No data'):
        val = row.get(f"Opp_{stat}")
        if pd.isna(val) or val in (None, '', 'N/A'):
            return default
        return val

    # Build the base prompt
    prompt = f"""<s>[INST] System: You are a world-class MLB prop betting analyst working alongside an AI model. Your job is to critically evaluate the model's prediction for a player prop bet using detailed statistics and game context.

User: I need your expert analysis on the following MLB prop bet:

You will be given:
1. A specific prop bet (e.g. Hits+Runs+RBIs, Total Bases, Fantasy Score, Strikeouts)
2. The model's Over/Under prediction and confidence level
3. A complete statistical profile of the player, opponent, and game environment

---

🎯 **Your Tasks**
1. State **your** Over/Under pick
2. Say whether the model’s prediction is **reasonable**
3. Give a **1-to-3-sentence** justification (≤ 40 words) with concrete stats
4. Tag your confidence level

🛠️ **Important**: The RF model now has a week's worth of training data, treat it as such. A week in this context is roughly 2200 rows of data.

### Reasoning mode
Think step-by-step **internally**. Do **not** expose your chain-of-thought.  
When finished, output exactly four comma-separated fields on one line:  
`LLM_Prediction,LLM_RF_Agreement,LLM_Confidence,LLM_Justification`

---

📌 **Prop Details**
- **Player**: {player_name}
- **Prop Line**: {prop_type} at {prop_value}
- **Model Prediction**: {rf_pred} (Confidence: {rf_conf}%)
- **Player Type**: {model_type.capitalize()}

---

📊 **Player Stats**

**Season Averages vs RHP:**
- AVG: {get_value('AVG_vs_rhp')} | OBP: {get_value('OBP_vs_rhp')} | SLG: {get_value('SLG_vs_rhp')} | OPS: {get_value('OPS_vs_rhp')}

**Season Averages vs LHP:**
- AVG: {get_value('AVG_vs_lhp')} | OBP: {get_value('OBP_vs_lhp')} | SLG: {get_value('SLG_vs_lhp')} | OPS: {get_value('OPS_vs_lhp')}

**Raw Splits (Total Counts):**  
- vs RHP — AB: {get_value('AB_vs_rhp')} | H: {get_value('H_vs_rhp')} | HR: {get_value('HR_vs_rhp')} | RBI: {get_value('RBI_vs_rhp')} | PA: {get_value('PA_vs_rhp')}  
- vs LHP — AB: {get_value('AB_vs_lhp')} | H: {get_value('H_vs_lhp')} | HR: {get_value('HR_vs_lhp')} | RBI: {get_value('RBI_vs_lhp')} | PA: {get_value('PA_vs_lhp')}

**Rate & Quality Metrics:**  
- wOBA vs RHP: {get_value('wOBA_vs_rhp')} | wOBA vs LHP: {get_value('wOBA_vs_lhp')}  
- xwOBA: {get_value('xwOBA')} | xBA: {get_value('xBA')}  
- Barrel%: {get_value('Barrel%')} | Hard Hit %: {get_value('Hard Hit %')}  
- EV (avg exit velocity): {get_value('EV')} mph

**Plate Discipline:**  
- BB% vs RHP: {get_value('BB%_vs_rhp')} | K% vs RHP: {get_value('K%_vs_rhp')} | ISO vs RHP: {get_value('ISO_vs_rhp')}  
- BB% vs LHP: {get_value('BB%_vs_lhp')} | K% vs LHP: {get_value('K%_vs_lhp')} | ISO vs LHP: {get_value('ISO_vs_lhp')}  

**Recent Form vs RHP (Last 15 Games):**  
- AVG: {get_value('AVG_vs_rhp_15')} | OBP: {get_value('OBP_vs_rhp_15')} | SLG: {get_value('SLG_vs_rhp_15')} | OPS: {get_value('OPS_vs_rhp_15')}

**Recent Form vs LHP (Last 15 Games):**  
- AVG: {get_value('AVG_vs_lhp_15')} | OBP: {get_value('OBP_vs_lhp_15')} | SLG: {get_value('SLG_vs_lhp_15')} | OPS: {get_value('OPS_vs_lhp_15')}

**Pitch-Specific Hard-Hit Metrics:**  
- 4-seam FB HardHit%: {get_value('4seam_fastball_HardHit%')}  
- 4-seam FB RV100: {get_value('4seam_fastball_RV100')}  
- 4-seam FB wOBA: {get_value('4seam_fastball_wOBA')} | 4-seam FB xwOBA: {get_value('4seam_fastball_xwOBA')}
---

📊 **Opponent Info**
**Pitcher Matchup:**
- G–W–L: {get_pitcher_stat('G')}-{get_pitcher_stat('W')}-{get_pitcher_stat('L')} | ERA: {get_pitcher_stat('ERA')}
- SO: {get_pitcher_stat('SO')} | K/9: {get_pitcher_stat('K/9')} | BB/9: {get_pitcher_stat('BB/9')} | K/BB: {get_pitcher_stat('K/BB')}
- HR/9: {get_pitcher_stat('HR/9')} | H/9: {get_pitcher_stat('H/9')}
- K%: {get_pitcher_stat('K%')} | BB%: {get_pitcher_stat('BB%')} | K–BB%: {get_pitcher_stat('K-BB%')}
- AVG Against: {get_pitcher_stat('AVG Against')} | WHIP: {get_pitcher_stat('WHIP')}
- BABIP: {get_pitcher_stat('BABIP')} | LOB%: {get_pitcher_stat('LOB%')}
- ERA-: {get_pitcher_stat('ERA-')} | FIP: {get_pitcher_stat('FIP')} | FIP-: {get_pitcher_stat('FIP-')}

**Pitch Mix (Usage %):**
- Four Seamer: {get_pitcher_stat('Four Seamer')}% | Sinker: {get_pitcher_stat('Sinker')}% | Slider: {get_pitcher_stat('Slider')}% 
- Curveball: {get_pitcher_stat('Curveball')}% | Changeup: {get_pitcher_stat('Changeup')}% | Cutter: {get_pitcher_stat('Cutter')}%
- Split Finger: {get_pitcher_stat('Split Finger')}% | Knuckle Curve: {get_pitcher_stat('Knuckle Curve')}%
- Sweeper: {get_pitcher_stat('Sweeper')}% | Slurve: {get_pitcher_stat('Slurve')}%

**Batted-Ball Profile:**
- Heart: {get_pitcher_stat('Heart_Count')} ({get_pitcher_stat('Heart_Pct')}%)  
- Shadow: {get_pitcher_stat('Shadow_Count')} ({get_pitcher_stat('Shadow_Pct')}%)  
- Chase: {get_pitcher_stat('Chase_Count')} ({get_pitcher_stat('Chase_Pct')}%)  
- Waste: {get_pitcher_stat('Waste_Count')} ({get_pitcher_stat('Waste_Pct')}%)

**Recent Form (15d):**
- FB Velo (avg): {get_pitcher_stat('15_day_fastball_velo')} mph | Spin: {get_pitcher_stat('15_day_fastball_spin')} rpm  
- HardHit%: {get_pitcher_stat('15_day_hard_hit_pct')}% | Barrel%: {get_pitcher_stat('15_day_barrel_pct')}%  
- GB%: {get_pitcher_stat('15_day_gb_pct')}% | FB%: {get_pitcher_stat('15_day_fb_pct')}% | LD%: {get_pitcher_stat('15_day_ld_pct')}%

**Velocity & Spin (30d):**
- FB Velo (avg): {get_pitcher_stat('30_day_fastball_velo')} mph | Spin: {get_pitcher_stat('30_day_fastball_spin')} rpm  
- HardHit%: {get_pitcher_stat('30_day_hard_hit_pct')}% | Barrel%: {get_pitcher_stat('30_day_barrel_pct')}%  
- GB%: {get_pitcher_stat('30_day_gb_pct')}% | FB%: {get_pitcher_stat('30_day_fb_pct')}% | LD%: {get_pitcher_stat('30_day_ld_pct')}%

---

🌦️ **Game Conditions**
- Stadium: {get_value('Stadium')}
- Park Factor (Basic): {get_value('Park_Factor_Basic')}
- Park Factor (HR): {get_value('Park_Factor_HR')}
- Temperature: {get_value('Game-Time Temp (°F)')}°F
- Wind: {get_value('Game-Time Wind Speed (mph)')} mph {get_value('Game-Time Wind Dir (°)')}°
- Wind Effect: {get_value('Game-Time Effect on Hitters')}

📊 **League Baselines (2025 YTD)**
- AVG .244 | OBP .316 | SLG .395 | OPS .711
- wOBA .314 | xwOBA .326
- Hard-Hit% 40.9 | Barrel% 8.6
- K% 22.0 | BB% 8.6

"""
    # Add model type insights section if available
    if insights_db and model_type in insights_db and insights_db[model_type]:
        # Get the 3 most recent insights
        recent_insights = insights_db[model_type][-3:]

        # Add insights section to prompt
        insights_section = "\n\n---\n\n📈 **Historical Model Insights**"

        for i, insight in enumerate(recent_insights):
            date = insight.get('date', 'N/A')
            key_finding = insight.get('strongest_insight', 'N/A')
            key_factors = insight.get('key_factors', [])

            insights_section += f"\n{i + 1}. **{date}**: {key_finding}"

            if key_factors:
                insights_section += f"\n   Key factors: {', '.join(key_factors[:3])}"

        prompt += insights_section

    # Add prop type insights section if available
    if insights_db and 'prop_types' in insights_db and prop_type in insights_db['prop_types']:
        # Get the most recent insight for this prop type
        prop_insights = insights_db['prop_types'][prop_type]
        latest_insight = prop_insights[-1] if prop_insights else {}

        prop_insights_section = "\n\n---\n\n📊 **Prop Type Insights**"

        if 'key_factors' in latest_insight:
            prop_insights_section += f"\n**Key Factors**: {latest_insight['key_factors']}"

        if 'pattern_analysis' in latest_insight:
            prop_insights_section += f"\n**Pattern Analysis**: {latest_insight['pattern_analysis']}"

        if 'strongest_insight' in latest_insight:
            prop_insights_section += f"\n**Strongest Insight**: {latest_insight['strongest_insight']}"

        prompt += prop_insights_section

    # Complete the prompt
    prompt += """

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
    logger.info("Querying LLM...")
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:latest"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=120
        )

        if result.stderr:
            stderr_output = result.stderr.decode("utf-8")
            if stderr_output.strip():
                logger.warning(f"LLM stderr output: {stderr_output}")

        response = result.stdout.decode("utf-8")

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

    # Load insights database
    insights_db = load_insights_database()
    logger.info(
        f"Loaded insights database with {len(insights_db.get('hitter', []))} hitter insights and {len(insights_db.get('pitcher', []))} pitcher insights")

    # Load master data
    master_hitter, master_pitcher = load_master_data()

    # Process predictions with insights
    llm_preds, llm_justifications, llm_agreements, llm_confidences = [], [], [], []

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
        model_type = row.get("Model_Type", "unknown").lower()
        logger.info(f"Processing prediction {idx + 1}/{len(df)} for {player_name} ({model_type})")

        # Build prompt with insights
        prompt = build_prompt(row, insights_db)

        # Query LLM
        response = query_llm(prompt)

        # Parse response
        prediction, agreement, justification, confidence = parse_llm_response(response, row.get("RF_Prediction", 0))

        # Store results
        llm_preds.append(prediction)
        llm_agreements.append(agreement)
        llm_justifications.append(justification)
        llm_confidences.append(confidence)

        logger.info(f"LLM prediction for {player_name}: {prediction}, Agreement: {agreement}, Confidence: {confidence}")

    # Add results to DataFrame
    df["LLM_Prediction"] = llm_preds
    df["LLM_RF_Agreement"] = llm_agreements
    df["LLM_Justification"] = llm_justifications
    df["LLM_Confidence"] = llm_confidences

    # Add this right before df.to_csv(PREDICTIONS_PATH, index=False):
    desired_columns = ['Player', 'Prop Type', 'Prop Value', 'Start Time', 'RF_Prediction',
                       'RF_Confidence', 'Model_Type', 'LLM_Prediction', 'LLM_RF_Agreement',
                       'LLM_Confidence', 'LLM_Justification', 'Actual_Stat', 'Actual_Result',
                       'Reflection']

    # Ensure all desired columns exist (add empty ones if missing)
    for col in desired_columns:
        if col not in df.columns:
            df[col] = None

    # Select only the desired columns in the specified order
    df = df[desired_columns]

    # Overwrite the original predictions CSV with added LLM columns
    df.to_csv(PREDICTIONS_PATH, index=False)
    logger.info(f"LLM-enhanced predictions added to original file: {PREDICTIONS_PATH}")

    df.to_csv(PREDICTIONS_PATH, index=False)
    logger.info(f"LLM-enhanced predictions added to original file: {PREDICTIONS_PATH}")

    # ==== NEW TOP-PICKS SELECTION ====
    valid_conf = {"High", "Medium"}
    mask = (
            (df["LLM_RF_Agreement"] == "True") &
            (df["RF_Confidence"] >= 0.6) &
            (df["LLM_Confidence"].isin(valid_conf))
    )

    top_picks = (
        df[mask]
        .sort_values("RF_Confidence", ascending=False)
        .head(10)
    )

    if top_picks.empty:
        logger.warning("No top picks met the RF/LLM agreement & confidence criteria.")
    else:
        top_picks.to_csv(TOP_PICKS_PATH, index=False)
        logger.info(f"Wrote {len(top_picks)} top picks to {TOP_PICKS_PATH}")


    logger.info("LLM inference pipeline completed")

if __name__ == "__main__":
    main()
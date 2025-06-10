
import pandas as pd
import subprocess
import json
from datetime import datetime

# Config
PREDICTIONS_PATH = "MLB_Results/" + datetime.now().strftime("%Y-%m-%d") + "_mlb_predictions.csv"
OUTPUT_PATH = PREDICTIONS_PATH.replace(".csv", "_with_llm.csv")

# Load daily prediction file
df = pd.read_csv(PREDICTIONS_PATH)

# Helper to format prompt for each row
def build_prompt(row):
    return f"""
You are an expert MLB betting analyst. You will be given:
1. A player prop (e.g., Hits+Runs+RBIs 0.5)
2. A summary of stats for the hitter and opposing pitcher
3. A prediction made by a Random Forest model

Your job is to:
- Determine if the RF prediction is valid (yes/no)
- Provide your own Over/Under prediction
- Justify your reasoning clearly

---

Player: {row['Player_hitter']}
Prop: {row['Prop Type']} at {row['Prop Value']}
RF Prediction: {'Over' if row['RF_Prediction'] == 1 else 'Under'} with confidence {round(row['RF_Confidence']*100, 1)}%

Key Stats:
- AVG vs RHP: {row.get('AVG_vs_rhp', 'N/A')}
- OBP vs RHP: {row.get('OBP_vs_rhp', 'N/A')}
- SLG vs RHP: {row.get('SLG_vs_rhp', 'N/A')}
- OPS vs RHP: {row.get('OPS_vs_rhp', 'N/A')}
- wOBA: {row.get('wOBA', 'N/A')}
- Barrel%: {row.get('Barrel%', 'N/A')}
- EV: {row.get('EV', 'N/A')}
- Opposing Pitcher ERA: {row.get('ERA_pitcher', 'N/A')}
- Pitcher WHIP: {row.get('WHIP_pitcher', 'N/A')}
- K/9: {row.get('K/9_pitcher', 'N/A')}
- Park Factor HR: {row.get('Park_Factor_HR', 'N/A')}
- Game-Time Temp: {row.get('Game-Time Temp (°F)', 'N/A')}
- Wind Speed: {row.get('Game-Time Wind Speed (mph)', 'N/A')}

---

Respond in this exact format:
LLM_Prediction: Over or Under
LLM_RF_Agreement: True or False
LLM_Justification: [brief explanation]
""".strip()

# Helper to call Ollama and get response from phi3:mini
def query_llm(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "phi3:mini"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        return result.stdout.decode("utf-8")
    except Exception as e:
        return f"Error: {str(e)}"

# Run inference row-by-row with logging
llm_preds, llm_justifications, llm_agreements = [], [], []

for _, row in df.iterrows():
    player_name = row.get("Player_hitter", "Unknown")
    print(f"🔍 Prompting LLM for {player_name}...")

    prompt = build_prompt(row)
    response = query_llm(prompt)

    print(f"✅ Response received for {player_name}")

    # Parse results
    try:
        pred = "Over" if "Over" in response else "Under" if "Under" in response else "Unknown"
        agree = "True" if "True" in response else "False" if "False" in response else "Unknown"
        reason_line = [line for line in response.splitlines() if "LLM_Justification:" in line]
        justification = reason_line[0].split("LLM_Justification:")[-1].strip() if reason_line else "No justification found"
    except Exception:
        pred, agree, justification = "Unknown", "Unknown", response.strip()

    llm_preds.append(pred)
    llm_agreements.append(agree)
    llm_justifications.append(justification)

# Append results
df["LLM_Prediction"] = llm_preds
df["LLM_RF_Agreement"] = llm_agreements
df["LLM_Justification"] = llm_justifications

# Save output
df.to_csv(OUTPUT_PATH, index=False)
print(f"LLM-enhanced predictions saved to: {OUTPUT_PATH}")
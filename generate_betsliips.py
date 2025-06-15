import pandas as pd
import json
import os
import re
from datetime import datetime
import logging
from openai import OpenAI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key="")

def load_top_picks(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Top picks file not found: {path}")
    return pd.read_csv(path)

def build_prompt(picks: pd.DataFrame, bankroll: float) -> str:
    picks_json = json.dumps(picks.to_dict(orient="records"), indent=2)

    return f"""You are a PrizePicks betting strategist.

You are given a list of player props and a total bankroll of ${bankroll:.2f}. Your job is to generate the most **mathematically optimal 2–3 leg Power Play slips** possible. Follow the instructions exactly.

🎯 OBJECTIVE:
Maximize **total expected return** across all slips. Use high-confidence, high-EV combinations only. No randomness. No diversity. Only value.

🚫 NON-NEGOTIABLE RULES (MUST FOLLOW EXACTLY):
- Spend **exactly ${bankroll:.2f}** total across all slips (no rounding errors)
- Each slip must contain **2 or 3 different players**
- No player may appear in more than one slip
- No 1-leg slips, no 4+ leg slips
- All slips must be **Power Play** (all legs must hit)
- Fixed payout multipliers:
  - 2-leg = 3×
  - 3-leg = 6×
- Each slip’s "stake" must be ≥ 1.00
- Do **not** use any variables, math expressions, or placeholder logic
- Do **not** output markdown, commentary, or explanation
- Do **not** include invalid JSON — only raw output

📊 STRATEGY:
- Rank picks by "RF_Confidence" (higher is better)
- Favor 2-leg combos of elite confidence unless a 3-leg gives better EV
- EV = stake × multiplier × win_probability
- win_probability = product of "RF_Confidence" values, rounded to 4 decimals
- expected_return = stake × multiplier × win_probability, rounded to 2 decimals
- Allocate more stake to slips with better expected_return
- Stake amounts must sum to exactly ${bankroll:.2f} (round to nearest cent)

📦 OUTPUT FORMAT (STRICT RAW JSON ONLY):
Return a **JSON array** of betslip objects. Each object must include:

- "legs": list of 2 or 3 picks (same structure as input)
  - Each leg must include:
    - "Player"
    - "Prop Type"
    - "Prop Value"
    - "RF_Confidence"
    - "Pick": must be "Over" or "Under", based on model prediction
- "stake": float (e.g. 8.33)
- "payout_multiplier": 3 or 6
- "win_probability": float (product of RF_Confidence values), rounded to 4 decimals
- "expected_return": float (stake × multiplier × win_probability), rounded to 2 decimals

⚠️ WARNING:
- Output must be valid JSON
- Any violation of formatting or constraints invalidates the entire output
- No markdown, comments, or explanations — only JSON

📋 PICKS:
{picks_json}
"""

def query_llm(prompt: str) -> str:
    logger.info("Querying GPT-4 Turbo via OpenAI API...")
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip()

def clean_and_parse_json(raw: str):
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        try:
            # Strip anything before the first [ and after the last ]
            json_like = re.search(r'\[.*\]', raw, re.DOTALL)
            if not json_like:
                raise RuntimeError("No valid JSON array found in LLM response.")
            return json.loads(json_like.group(0))
        except Exception:
            raise RuntimeError("Failed to parse JSON response")

def main():
    today = datetime.now().strftime("%Y-%m-%d")
    input_path = f"MLB_Results/{today}_mlb_top_picks.csv"
    output_path = f"MLB_Results/{today}_generated_betslips.json"

    # Load picks
    df = load_top_picks(input_path)

    # Ask user for bankroll
    try:
        bankroll = float(input("Enter total bankroll (e.g. 25): ").strip())
    except ValueError:
        logger.warning("Invalid bankroll input. Defaulting to $25.")
        bankroll = 25.0

    # Build and send prompt
    prompt = build_prompt(df, bankroll)

    response = query_llm(prompt)
    logger.info("LLM responded. Parsing slips...")

    slips = clean_and_parse_json(response)
    logger.info(f"Parsed {len(slips)} slips")

    # Optional validation
    total_stake = round(sum(slip.get("stake", 0) for slip in slips), 2)
    if total_stake != round(bankroll, 2):
        logger.warning(f"⚠️ Total stake = ${total_stake}, expected ${bankroll:.2f}")

    # Save result
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(slips, f, indent=2)
    logger.info(f"Saved slips to {output_path}")

if __name__ == "__main__":
    main()
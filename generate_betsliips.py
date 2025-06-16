import pandas as pd
import json, requests
import os
import re
from datetime import datetime
import logging
from openai import OpenAI

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key="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")

def load_top_picks(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Top picks file not found: {path}")
    return pd.read_csv(path)

def get_bankroll_info(api_url="http://127.0.0.1:5001/api/bankroll-llm"):
    resp = requests.get(api_url)
    resp.raise_for_status()
    info = resp.json()
    return info["bankroll"], info["net_result_yesterday"], info["yesterday_date"]

def build_prompt(picks: pd.DataFrame, bankroll: float, net_result_yesterday, yesterday_date):
    picks_json = json.dumps(picks.to_dict(orient="records"), indent=2)
    max_stake = int(bankroll * 0.10)
    if max_stake < 1:
        max_stake = 1

    # Summary for the LLM
    if net_result_yesterday is not None and yesterday_date:
        net_str = f"Yesterday ({yesterday_date}), your net result was ${net_result_yesterday:+.2f}."
    else:
        net_str = "This is your first day. No results yet."

    return f"""{net_str} Your current bankroll is ${bankroll:.2f}.
You must not risk more than ${max_stake} total across all slips today (10% of your bankroll, rounded down).

-----
**BETTING PHILOSOPHY AND RULES (READ CAREFULLY):**
- **Quality Over Quantity:** Only bet when you have a clear edge—do NOT force action for the sake of volume. Fewer, high-quality bets are always better than forced volume.
- **Unit Sizing & Risk:** Use small, consistent unit sizes (e.g. 1–2% of bankroll per slip) and NEVER exceed ${max_stake} total staked in a single day (10% of bankroll).
- **Slate-Driven, Not Forced:** The number of bets is determined by value, NOT by the size of the slate. If only 1–2 bets have a real edge, only play those. Some days, no bet is the sharp move.
- **No Chasing or Tilt:** Every bet stands alone. Never increase bet count after losses. Never bet to “catch up.”
- **Market Efficiency:** Prefer picks in soft markets/props where models outperform and oddsmakers are weaker. Avoid main/efficient markets unless the model edge is clear.
- **No Arbitrary Quota:** You are NOT required to risk the full daily cap. On low-confidence days, bet less—or skip. Maximize EV, not action.
- **Line Shopping Logic:** Only generate a slip if the value is there; if you wouldn’t make this bet at the given line, skip it.
-----

You are a PrizePicks betting strategist.

You are given a list of player props and a total bankroll of ${bankroll:.2f}.
Your job is to generate the most **mathematically optimal 2–3 leg Power Play slips** possible, following the philosophy above. If nothing is high-value, generate 0–1 slip with minimum stake, or skip completely. **Never force bets on weak edges.**

🚨 **IMPORTANT:** Never exceed the ${max_stake} daily risk limit. The sum of all "stake" values must be ≤ ${max_stake} today. Fewer slips and lower stakes are OK.

🎯 OBJECTIVE:
Maximize **total expected return** across all slips. Use high-confidence, high-EV combinations only. No randomness. No diversity. Only value.

🚫 NON-NEGOTIABLE RULES (MUST FOLLOW EXACTLY):
- Spend at most ${max_stake} total across all slips today; less is fine if confidence is low.
- Each slip must contain **2 or 3 different players**
- No player may appear in more than one slip
- No 1-leg slips, no 4+ leg slips
- All slips must be **Power Play** (all legs must hit)
- Fixed payout multipliers:
  - 2-leg = 3×
  - 3-leg = 6×
- Each slip’s "stake" must be ≥ 1.00 and ≤ bankroll/2
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
- Stake amounts must sum to **the total you decide to risk for today** (but ≤ ${max_stake} max; less is OK!)

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

    # Get bankroll and yesterday result from dashboard API
    try:
        bankroll, net_result_yesterday, yesterday_date = get_bankroll_info()
        logger.info(f"Fetched bankroll: ${bankroll:.2f}, yesterday result: {net_result_yesterday}")
    except Exception as e:
        logger.warning(f"Failed to fetch bankroll info from API: {e}")
        bankroll, net_result_yesterday, yesterday_date = 500.0, None, None

    prompt = build_prompt(df, bankroll, net_result_yesterday, yesterday_date)
    response = query_llm(prompt)
    logger.info("LLM responded. Parsing slips...")

    slips = clean_and_parse_json(response)
    logger.info(f"Parsed {len(slips)} slips")

    # Save result
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(slips, f, indent=2)
    logger.info(f"Saved slips to {output_path}")

if __name__ == "__main__":
    main()
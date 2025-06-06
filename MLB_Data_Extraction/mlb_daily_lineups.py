#!/usr/bin/env python3
"""
daily_lineups.py

Scrape MLB.com starting lineups for today’s games and write out a CSV
with one row per player (hitters in order, then the starter), containing:
  Team, Player, Position, Handedness
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def parse_handedness(raw: str) -> str:
    """Map a prefix like “(L)”, “(R)”, “(S)” or “RHP”/“LHP” to left/right/switch."""
    if raw.startswith("(L)") or raw == "LHP":
        return "left"
    if raw.startswith("(R)") or raw == "RHP":
        return "right"
    if raw.startswith("(S)"):
        return "switch"
    return ""

def fetch_lineups():
    url = "https://www.mlb.com/starting-lineups"
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    rows = []

    for matchup in soup.select(".starting-lineups__matchup"):
        away = matchup.select_one(
            ".starting-lineups__team-name--away .starting-lineups__team-name--link"
        ).get_text(strip=True)
        home = matchup.select_one(
            ".starting-lineups__team-name--home .starting-lineups__team-name--link"
        ).get_text(strip=True)

        # grab the two pitcher-summary blocks that actually have a name
        pblocks = [
            ps for ps in matchup.select(".starting-lineups__pitcher-summary")
            if ps.select_one(".starting-lineups__pitcher-name")
        ]

        def extract_pitcher(ps):
            name_tag = ps.select_one(".starting-lineups__pitcher-name .starting-lineups__pitcher--link")
            if name_tag is None:
                name_tag = ps.select_one(".starting-lineups__pitcher-name")
            name = name_tag.get_text(strip=True) if name_tag else "Unknown"

            pos_tag = ps.select_one(".starting-lineups__pitcher-pitch-hand")
            pos = pos_tag.get_text(strip=True) if pos_tag else ""
            hand = parse_handedness(pos)

            return name, pos, hand

        away_pitcher = extract_pitcher(pblocks[0]) if len(pblocks) > 0 else (None, None, None)
        home_pitcher = extract_pitcher(pblocks[1]) if len(pblocks) > 1 else (None, None, None)

        # — hitters, desktop view only (no repeats) —
        away_selector = ".starting-lineups__teams--sm .starting-lineups__team--away li.starting-lineups__player"
        home_selector = ".starting-lineups__teams--sm .starting-lineups__team--home li.starting-lineups__player"

        for li in matchup.select(away_selector):
            name = li.select_one(".starting-lineups__player--link").get_text(strip=True)
            raw  = li.select_one(".starting-lineups__player--position").get_text(strip=True)
            pos  = raw.split(")", 1)[-1].strip()      # drop “(L)” etc
            hand = parse_handedness(raw)
            rows.append({
                "Team":       away,
                "Player":     name,
                "Position":   pos,
                "Handedness": hand
            })

        # away starter
        if away_pitcher[0]:
            rows.append({
                "Team":       away,
                "Player":     away_pitcher[0],
                "Position":   away_pitcher[1],
                "Handedness": away_pitcher[2]
            })

        for li in matchup.select(home_selector):
            name = li.select_one(".starting-lineups__player--link").get_text(strip=True)
            raw  = li.select_one(".starting-lineups__player--position").get_text(strip=True)
            pos  = raw.split(")", 1)[-1].strip()
            hand = parse_handedness(raw)
            rows.append({
                "Team":       home,
                "Player":     name,
                "Position":   pos,
                "Handedness": hand
            })

        # home starter
        if home_pitcher[0]:
            rows.append({
                "Team":       home,
                "Player":     home_pitcher[0],
                "Position":   home_pitcher[1],
                "Handedness": home_pitcher[2]
            })

    return rows

def main():
    data = fetch_lineups()
    df   = pd.DataFrame(data, columns=["Team", "Player", "Position", "Handedness"])

    # write into your existing MLB_Prop_Data_CSV folder
    script_dir = os.path.dirname(__file__)
    csv_folder = os.path.abspath(os.path.join(script_dir, "..", "MLB_Prop_Data_CSV"))
    os.makedirs(csv_folder, exist_ok=True)

    out_path = os.path.join(csv_folder, "daily_lineups.csv")
    df.to_csv(out_path, index=False, encoding="utf-8")
    print(f"✅ Daily lineups written to {out_path}")

if __name__ == "__main__":
    main()

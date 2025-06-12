<div id="top">

<!-- HEADER STYLE: CLASSIC -->
<div align="center">


# SPORTS-BETTING-AI

<em>Predict, Win, Dominate with AI-Driven Sports Insights</em>

<!-- BADGES -->
<img src="https://img.shields.io/github/last-commit/willh3518/Sports-betting-AI?style=flat&logo=git&logoColor=white&color=0080ff" alt="last-commit">
<img src="https://img.shields.io/github/languages/top/willh3518/Sports-betting-AI?style=flat&color=0080ff" alt="repo-top-language">
<img src="https://img.shields.io/github/languages/count/willh3518/Sports-betting-AI?style=flat&color=0080ff" alt="repo-language-count">

<em>Built with the tools and technologies:</em>

<img src="https://img.shields.io/badge/JSON-000000.svg?style=flat&logo=JSON&logoColor=white" alt="JSON">
<img src="https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white" alt="Markdown">
<img src="https://img.shields.io/badge/ReadMe-018EF5.svg?style=flat&logo=ReadMe&logoColor=white" alt="ReadMe">
<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">

</div>
<br>

---

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Testing](#testing)
- [Project Structure](#project-structure)
    - [Project Index](#project-index)
- [Contributing](#contributing)
- [Acknowledgment](#acknowledgment)

---

## Overview

Sports-betting-AI is a comprehensive developer toolkit designed to automate sports data collection, analysis, and predictive modeling. It integrates web scraping, machine learning inference, and web deployment to support data-driven sports betting applications. The core features include:

- 🧩 **Data Ingestion:** Automates web scraping and API data collection from MLB, NBA, and sports platforms.
- 🚀 **ML Prediction & Training:** Leverages traditional ML and deep learning models to forecast player performance and game outcomes.
- 🔍 **Proxy Validation:** Ensures network reliability by validating and managing proxy servers for web requests.
- 🌐 **Web Application:** Provides a Flask-based interface for real-time predictions, insights, and analytics.
- ⚡ **Caching & Optimization:** Implements caching mechanisms to enhance performance and reduce latency.
- 📊 **Data Organization:** Structures complex sports data for efficient analysis and decision-making.

---

## Project Structure

```sh
└── Sports-betting-AI/
    ├── Data_Extraction
    │   ├── Did_Prop_Hit.py
    │   ├── H2H_CurrentSeason.py
    │   ├── Home_or_Away.py
    │   ├── Last_10_H2H.py
    │   ├── Last_10_Hit_Percentage.py
    │   ├── Last_10_Season.py
    │   ├── Last_5_Season.py
    │   ├── Main.py
    │   ├── Merge_Data.py
    │   ├── Opponent_Defensive_Rating.py
    │   ├── PrizePicks_Scraper.py
    │   ├── Processing_Data.py
    │   ├── Season_Hit_Percentage.py
    │   ├── Season_Stats.py
    │   ├── Stats_Without_Injured_Starter.py
    │   ├── get_current_player_ids.py
    │   ├── prizepicks_data.csv
    │   └── utils.py
    ├── MLB_Dashboard
    │   ├── app.py
    │   ├── config.py
    │   ├── static
    │   ├── templates
    │   └── utils.py
    ├── MLB_Data_Extraction
    │   ├── MLB_Main.py
    │   ├── create_training_data.py
    │   ├── hitter_stats_merge.py
    │   ├── mlb_daily_lineups.py
    │   ├── mlb_hitter_advanced_stats.py
    │   ├── mlb_hitter_pitcher_hotzones.py
    │   ├── mlb_hitter_vs_pitches.py
    │   ├── mlb_lhp_avg.py
    │   ├── mlb_lhp_last10.py
    │   ├── mlb_lhp_last15.py
    │   ├── mlb_lhp_last5.py
    │   ├── mlb_pitcher_advanced_stats.py
    │   ├── mlb_pitcher_last15_last30.py
    │   ├── mlb_pitcher_pitch_usage.py
    │   ├── mlb_pitchers_stats.py
    │   ├── mlb_prep.log
    │   ├── mlb_prizepicks.py
    │   ├── mlb_rhp_avg.py
    │   ├── mlb_rhp_last10.py
    │   ├── mlb_rhp_last15.py
    │   ├── mlb_rhp_last5.py
    │   ├── mlb_stadium_weather.py
    │   ├── mlb_statcast_stats.py
    │   ├── mlb_utils.py
    │   ├── pitcher_stats_merge.py
    │   ├── prepare_mlb_predictions.py
    │   └── temp.py
    ├── MLB_Logs
    │   ├── events.out.tfevents.1749501690.Mac.20525.0.v2
    │   ├── events.out.tfevents.1749501886.Mac.21791.0.v2
    │   ├── events.out.tfevents.1749502357.Mac.21863.0.v2
    │   ├── events.out.tfevents.1749502571.Mac.21898.0.v2
    │   ├── events.out.tfevents.1749503015.Mac.21968.0.v2
    │   ├── events.out.tfevents.1749582444.Mac.33683.0.v2
    │   ├── events.out.tfevents.1749582444.Mac.33683.1.v2
    │   ├── events.out.tfevents.1749582845.Mac.33760.0.v2
    │   ├── events.out.tfevents.1749582845.Mac.33760.1.v2
    │   ├── events.out.tfevents.1749583001.Mac.33796.0.v2
    │   ├── events.out.tfevents.1749583001.Mac.33796.1.v2
    │   ├── events.out.tfevents.1749585704.Mac.34434.0.v2
    │   ├── events.out.tfevents.1749585704.Mac.34434.1.v2
    │   ├── events.out.tfevents.1749585704.Mac.34434.2.v2
    │   ├── events.out.tfevents.1749608866.Mac.42484.0.v2
    │   ├── events.out.tfevents.1749608866.Mac.42484.1.v2
    │   ├── events.out.tfevents.1749608866.Mac.42484.2.v2
    │   ├── events.out.tfevents.1749657268.Mac.9723.0.v2
    │   └── events.out.tfevents.1749657427.Mac.9774.0.v2
    ├── MLB_Models
    │   ├── mlb_hitter_rf_model.pkl
    │   └── mlb_pitcher_rf_model.pkl
    ├── MLB_Prop_Data_CSV
    │   ├── MLB_Training_Data
    │   ├── Park_factors_2024.csv
    │   ├── ballpark_orientation_with_coords.csv
    │   ├── daily_lineups.csv
    │   ├── hitter_boxscore_results.csv
    │   ├── hitter_training_data.csv
    │   ├── master_hitter_dataset.csv
    │   ├── master_pitcher_dataset.csv
    │   ├── mlb_advanced_vs_lhp.csv
    │   ├── mlb_advanced_vs_rhp.csv
    │   ├── mlb_full_schedule.csv
    │   ├── mlb_hitter_hotzones.csv
    │   ├── mlb_hitter_statcast_stats.csv
    │   ├── mlb_hitter_vs_pitchtype.csv
    │   ├── mlb_last15_avg.csv
    │   ├── mlb_last30_avg.csv
    │   ├── mlb_pitcher_advanced_stats.csv
    │   ├── mlb_pitcher_hotzones.csv
    │   ├── mlb_pitcher_last15.csv
    │   ├── mlb_pitcher_last30.csv
    │   ├── mlb_pitcher_pitch_usage.csv
    │   ├── mlb_pitcher_stats.csv
    │   ├── mlb_prizepicks.csv
    │   ├── mlb_vs_lhp_avg.csv
    │   ├── mlb_vs_lhp_last10.csv
    │   ├── mlb_vs_lhp_last15.csv
    │   ├── mlb_vs_lhp_last5.csv
    │   ├── mlb_vs_rhp_avg.csv
    │   ├── mlb_vs_rhp_last10.csv
    │   ├── mlb_vs_rhp_last15.csv
    │   ├── mlb_vs_rhp_last5.csv
    │   ├── pitcher_boxscore_results.csv
    │   ├── pitcher_training_data.csv
    │   ├── player_fg_ids.csv
    │   ├── stadium_weather_summary.csv
    │   └── team_abbrev_map.csv
    ├── MLB_Results
    │   ├── 2025-06-10_mlb_betslips.json
    │   ├── 2025-06-10_mlb_predictions.csv
    │   ├── 2025-06-10_mlb_top_picks.csv
    │   ├── 2025-06-11_mlb_betslips.csv
    │   ├── 2025-06-11_mlb_predictions.csv
    │   ├── 2025-06-11_mlb_top_picks.csv
    │   ├── 2025-06-12_mlb_betslips.csv
    │   ├── 2025-06-12_mlb_predictions.csv
    │   ├── 2025-06-12_mlb_top_picks.csv
    │   ├── MLB_Prop_Accuracy.csv
    │   └── mlb_insights_db.json
    ├── Machine Learning.py
    ├── Prop_Data_CSV
    │   ├── Constant_CSV
    │   ├── box_scores.csv
    │   ├── final_combined_data.csv
    │   ├── h2h_currentseason.csv
    │   ├── home_away_status.csv
    │   ├── last_10_games_avg.csv
    │   ├── last_10_h2h.csv
    │   ├── last_10_hit_percentage.csv
    │   ├── last_5_games_avg.csv
    │   ├── model_tracking.csv
    │   ├── nba_player_ids.csv
    │   ├── opponent_defensive_ratings.csv
    │   ├── prizepicks_data.csv
    │   ├── processed_data.csv
    │   ├── season_hit_percentage.csv
    │   ├── season_stats.csv
    │   └── season_stats_without_injured_players.csv
    ├── Proxy_testing
    │   ├── proxy_test.py
    │   └── proxyscrape_premium_http_proxies.txt
    ├── README.md
    ├── Tracking_Model_accuracy.py
    ├── allprops_app
    │   ├── __init__.py
    │   ├── access_code.txt
    │   ├── access_config.py
    │   ├── app.py
    │   └── templates
    ├── app
    │   ├── __init__.py
    │   ├── models.py
    │   ├── routes
    │   ├── static
    │   └── templates
    ├── check_proxies.py
    ├── injured_starters.csv
    ├── instance
    │   └── propilot.db
    ├── lineups_projected_minutes.csv
    ├── llm_inference.log
    ├── llm_inference.py
    ├── llm_reflection.py
    ├── logs
    │   ├── events.out.tfevents.1741307874.Wills-MacBook-Pro-2.local.39325.0.v2
    │   ├── events.out.tfevents.1741585565.Wills-MacBook-Pro-2.local.48525.0.v2
    │   ├── events.out.tfevents.1741585565.Wills-MacBook-Pro-2.local.48525.1.v2
    │   ├── events.out.tfevents.1741586139.Wills-MacBook-Pro-2.local.49801.0.v2
    │   ├── events.out.tfevents.1741586578.Wills-MacBook-Pro-2.local.49899.0.v2
    │   ├── events.out.tfevents.1741586612.Wills-MacBook-Pro-2.local.49913.0.v2
    │   ├── events.out.tfevents.1741671931.Wills-MacBook-Pro-2.local.62164.0.v2
    │   ├── events.out.tfevents.1741700173.Wills-MacBook-Pro-2.local.66908.0.v2
    │   ├── events.out.tfevents.1741749623.Wills-MacBook-Pro-2.local.81469.0.v2
    │   ├── events.out.tfevents.1741786998.Wills-MacBook-Pro-2.local.83595.0.v2
    │   ├── events.out.tfevents.1741843280.Wills-MacBook-Pro-2.local.97344.0.v2
    │   ├── events.out.tfevents.1741885670.Wills-MacBook-Pro-2.local.6884.0.v2
    │   ├── events.out.tfevents.1741984265.Wills-MacBook-Pro-2.local.10806.0.v2
    │   ├── events.out.tfevents.1741984928.Wills-MacBook-Pro-2.local.13392.0.v2
    │   ├── events.out.tfevents.1742069039.Wills-MacBook-Pro-2.local.14311.0.v2
    │   ├── events.out.tfevents.1742752138.Wills-MacBook-Pro-2.local.60091.0.v2
    │   ├── events.out.tfevents.1742790293.Wills-MacBook-Pro-2.local.63540.0.v2
    │   ├── events.out.tfevents.1742790440.Wills-MacBook-Pro-2.local.63677.0.v2
    │   ├── events.out.tfevents.1742871714.Wills-MacBook-Pro-2.local.71822.0.v2
    │   ├── events.out.tfevents.1742883508.Wills-MacBook-Pro-2.local.72727.0.v2
    │   ├── events.out.tfevents.1742883532.Wills-MacBook-Pro-2.local.72754.0.v2
    │   ├── events.out.tfevents.1742922593.Wills-MacBook-Pro-2.local.76897.0.v2
    │   ├── events.out.tfevents.1742963744.Wills-MacBook-Pro-2.local.86275.0.v2
    │   ├── events.out.tfevents.1742999374.Wills-MacBook-Pro-2.local.89039.0.v2
    │   ├── events.out.tfevents.1743091870.Wills-MacBook-Pro-2.local.99176.0.v2
    │   ├── events.out.tfevents.1743092409.Wills-MacBook-Pro-2.local.1950.0.v2
    │   ├── events.out.tfevents.1743188945.Wills-MacBook-Pro-2.local.11406.0.v2
    │   ├── events.out.tfevents.1743456947.Wills-MacBook-Pro-2.local.25257.0.v2
    │   ├── events.out.tfevents.1743526279.Wills-MacBook-Pro-2.local.28897.0.v2
    │   ├── events.out.tfevents.1743538877.Wills-MacBook-Pro-2.local.33220.0.v2
    │   ├── events.out.tfevents.1743601225.Wills-MacBook-Pro-2.local.46730.0.v2
    │   ├── events.out.tfevents.1743612099.Wills-MacBook-Pro-2.local.49119.0.v2
    │   ├── events.out.tfevents.1743727826.Wills-MacBook-Pro-2.local.55175.0.v2
    │   ├── events.out.tfevents.1744143443.Wills-MacBook-Pro-2.local.77760.0.v2
    │   ├── events.out.tfevents.1744205895.Wills-MacBook-Pro-2.local.81631.0.v2
    │   ├── events.out.tfevents.1744219126.Wills-MacBook-Pro-2.local.88883.0.v2
    │   ├── events.out.tfevents.1744300156.Wills-MacBook-Pro-2.local.96520.0.v2
    │   ├── events.out.tfevents.1744770878.Wills-MacBook-Pro-2.local.6318.0.v2
    │   ├── events.out.tfevents.1744830617.Wills-MacBook-Pro-2.local.12530.0.v2
    │   ├── events.out.tfevents.1744832787.Wills-MacBook-Pro-2.local.19338.0.v2
    │   ├── events.out.tfevents.1745353589.Wills-MacBook-Pro-2.local.82850.0.v2
    │   ├── events.out.tfevents.1745439948.Wills-MacBook-Pro-2.local.3569.0.v2
    │   ├── events.out.tfevents.1745441353.Wills-MacBook-Pro-2.local.10810.0.v2
    │   ├── events.out.tfevents.1745525902.Wills-MacBook-Pro-2.local.19770.0.v2
    │   ├── events.out.tfevents.1745526697.Wills-MacBook-Pro-2.local.25044.0.v2
    │   ├── events.out.tfevents.1745604367.Wills-MacBook-Pro-2.local.29391.0.v2
    │   ├── events.out.tfevents.1745605890.Wills-MacBook-Pro-2.local.34928.0.v2
    │   ├── events.out.tfevents.1745774360.Wills-MacBook-Pro-2.local.43747.0.v2
    │   ├── events.out.tfevents.1745775562.Wills-MacBook-Pro-2.local.47566.0.v2
    │   ├── events.out.tfevents.1745880279.Wills-MacBook-Pro-2.local.52946.0.v2
    │   ├── events.out.tfevents.1745891441.Wills-MacBook-Pro-2.local.58313.0.v2
    │   ├── events.out.tfevents.1745907624.Wills-MacBook-Pro-2.local.60983.0.v2
    │   ├── events.out.tfevents.1745946605.Wills-MacBook-Pro-2.local.67275.0.v2
    │   ├── events.out.tfevents.1745995364.Wills-MacBook-Pro-2.local.70896.0.v2
    │   ├── events.out.tfevents.1746032512.Wills-MacBook-Pro-2.local.80012.0.v2
    │   ├── events.out.tfevents.1746129444.Wills-MacBook-Pro-2.local.84290.0.v2
    │   ├── events.out.tfevents.1746132813.Wills-MacBook-Pro-2.local.87500.0.v2
    │   ├── events.out.tfevents.1746211812.Wills-MacBook-Pro-2.local.92714.0.v2
    │   ├── events.out.tfevents.1746213061.Wills-MacBook-Pro-2.local.95542.0.v2
    │   ├── events.out.tfevents.1746285741.Wills-MacBook-Pro-2.local.96586.0.v2
    │   ├── events.out.tfevents.1746288288.Wills-MacBook-Pro-2.local.99678.0.v2
    │   ├── events.out.tfevents.1746379117.Wills-MacBook-Pro-2.local.3147.0.v2
    │   ├── events.out.tfevents.1746380267.Wills-MacBook-Pro-2.local.6399.0.v2
    │   ├── events.out.tfevents.1746380512.Wills-MacBook-Pro-2.local.6444.0.v2
    │   ├── events.out.tfevents.1746380762.Wills-MacBook-Pro-2.local.6487.0.v2
    │   ├── events.out.tfevents.1746380897.Wills-MacBook-Pro-2.local.6605.0.v2
    │   ├── events.out.tfevents.1746381123.Wills-MacBook-Pro-2.local.6859.0.v2
    │   ├── events.out.tfevents.1746381159.Wills-MacBook-Pro-2.local.6886.0.v2
    │   ├── events.out.tfevents.1746381289.Wills-MacBook-Pro-2.local.7050.0.v2
    │   ├── events.out.tfevents.1746394335.Wills-MacBook-Pro-2.local.15466.0.v2
    │   ├── events.out.tfevents.1746394488.Wills-MacBook-Pro-2.local.15675.0.v2
    │   ├── events.out.tfevents.1746394688.Wills-MacBook-Pro-2.local.15870.0.v2
    │   ├── events.out.tfevents.1746395297.Wills-MacBook-Pro-2.local.16520.0.v2
    │   ├── events.out.tfevents.1746395320.Wills-MacBook-Pro-2.local.16593.0.v2
    │   ├── events.out.tfevents.1746395391.Wills-MacBook-Pro-2.local.16679.0.v2
    │   ├── events.out.tfevents.1746395518.Wills-MacBook-Pro-2.local.16827.0.v2
    │   ├── events.out.tfevents.1746395534.Wills-MacBook-Pro-2.local.16836.0.v2
    │   ├── events.out.tfevents.1746395604.Wills-MacBook-Pro-2.local.16948.0.v2
    │   ├── events.out.tfevents.1746395675.Wills-MacBook-Pro-2.local.17012.0.v2
    │   ├── events.out.tfevents.1746395760.Wills-MacBook-Pro-2.local.17078.0.v2
    │   ├── events.out.tfevents.1746395804.Wills-MacBook-Pro-2.local.17137.0.v2
    │   ├── events.out.tfevents.1746395910.Wills-MacBook-Pro-2.local.17246.0.v2
    │   ├── events.out.tfevents.1746396001.Wills-MacBook-Pro-2.local.17319.0.v2
    │   ├── events.out.tfevents.1746396075.Wills-MacBook-Pro-2.local.17383.0.v2
    │   ├── events.out.tfevents.1746396158.Wills-MacBook-Pro-2.local.17512.0.v2
    │   ├── events.out.tfevents.1746396225.Wills-MacBook-Pro-2.local.17575.0.v2
    │   ├── events.out.tfevents.1746396310.Wills-MacBook-Pro-2.local.17641.0.v2
    │   ├── events.out.tfevents.1746396379.Wills-MacBook-Pro-2.local.17724.0.v2
    │   ├── events.out.tfevents.1746396511.Wills-MacBook-Pro-2.local.17873.0.v2
    │   ├── events.out.tfevents.1746396652.Wills-MacBook-Pro-2.local.17992.0.v2
    │   ├── events.out.tfevents.1746396800.Wills-MacBook-Pro-2.local.18094.0.v2
    │   ├── events.out.tfevents.1746396966.Wills-MacBook-Pro-2.local.18278.0.v2
    │   ├── events.out.tfevents.1746397065.Wills-MacBook-Pro-2.local.18387.0.v2
    │   ├── events.out.tfevents.1746397168.Wills-MacBook-Pro-2.local.18490.0.v2
    │   ├── events.out.tfevents.1746397352.Wills-MacBook-Pro-2.local.18686.0.v2
    │   ├── events.out.tfevents.1746397473.Wills-MacBook-Pro-2.local.18787.0.v2
    │   ├── events.out.tfevents.1746397707.Wills-MacBook-Pro-2.local.19012.0.v2
    │   ├── events.out.tfevents.1746397714.Wills-MacBook-Pro-2.local.19019.0.v2
    │   ├── events.out.tfevents.1746397723.Wills-MacBook-Pro-2.local.19026.0.v2
    │   ├── events.out.tfevents.1746397728.Wills-MacBook-Pro-2.local.19033.0.v2
    │   ├── events.out.tfevents.1746397733.Wills-MacBook-Pro-2.local.19040.0.v2
    │   ├── events.out.tfevents.1746397737.Wills-MacBook-Pro-2.local.19047.0.v2
    │   ├── events.out.tfevents.1746397753.Wills-MacBook-Pro-2.local.19070.0.v2
    │   ├── events.out.tfevents.1746397757.Wills-MacBook-Pro-2.local.19077.0.v2
    │   ├── events.out.tfevents.1746397764.Wills-MacBook-Pro-2.local.19129.0.v2
    │   ├── events.out.tfevents.1746397768.Wills-MacBook-Pro-2.local.19136.0.v2
    │   ├── events.out.tfevents.1746397773.Wills-MacBook-Pro-2.local.19143.0.v2
    │   ├── events.out.tfevents.1746397780.Wills-MacBook-Pro-2.local.19150.0.v2
    │   ├── events.out.tfevents.1746397784.Wills-MacBook-Pro-2.local.19157.0.v2
    │   ├── events.out.tfevents.1746397787.Wills-MacBook-Pro-2.local.19163.0.v2
    │   ├── events.out.tfevents.1746397790.Wills-MacBook-Pro-2.local.19173.0.v2
    │   ├── events.out.tfevents.1746397794.Wills-MacBook-Pro-2.local.19184.0.v2
    │   ├── events.out.tfevents.1746397799.Wills-MacBook-Pro-2.local.19191.0.v2
    │   ├── events.out.tfevents.1746397804.Wills-MacBook-Pro-2.local.19198.0.v2
    │   ├── events.out.tfevents.1746397809.Wills-MacBook-Pro-2.local.19206.0.v2
    │   ├── events.out.tfevents.1746397816.Wills-MacBook-Pro-2.local.19213.0.v2
    │   ├── events.out.tfevents.1746397821.Wills-MacBook-Pro-2.local.19261.0.v2
    │   ├── events.out.tfevents.1746397828.Wills-MacBook-Pro-2.local.19270.0.v2
    │   ├── events.out.tfevents.1746397833.Wills-MacBook-Pro-2.local.19278.0.v2
    │   ├── events.out.tfevents.1746397837.Wills-MacBook-Pro-2.local.19285.0.v2
    │   ├── events.out.tfevents.1746397867.Wills-MacBook-Pro-2.local.19308.0.v2
    │   ├── events.out.tfevents.1746465234.Wills-MacBook-Pro-2.local.28679.0.v2
    │   ├── events.out.tfevents.1746548720.Wills-MacBook-Pro-2.local.48322.0.v2
    │   ├── events.out.tfevents.1746562738.Wills-MacBook-Pro-2.local.51454.0.v2
    │   ├── events.out.tfevents.1746627367.Wills-MacBook-Pro-2.local.56509.0.v2
    │   ├── events.out.tfevents.1746652775.Wills-MacBook-Pro-2.local.59849.0.v2
    │   ├── events.out.tfevents.1746680940.Wills-MacBook-Pro-2.local.63468.0.v2
    │   ├── events.out.tfevents.1746734925.Wills-MacBook-Pro-2.local.13534.0.v2
    │   ├── events.out.tfevents.1746741276.Wills-MacBook-Pro-2.local.14870.0.v2
    │   ├── events.out.tfevents.1746741377.Wills-MacBook-Pro-2.local.15003.0.v2
    │   ├── events.out.tfevents.1746741480.Wills-MacBook-Pro-2.local.15130.0.v2
    │   ├── events.out.tfevents.1746741729.Wills-MacBook-Pro-2.local.15315.0.v2
    │   ├── events.out.tfevents.1746741746.Wills-MacBook-Pro-2.local.15345.0.v2
    │   ├── events.out.tfevents.1746741778.Wills-MacBook-Pro-2.local.15378.0.v2
    │   ├── events.out.tfevents.1746741982.Wills-MacBook-Pro-2.local.15555.0.v2
    │   ├── events.out.tfevents.1746741990.Wills-MacBook-Pro-2.local.15574.0.v2
    │   ├── events.out.tfevents.1746742671.Wills-MacBook-Pro-2.local.16208.0.v2
    │   ├── events.out.tfevents.1746743088.Wills-MacBook-Pro-2.local.16551.0.v2
    │   ├── events.out.tfevents.1746743184.Wills-MacBook-Pro-2.local.16627.0.v2
    │   ├── events.out.tfevents.1746748086.Wills-MacBook-Pro-2.local.19005.0.v2
    │   ├── events.out.tfevents.1746748206.Wills-MacBook-Pro-2.local.19078.0.v2
    │   ├── events.out.tfevents.1746748236.Wills-MacBook-Pro-2.local.19123.0.v2
    │   ├── events.out.tfevents.1746760870.Wills-MacBook-Pro-2.local.31801.0.v2
    │   ├── events.out.tfevents.1746858282.Wills-MacBook-Pro-2.local.72501.0.v2
    │   ├── events.out.tfevents.1746858419.Wills-MacBook-Pro-2.local.72649.0.v2
    │   ├── events.out.tfevents.1746895252.Wills-MacBook-Pro-2.local.73497.0.v2
    │   ├── events.out.tfevents.1746980159.Wills-MacBook-Pro-2.local.76693.0.v2
    │   ├── events.out.tfevents.1746992133.Wills-MBP-2.78538.0.v2
    │   ├── events.out.tfevents.1747025388.Wills-MacBook-Pro-2.local.88786.0.v2
    │   ├── events.out.tfevents.1747072532.Mac.localdomain.15577.0.v2
    │   ├── events.out.tfevents.1747155060.Wills-MBP-2.localdomain.36563.0.v2
    │   ├── events.out.tfevents.1747155263.Wills-MBP-2.localdomain.36866.0.v2
    │   ├── events.out.tfevents.1747155597.Wills-MBP-2.localdomain.37274.0.v2
    │   ├── events.out.tfevents.1747240088.Wills-MBP-2.localdomain.3930.0.v2
    │   ├── events.out.tfevents.1747245288.Wills-MBP-2.localdomain.6343.0.v2
    │   ├── events.out.tfevents.1747313735.Wills-MBP-2.localdomain.9025.0.v2
    │   ├── events.out.tfevents.1747313852.Wills-MBP-2.localdomain.9105.0.v2
    │   ├── events.out.tfevents.1747415402.Wills-MBP-2.31238.0.v2
    │   ├── events.out.tfevents.1747416535.Wills-MBP-2.31864.0.v2
    │   ├── events.out.tfevents.1747592105.Wills-MBP-2.80902.0.v2
    │   ├── events.out.tfevents.1747594268.Wills-MBP-2.81886.0.v2
    │   ├── events.out.tfevents.1747678796.Wills-MBP-2.5022.0.v2
    │   ├── events.out.tfevents.1747782075.Wills-MacBook-Pro-2.local.24790.0.v2
    │   ├── events.out.tfevents.1747850324.Mac.30315.0.v2
    │   ├── events.out.tfevents.1747850502.Mac.30445.0.v2
    │   ├── events.out.tfevents.1747946300.Mac.36855.0.v2
    │   ├── events.out.tfevents.1747952401.Mac.38316.0.v2
    │   ├── events.out.tfevents.1748129363.Wills-MacBook-Pro-2.local.51429.0.v2
    │   ├── events.out.tfevents.1748129508.Wills-MacBook-Pro-2.local.51475.0.v2
    │   ├── events.out.tfevents.1748328851.Mac.80556.0.v2
    │   ├── events.out.tfevents.1748328902.Mac.80630.0.v2
    │   ├── events.out.tfevents.1748367857.Mac.86472.0.v2
    │   ├── events.out.tfevents.1748474221.Mac.93243.0.v2
    │   ├── events.out.tfevents.1748474606.Mac.93377.0.v2
    │   ├── events.out.tfevents.1748551537.Mac.29508.0.v2
    │   ├── events.out.tfevents.1748552266.Mac.29714.0.v2
    │   ├── events.out.tfevents.1748574034.Mac.76745.0.v2
    │   ├── events.out.tfevents.1748717991.Mac.17110.0.v2
    │   ├── events.out.tfevents.1749153246.Mac.63796.0.v2
    │   └── events.out.tfevents.1749227031.Mac.72268.0.v2
    ├── mlb_actual_results.py
    ├── mlb_machine_learning.py
    ├── mlb_ml.log
    ├── mlb_reflection.log
    ├── model.pkl
    ├── model_tracking.csv
    ├── predictions.csv
    ├── predictions_nn.csv
    ├── prizepicks_json_scraper.py
    ├── projected_minutes.py
    ├── prop_day_alert.py
    ├── proxyscrape_premium_http_proxies.txt
    ├── run.py
    ├── sports-betting-ai.png
    ├── statmusecookies.json
    ├── temp_results.csv
    ├── top5_picks_nn.csv
    ├── top5_picks_rf.csv
    ├── trained_features.txt
    ├── underdog_json_scraper.py
    ├── underdog_props.csv
    ├── user_data
    │   ├── ChromeFeatureState
    │   ├── Default
    │   ├── GrShaderCache
    │   ├── GraphiteDawnCache
    │   ├── Last Version
    │   ├── Local State
    │   ├── RunningChromeVersion
    │   ├── ShaderCache
    │   ├── SingletonCookie
    │   ├── SingletonLock
    │   ├── SingletonSocket
    │   ├── Variations
    │   ├── first_party_sets.db
    │   ├── first_party_sets.db-journal
    │   └── segmentation_platform
    └── working_proxies.txt
```

---

### Project Index

<details open>
	<summary><b><code>SPORTS-BETTING-AI/</code></b></summary>
	<!-- __root__ Submodule -->
	<details>
		<summary><b>__root__</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ __root__</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/llm_inference.py'>llm_inference.py</a></b></td>
					<td style='padding: 8px;'>- The <code>llm_inference.py</code> file serves as the core component responsible for generating and managing predictions related to Major League Baseball (MLB) data within the overall system architecture<br>- Its primary purpose is to process historical and current player data to produce insights, forecasts, and strategic recommendations—such as top player picks and betting slips—that support decision-making workflows<br>- The script consolidates data handling, inference execution, and result storage, ensuring that the system can deliver timely, organized predictions and insights to inform betting strategies or analytical assessments in the MLB domain.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/prizepicks_json_scraper.py'>prizepicks_json_scraper.py</a></b></td>
					<td style='padding: 8px;'>- Prizepicks_json_scraper.pyThis script serves as a dedicated web scraper designed to extract JSON data from the PrizePicks platform<br>- Its primary purpose within the codebase is to automate the retrieval of structured data—likely related to game odds, player stats, or betting information—by sending HTTP requests with specific cookies and headers<br>- The collected data can then be processed, analyzed, or stored for further use, supporting features such as data aggregation, analysis, or decision-making within the larger application architecture<br>- Overall, this component functions as a crucial data ingestion tool, enabling the system to stay updated with real-time or historical data from PrizePicks.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/underdog_json_scraper.py'>underdog_json_scraper.py</a></b></td>
					<td style='padding: 8px;'>- Fetches and processes Underdog Fantasy NBA data to map teams, players, and game props<br>- Generates a structured CSV with current prop lines, detects changes from previous data, and sends real-time alerts via Discord for significant updates<br>- Facilitates monitoring and analysis of player prop movements within the broader fantasy sports data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/projected_minutes.py'>projected_minutes.py</a></b></td>
					<td style='padding: 8px;'>- Fetches and processes NBA player lineup data by automating web scraping from a sports analytics website<br>- Extracts player names and projected minutes, normalizes data, and outputs it into a CSV file for further analysis or integration within the broader sports data architecture<br>- Facilitates real-time updates of player usage metrics for performance tracking and decision-making.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/mlb_machine_learning.py'>mlb_machine_learning.py</a></b></td>
					<td style='padding: 8px;'>- Mlb_machine_learning.pyThis script orchestrates the training and evaluation of machine learning models aimed at analyzing Major League Baseball (MLB) player data<br>- It leverages both traditional machine learning techniques (e.g., Random Forest classifiers) and deep learning frameworks (e.g., TensorFlow) to develop predictive models<br>- The codes primary purpose is to process MLB training datasets, train models to predict player performance or outcomes, and generate evaluation metrics, thereby supporting data-driven insights within the broader MLB analytics architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/check_proxies.py'>check_proxies.py</a></b></td>
					<td style='padding: 8px;'>- Performs validation of proxy servers by testing their connectivity and responsiveness to a specific target URL<br>- Identifies and filters functional proxies, then saves the verified list for subsequent use<br>- This process enhances the reliability of proxy-based operations within the broader system, ensuring only effective proxies are utilized for network requests.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/proxyscrape_premium_http_proxies.txt'>proxyscrape_premium_http_proxies.txt</a></b></td>
					<td style='padding: 8px;'>- Proxy List File (<code>proxyscrape_premium_http_proxies.txt</code>)This file serves as a repository of premium HTTP proxy addresses used within the project<br>- It provides a curated list of proxy endpoints that facilitate anonymous and secure network requests, enabling the application to route traffic through various proxy servers<br>- This setup supports functionalities such as web scraping, data collection, or any operation requiring IP rotation to enhance privacy, avoid rate limiting, or bypass geo-restrictions<br>- Overall, it plays a crucial role in the architecture by supplying reliable proxy configurations that underpin the systems network communication layer.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/statmusecookies.json'>statmusecookies.json</a></b></td>
					<td style='padding: 8px;'>- Defines and manages user tracking and session cookies for the statmuse.com platform, supporting user identification, consent preferences, and personalization<br>- These cookies facilitate user experience continuity, analytics, and targeted interactions within the overall web architecture, ensuring compliance with privacy settings and enhancing site functionality.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/llm_reflection.py'>llm_reflection.py</a></b></td>
					<td style='padding: 8px;'>- Facilitates post-prediction analysis by aggregating MLB betting results, evaluating model accuracy, and generating insights through large language model reflections<br>- It identifies patterns, key factors, and potential biases in predictions, updating a centralized insights database and performance metrics to inform ongoing model improvements and strategic decision-making within the overall architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Tracking_Model_accuracy.py'>Tracking_Model_accuracy.py</a></b></td>
					<td style='padding: 8px;'>- Calculates and logs the accuracy of the random forest models predictions against actual sports betting outcomes<br>- It merges prediction data with real results, computes performance metrics, and appends the results to a tracking CSV for ongoing model evaluation<br>- This process supports continuous monitoring and assessment of model performance within the broader sports betting AI architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/working_proxies.txt'>working_proxies.txt</a></b></td>
					<td style='padding: 8px;'>- Working_proxies.txtThis file serves as a repository of proxy server addresses used within the project<br>- Its primary purpose is to provide a centralized list of proxy IPs and ports that facilitate network requests through different proxies, enhancing anonymity, load distribution, or access to geo-restricted resources<br>- In the broader architecture, this file supports components responsible for managing network traffic, ensuring reliable and scalable proxy utilization across various modules of the system.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/mlb_actual_results.py'>mlb_actual_results.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates and updates MLB player statistics by scraping recent game data, fetching API insights, and calculating fantasy scores<br>- Integrates actual results into prediction workflows, ensuring data accuracy for modeling and analysis<br>- Facilitates seamless data flow across extraction, processing, and result validation within the broader MLB data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/README.md'>README.md</a></b></td>
					<td style='padding: 8px;'>- Provides the core functionalities for automating sports data collection, analysis, and predictive modeling within the sports betting ecosystem<br>- Facilitates web scraping of sports stats, integrates machine learning inference for insights, manages data organization, and supports real-time updates, enabling users to develop data-driven betting tools and analytics seamlessly.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Machine Learning.py'>Machine Learning.py</a></b></td>
					<td style='padding: 8px;'>- Facilitates the training, prediction, and evaluation of a sports betting prop model by processing game data, ensuring feature consistency, and leveraging a Random Forest classifier<br>- Generates actionable insights through predictions, confidence scores, and top picks, while integrating TensorBoard logging for performance tracking<br>- Supports ongoing model refinement and decision-making in a sports analytics architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/run.py'>run.py</a></b></td>
					<td style='padding: 8px;'>- Initialize and launch the web application server, enabling the project to handle incoming requests<br>- It sets up the application instance and runs it in debug mode on a specified host and port, serving as the entry point for the entire systems runtime environment<br>- This file ensures the application is accessible and operational for development and testing purposes.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/trained_features.txt'>trained_features.txt</a></b></td>
					<td style='padding: 8px;'>- Defines a comprehensive set of features and metrics related to basketball game performance, focusing on player and team statistics, opponent ratings, and recent form indicators<br>- Serves as a foundational dataset for modeling and analyzing game outcomes, player efficiency, and strategic insights within the overall architecture of predictive analytics and performance evaluation in the project.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/prop_day_alert.py'>prop_day_alert.py</a></b></td>
					<td style='padding: 8px;'>- Facilitates daily prop updates by generating a unique access code, storing it locally, and notifying stakeholders via Discord webhook<br>- Ensures secure, timely dissemination of the Props of the Day information, integrating with the broader application architecture to support user engagement and access control.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- MLB_Results Submodule -->
	<details>
		<summary><b>MLB_Results</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ MLB_Results</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Results/mlb_insights_db.json'>mlb_insights_db.json</a></b></td>
					<td style='padding: 8px;'>- MLB Insights DatabaseThis JSON file serves as a structured repository of analytical insights and key factors related to predicting baseball player performance metrics, specifically Hits, Runs, and RBIs<br>- It encapsulates expert-driven observations, highlighting the most influential variables and patterns that impact prediction accuracy<br>- By consolidating these insights, the file supports data-driven decision-making and enhances the predictive capabilities of the broader MLB analysis system, ultimately aiding users in making more informed betting or strategic decisions based on player and game dynamics.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Results/2025-06-10_mlb_betslips.json'>2025-06-10_mlb_betslips.json</a></b></td>
					<td style='padding: 8px;'>- Aggregates and presents curated MLB betting predictions for June 10, 2025, highlighting top confidence picks, combined prop insights, and overall overs/unders<br>- It synthesizes model forecasts and contextual justifications to guide betting decisions, emphasizing player performance, game conditions, and prediction confidence levels to support strategic wagering across multiple scenarios.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- allprops_app Submodule -->
	<details>
		<summary><b>allprops_app</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ allprops_app</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/allprops_app/access_config.py'>access_config.py</a></b></td>
					<td style='padding: 8px;'>- Provides a mechanism to generate, store, and retrieve a persistent daily access code, facilitating controlled access within the application<br>- It ensures a unique code is maintained across sessions, supporting security or feature gating by dynamically managing access credentials aligned with the overall system architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/allprops_app/access_code.txt'>access_code.txt</a></b></td>
					<td style='padding: 8px;'>- Stores the access code AP4XMR used for authentication or authorization within the allprops_app architecture<br>- It likely functions as a key component for secure access management, enabling controlled entry to specific features or data<br>- This files purpose is to facilitate seamless and secure user interactions across the applications modules.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/allprops_app/app.py'>app.py</a></b></td>
					<td style='padding: 8px;'>- Provides a web interface for secure access to NBA player props data, integrating multiple data sources to compile detailed player profiles, projected minutes, and betting lines from various platforms<br>- Facilitates data retrieval and presentation within a Flask application, supporting dynamic content delivery for sports betting insights and analysis.</td>
				</tr>
			</table>
			<!-- templates Submodule -->
			<details>
				<summary><b>templates</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ allprops_app.templates</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/allprops_app/templates/allprops.html'>allprops.html</a></b></td>
							<td style='padding: 8px;'>- This HTML template serves as the main user interface for the PropPilot AI application, specifically rendering the All Props page<br>- It provides a structured, styled layout that displays a comprehensive list or overview of properties (props) managed within the system<br>- By integrating Bootstrap for responsive design and theming support, this file ensures a consistent and visually appealing presentation across different themes<br>- Overall, it acts as the central view component, facilitating user interaction with the application's core data—props—within the broader architecture of the PropPilot AI platform.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/allprops_app/templates/enter_code.html'>enter_code.html</a></b></td>
							<td style='padding: 8px;'>- Facilitates secure user access by providing an interface for entering a daily access code, integral to the authentication flow within the application<br>- It ensures that only authorized users can proceed, supporting the overall security architecture and controlled content delivery in the project<br>- This page acts as a gatekeeper, reinforcing access restrictions based on code validation.</td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- user_data Submodule -->
	<details>
		<summary><b>user_data</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ user_data</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Variations'>Variations</a></b></td>
					<td style='padding: 8px;'>- Tracks user experience stability metrics and variation states to monitor application health and stability<br>- It captures whether the user session exited cleanly and maintains crash streak data, contributing to overall system reliability assessments<br>- This component supports the broader architecture by enabling proactive detection of stability issues and informing improvements across the user experience.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/ChromeFeatureState'>ChromeFeatureState</a></b></td>
					<td style='padding: 8px;'>- Defines user-specific Chrome feature configurations, specifying which features are enabled or disabled to tailor browser behavior<br>- It supports the overall architecture by managing feature flags and experimental parameters, ensuring consistent feature rollout and user experience customization across the browser environment.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Last Version'>Last Version</a></b></td>
					<td style='padding: 8px;'>- Provides the latest version identifier for user data, ensuring synchronization and consistency across the system<br>- It serves as a reference point for tracking updates and managing data integrity within the broader architecture, facilitating version control and seamless integration with other components of the project.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/first_party_sets.db-journal'>first_party_sets.db-journal</a></b></td>
					<td style='padding: 8px;'>- Maintains transactional integrity for user data operations within the first-party sets database, ensuring reliable storage and retrieval of user association information<br>- Supports the broader architecture by enabling consistent management of user identities across multiple domains, facilitating privacy-preserving user recognition and data synchronization in the overall system.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Local State'>Local State</a></b></td>
					<td style='padding: 8px;'>- Provides persistent local state data related to user preferences, privacy settings, performance metrics, and profile information within the application<br>- It supports maintaining user experience consistency, optimizing performance, and managing privacy configurations across sessions, thereby ensuring a personalized and efficient user environment within the overall architecture.</td>
				</tr>
			</table>
			<!-- GrShaderCache Submodule -->
			<details>
				<summary><b>GrShaderCache</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ user_data.GrShaderCache</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000012'>f_000012</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the larger graphics rendering system, specifically tailored for the ANGLE Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, such as position, coverage, and color information, to optimize rendering performance<br>- By caching these shader states, the system can quickly retrieve and reuse shader configurations, reducing compilation overhead and ensuring efficient rendering workflows across the applications architecture.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/data_2'>data_2</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content so I can generate the appropriate summary based on the project context.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_00000f'>f_00000f</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the larger graphics rendering system, specifically tailored for the ANGLE Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, such as position and color attributes, to optimize rendering performance and reduce shader compilation overhead during runtime<br>- By caching these shader details, the code contributes to efficient graphics processing within the applications architecture, ensuring smoother rendering workflows and improved overall performance across supported Apple hardware.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_00000c'>f_00000c</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering system, specifically tailored for the ANGLE Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, such as position and color attributes, to optimize rendering performance by enabling quick retrieval and reuse of shader programs during graphics processing<br>- In the context of the overall architecture, this file contributes to efficient graphics rendering workflows by reducing shader compilation overhead, thereby enhancing visual performance and responsiveness across the applications graphical interface.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000002'>f_000002</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering system, specifically tailored for the ANGLE Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, enabling efficient reuse of shader programs during rendering operations<br>- By caching shader information such as positions and local coordinates, it helps optimize rendering performance and reduce compilation overhead, contributing to the overall architectures goal of delivering high-performance graphics rendering on Apple hardware.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/data_0'>data_0</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with any additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000004'>f_000004</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering architecture, specifically tailored for the Apple Metal Renderer using ANGLE<br>- Its primary purpose is to store precompiled shader data, enabling efficient reuse and reducing compilation overhead during rendering operations<br>- By caching shader information such as position and color attributes, it facilitates faster rendering performance and contributes to the overall graphics pipelines efficiency within the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000015'>f_000015</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader graphics rendering system of the project<br>- Its primary purpose is to store precompiled shader data, which facilitates efficient rendering by enabling quick retrieval of shader programs tailored to specific hardware and rendering contexts<br>- Positioned within the user data directory, it supports the projects architecture by optimizing graphics performance, particularly on Apple devices utilizing the ANGLE Metal Renderer<br>- Overall, this file contributes to the seamless and performant rendering pipeline by ensuring that shader resources are readily available and efficiently managed across different hardware configurations.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000016'>f_000016</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the overall graphics rendering architecture<br>- Its primary purpose is to store precompiled shader data associated with specific rendering configurations, such as the Apple ANGLE Metal Renderer<br>- By caching shader information, it enables efficient reuse of shader programs during rendering, reducing load times and improving performance across the graphics pipeline<br>- This component plays a crucial role in optimizing rendering workflows within the project’s architecture, ensuring smooth and efficient graphics processing across supported hardware and rendering contexts.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000010'>f_000010</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering architecture, specifically tailored for the ANGLE (Almost Native Graphics Layer Engine) Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, enabling efficient reuse of shader programs during rendering operations<br>- By caching shader information such as position and color attributes, it helps optimize rendering performance and reduce compilation overhead, contributing to the overall efficiency and responsiveness of the graphics pipeline in the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000003'>f_000003</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering architecture, specifically tailored for the ANGLE (Almost Native Graphics Layer Engine) Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, enabling efficient reuse of shader programs during rendering operations<br>- By caching shader information such as position, color, and circle edge parameters, it helps optimize rendering performance and reduce compilation overhead, contributing to the overall efficiency and responsiveness of the graphics pipeline in the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000008'>f_000008</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the larger rendering system, specifically tailored for the ANGLE Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, which facilitates efficient rendering by reducing shader compilation overhead during runtime<br>- Positioned within the user data directory, it supports optimized graphics performance for applications leveraging Metal on Apple hardware, contributing to the overall architecture by enabling faster, more reliable rendering workflows.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000006'>f_000006</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader graphics rendering architecture<br>- Its primary purpose is to store precompiled shader data associated with specific rendering states, such as position, color, and local coordinates, optimized for the Apple Metal Renderer (specifically on Apple M4 Pro hardware)<br>- By caching these shader parameters, the system can efficiently reuse shader configurations, reducing load times and improving rendering performance across the application<br>- Overall, this file contributes to the architectures goal of delivering high-performance, real-time graphics by enabling rapid shader retrieval and minimizing redundant shader compilation.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_00000b'>f_00000b</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the user data directory, specifically storing precompiled shader data for rendering operations<br>- Its primary purpose is to facilitate efficient graphics rendering by caching shader information tailored to the Apple M4 Pro GPU with the ANGLE Metal Renderer<br>- In the context of the overall architecture, this cache enables rapid shader retrieval, reducing load times and improving rendering performance across the application.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_00000d'>f_00000d</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader graphics rendering architecture<br>- Its primary purpose is to store precompiled shader data, including associated metadata such as rendering context details and resource bindings<br>- By caching this information, the system can efficiently reuse shader programs during rendering, reducing load times and improving performance<br>- Overall, it plays a crucial role in optimizing the graphics pipeline, ensuring smooth and efficient rendering workflows within the application.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_00000a'>f_00000a</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering architecture, specifically tailored for the ANGLE (Almost Native Graphics Layer Engine) Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, enabling efficient reuse of shader programs during rendering operations<br>- By caching shader information such as position and color attributes, it helps optimize rendering performance and reduce compilation overhead, contributing to the overall efficiency and responsiveness of the graphics pipeline in the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000009'>f_000009</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering system, specifically tailored for the ANGLE Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, enabling efficient reuse of shader programs during rendering operations<br>- By caching shader information such as position, coverage, and color attributes, it helps optimize rendering performance and reduce compilation overhead, contributing to the overall efficiency and responsiveness of the graphics pipeline in the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000011'>f_000011</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader graphics rendering system, specifically tailored for the Apple Metal renderer<br>- Its primary purpose is to store precompiled shader data associated with a particular rendering state or asset, enabling efficient reuse and reducing shader compilation overhead during runtime<br>- By caching shader information, it contributes to optimized rendering performance and resource management within the overall graphics architecture of the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000007'>f_000007</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering system, specifically tailored for the ANGLE Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, enabling efficient reuse of shader programs during rendering operations<br>- By caching shader information such as position, color, and circle edge parameters, it facilitates faster rendering performance and reduces runtime compilation overhead, thereby contributing to the overall efficiency and responsiveness of the graphics pipeline in the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_00000e'>f_00000e</a></b></td>
							<td style='padding: 8px;'>- Apple M4 Pro, Version 15.1) environment<br>- This cache enables efficient reuse of shader programs during rendering, reducing load times and improving performance across the graphics pipeline<br>- Overall, it plays a crucial role in optimizing rendering workflows by maintaining readily accessible shader data tailored to the specific hardware and rendering context of the application.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000014'>f_000014</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering system, specifically storing precompiled shader data used by the ANGLE Metal Renderer on Apple devices<br>- Its primary purpose is to facilitate efficient rendering by providing quick access to optimized shader programs tailored for the target hardware and graphics API<br>- By caching these shaders, the system reduces runtime compilation overhead, ensuring smoother graphics performance and faster load times across the applications rendering workflows.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/data_1'>data_1</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to incorporate.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/data_3'>data_3</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to incorporate.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/index'>index</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000005'>f_000005</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering system, specifically storing precompiled shader data used by the rendering engine<br>- Its primary purpose is to facilitate efficient rendering by providing quick access to shader programs tailored for the Apple Metal Renderer, optimizing graphics performance on Apple devices<br>- By caching these shader configurations, the code helps ensure smooth, high-quality visual output within the applications graphics pipeline, contributing to the overall architectures goal of delivering performant and visually rich experiences.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000013'>f_000013</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering system, specifically tailored for the ANGLE (Almost Native Graphics Layer Engine) Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, enabling efficient reuse of shader programs during rendering operations<br>- By caching shader information such as position, coverage, and color attributes, it helps optimize rendering performance and reduce compilation overhead, contributing to the overall efficiency and responsiveness of the graphics pipeline in the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GrShaderCache/f_000001'>f_000001</a></b></td>
							<td style='padding: 8px;'>- This code file functions as a shader cache entry within the broader rendering architecture, specifically tailored for the ANGLE Metal Renderer on Apple devices<br>- Its primary purpose is to store precompiled shader data, enabling efficient reuse of shader programs during rendering operations<br>- By caching shader information such as position, color, and circle edge parameters, it facilitates rapid shader retrieval and minimizes compilation overhead, thereby enhancing rendering performance and consistency across the graphics pipeline<br>- This component plays a crucial role in the overall architecture by supporting optimized, hardware-accelerated graphics rendering on Apple platforms.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- Default Submodule -->
			<details>
				<summary><b>Default</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ user_data.Default</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Top Sites-journal'>Top Sites-journal</a></b></td>
							<td style='padding: 8px;'>- Provides a curated list of top user sites based on browsing activity, enhancing personalized user experience<br>- Integrates with the broader user data management system to deliver quick access to frequently visited sites, supporting efficient navigation and user engagement within the overall architecture<br>- Facilitates data-driven customization aligned with user preferences.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Login Data-journal'>Login Data-journal</a></b></td>
							<td style='padding: 8px;'>- Stores and organizes user login data to facilitate secure authentication processes within the application<br>- It serves as a centralized repository for login credentials, supporting user session management and enhancing overall security architecture<br>- This component integrates with other modules to enable seamless user access and data consistency across the platform.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Shortcuts'>Shortcuts</a></b></td>
							<td style='padding: 8px;'>- Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure<br>- This will help me craft a precise and relevant summary.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Preferences'>Preferences</a></b></td>
							<td style='padding: 8px;'>- Stores user preferences and configuration settings to personalize and optimize the applications behavior<br>- It encompasses accessibility, browsing, security, and account management data, enabling consistent user experiences across sessions<br>- This file integrates with the broader architecture to ensure user-specific customization and seamless functionality within the system.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Reporting and NEL'>Reporting and NEL</a></b></td>
							<td style='padding: 8px;'>- Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure<br>- This will help me craft a precise and relevant summary.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/BrowsingTopicsState'>BrowsingTopicsState</a></b></td>
							<td style='padding: 8px;'>- Defines and maintains the state of user browsing topics, capturing epoch-specific data such as calculation timestamps, model versions, and topic observations<br>- Serves as a persistent record within the broader user data architecture, enabling tracking of browsing behavior patterns and supporting personalized content recommendations over time<br>- Ensures data integrity through embedded security measures like HMAC keys.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/BrowsingTopicsSiteData'>BrowsingTopicsSiteData</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content, as well as the additional project structure details, so I can craft an accurate and succinct summary for you.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Safe Browsing Cookies-journal'>Safe Browsing Cookies-journal</a></b></td>
							<td style='padding: 8px;'>- Facilitates the management and synchronization of Safe Browsing cookies within the user data storage, ensuring secure and consistent browsing experience<br>- Integrates with the broader privacy and security architecture by maintaining cookie journal entries, which support threat detection and user privacy protections across the applications browsing environment.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/trusted_vault.pb'>trusted_vault.pb</a></b></td>
							<td style='padding: 8px;'>- Stores encrypted user trust data within the trusted vault, facilitating secure and reliable management of sensitive information<br>- It integrates seamlessly into the broader data architecture, ensuring that user credentials and trust-related details are protected and accessible for authentication and security processes across the system.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Favicons-journal'>Favicons-journal</a></b></td>
							<td style='padding: 8px;'>- Organizes and manages user-specific favicon preferences within the application, enabling personalized visual branding<br>- Integrates seamlessly into the broader user data management system, ensuring efficient retrieval and storage of favicon choices<br>- Supports a consistent user experience by maintaining individual favicon settings across sessions, contributing to the overall customization and personalization features of the platform.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Visited Links'>Visited Links</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Login Data'>Login Data</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to incorporate.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Reporting and NEL-journal'>Reporting and NEL-journal</a></b></td>
							<td style='padding: 8px;'>- Facilitates the generation and management of user-specific reports and journal entries within the reporting system<br>- Integrates default user data to ensure accurate and personalized documentation, supporting comprehensive analysis and record-keeping across the applications architecture<br>- Enhances data consistency and accessibility for user activity tracking and reporting workflows.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/TransportSecurity'>TransportSecurity</a></b></td>
							<td style='padding: 8px;'>- Defines and manages Transport Security Policies, specifically enforcing HTTPS and HSTS settings for various hosts<br>- It ensures secure communication by specifying expiry, subdomain inclusion, and mode configurations, contributing to the overall security architecture of the system<br>- This file plays a critical role in maintaining consistent transport security standards across the applications network interactions.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/BrowsingTopicsSiteData-journal'>BrowsingTopicsSiteData-journal</a></b></td>
							<td style='padding: 8px;'>- Defines and manages default browsing topics data for user sessions, enabling personalized content recommendations within the browsing experience<br>- Integrates seamlessly into the overall architecture by providing essential topic information, supporting tailored content delivery, and enhancing user engagement across the platform<br>- This component ensures consistent and efficient handling of browsing topics data throughout the system.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/History-journal'>History-journal</a></b></td>
							<td style='padding: 8px;'>- Organizes and manages user history entries within the journal system, enabling efficient storage, retrieval, and updates of user activity logs<br>- Integrates seamlessly into the broader data architecture to support personalized user experiences and activity tracking, ensuring data consistency and accessibility across the application<br>- Facilitates maintaining a comprehensive record of user interactions for analysis and feature enhancement.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Login Data For Account-journal'>Login Data For Account-journal</a></b></td>
							<td style='padding: 8px;'>- Facilitates secure storage and retrieval of user login credentials within the account journal system, supporting seamless user authentication processes<br>- Integrates with the broader data architecture to ensure consistent access to login data, enabling efficient account management and enhancing overall system security and user experience.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Favicons'>Favicons</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to consider.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cookies'>Cookies</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cookies-journal'>Cookies-journal</a></b></td>
							<td style='padding: 8px;'>- Tracks and manages user cookie preferences within the application, ensuring personalized and compliant user experiences<br>- Integrates seamlessly into the broader data handling architecture by storing and retrieving cookie consent data, supporting user privacy choices across sessions<br>- Enhances the system’s ability to adapt to user preferences while maintaining regulatory adherence.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/README'>README</a></b></td>
							<td style='padding: 8px;'>- Defines the handling of user preferences and stored data within Chromium, emphasizing that such information must remain secure and unaltered outside official APIs<br>- Ensures the integrity and privacy of user-specific settings by restricting modifications to authorized methods, thereby maintaining consistent user experience and data security across the browser environment.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/heavy_ad_intervention_opt_out.db-journal'>heavy_ad_intervention_opt_out.db-journal</a></b></td>
							<td style='padding: 8px;'>- Tracks transactional changes and ensures data integrity within the user data database, specifically managing the heavy ad intervention opt-out preferences<br>- Supports reliable updates and consistency for user settings related to ad interventions, contributing to the overall architecture by maintaining accurate user preferences and facilitating seamless user experience across the platform.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Network Persistent State'>Network Persistent State</a></b></td>
							<td style='padding: 8px;'>- Stores persistent network quality data to maintain consistent connectivity information across sessions<br>- It enables the system to recognize and utilize network conditions, such as 4G, ensuring reliable performance and optimized network management within the broader architecture<br>- This data supports adaptive behaviors and enhances user experience by preserving network state information over time.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Web Data'>Web Data</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to incorporate.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Trust Tokens'>Trust Tokens</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/History'>History</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DIPS-journal'>DIPS-journal</a></b></td>
							<td style='padding: 8px;'>- Facilitates the management and organization of user data within the DIPS-journal module, supporting seamless integration and retrieval of journal entries<br>- Enhances the overall data architecture by ensuring consistent handling of user information, thereby enabling efficient access and updates across the application<br>- Contributes to maintaining data integrity and supporting user-centric features within the broader system.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/SCT Auditing Pending Reports'>SCT Auditing Pending Reports</a></b></td>
							<td style='padding: 8px;'>- Facilitates tracking and management of pending SCT audit reports within the user data directory<br>- Supports the overall auditing workflow by organizing reports awaiting review, ensuring timely processing and status updates<br>- Integrates seamlessly into the broader system architecture to maintain audit report visibility and streamline compliance activities across the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Login Data For Account'>Login Data For Account</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Network Action Predictor'>Network Action Predictor</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Affiliation Database-journal'>Affiliation Database-journal</a></b></td>
							<td style='padding: 8px;'>- Facilitates management and retrieval of user affiliation data within the journal database, supporting efficient organization and access to user-related information<br>- Integrates seamlessly into the broader architecture by maintaining structured records, enabling accurate association of users with their respective affiliations, and ensuring data consistency across the platform<br>- Enhances the system’s ability to handle user identity and institutional relationships effectively.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Top Sites'>Top Sites</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the additional project context details.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Affiliation Database'>Affiliation Database</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional project details, so I can craft an accurate and succinct summary for you.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Web Data-journal'>Web Data-journal</a></b></td>
							<td style='padding: 8px;'>- Facilitates the management and organization of user data within the Web Data-journal module, supporting seamless data retrieval and storage<br>- Integrates with the overall architecture to ensure consistent handling of user interactions and data persistence, thereby enabling reliable tracking and analysis of user activity across the platform<br>- Enhances data integrity and accessibility within the broader system.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/LOG'>LOG</a></b></td>
							<td style='padding: 8px;'>- Facilitates the storage and organization of user data logs within the project architecture, ensuring efficient access and management of user activity records<br>- Supports the overall data handling strategy by maintaining a structured log repository, which aids in monitoring, debugging, and analyzing user interactions across the system<br>- Enhances data integrity and retrieval efficiency within the broader application ecosystem.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Shortcuts-journal'>Shortcuts-journal</a></b></td>
							<td style='padding: 8px;'>- Organizes user shortcut configurations within the journal application, enabling personalized and efficient access to frequently used functions<br>- Integrates seamlessly into the overall architecture by supporting user customization and enhancing workflow productivity, contributing to a more intuitive and streamlined user experience across the platform.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/SharedStorage'>SharedStorage</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Safe Browsing Cookies'>Safe Browsing Cookies</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure if available.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DIPS'>DIPS</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/LOCK'>LOCK</a></b></td>
							<td style='padding: 8px;'>- Stores user-specific lock information to manage access control and synchronization within the broader user data management system<br>- Ensures consistent handling of user data access, preventing conflicts and maintaining data integrity across the application<br>- Integrates seamlessly with the overall architecture to support secure, reliable user data operations.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Network Action Predictor-journal'>Network Action Predictor-journal</a></b></td>
							<td style='padding: 8px;'>- Facilitates the prediction of network actions based on user data, enabling personalized and adaptive network management within the overall architecture<br>- Integrates user behavior insights to optimize network performance and security, contributing to a more intelligent and responsive system<br>- Serves as a core component for enhancing user experience through data-driven decision-making in network operations.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/PreferredApps'>PreferredApps</a></b></td>
							<td style='padding: 8px;'>- Defines user preferences for default applications, establishing a baseline configuration within the user data directory<br>- Serves as a foundational component for managing personalized app settings, ensuring consistent user experience across sessions by storing preferred applications and versioning information<br>- Integrates into the broader architecture to facilitate seamless customization and preference persistence.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Trust Tokens-journal'>Trust Tokens-journal</a></b></td>
							<td style='padding: 8px;'>- Facilitates the management and storage of Trust Tokens journal entries within the user data directory, supporting the overall trust token lifecycle and ensuring secure, persistent tracking of token issuance and validation events<br>- This component integrates with the broader architecture to maintain integrity and consistency of trust-related data across user sessions.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Secure Preferences'>Secure Preferences</a></b></td>
							<td style='padding: 8px;'>- Defines user-specific security preferences and extension configurations within a Chromium-based environment, managing permissions, extension states, and security policies<br>- Facilitates personalized and secure browsing experiences by controlling extension behaviors, permissions, and system integrations, ensuring alignment with user and organizational security standards across the entire browser architecture.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/SharedStorage-wal'>SharedStorage-wal</a></b></td>
							<td style='padding: 8px;'>- Facilitates persistent storage of user data within shared storage, ensuring data durability and accessibility across sessions<br>- Integrates seamlessly into the overall architecture by maintaining user-specific information, supporting data synchronization, and enabling reliable data retrieval in the context of the applications data management layer<br>- This enhances user experience through consistent data availability and integrity.</td>
						</tr>
					</table>
					<!-- PersistentOriginTrials Submodule -->
					<details>
						<summary><b>PersistentOriginTrials</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.PersistentOriginTrials</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/PersistentOriginTrials/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Logs user interactions and system events related to persistent origin trials, supporting monitoring and troubleshooting within the user data management framework<br>- Facilitates tracking of trial status and user engagement, ensuring reliable deployment and analysis of feature experiments across the platform<br>- Integrates seamlessly into the broader architecture to maintain data integrity and operational insights.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/PersistentOriginTrials/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manages persistent origin trial configurations for user data, ensuring consistent feature access across sessions<br>- Integrates with the broader user data architecture to maintain trial states, supporting feature rollout strategies and user experience consistency within the project’s data management framework<br>- Facilitates reliable feature flagging and experimentation by preserving trial status across user sessions.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Segmentation Platform Submodule -->
					<details>
						<summary><b>Segmentation Platform</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Segmentation Platform</b></code>
							<!-- SegmentInfoDB Submodule -->
							<details>
								<summary><b>SegmentInfoDB</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Segmentation Platform.SegmentInfoDB</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Segmentation Platform/SegmentInfoDB/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Stores log entries related to user segmentation data management within the SegmentInfoDB component of the Segmentation Platform<br>- Facilitates tracking and troubleshooting of segmentation processes by maintaining a record of relevant events and activities, thereby supporting the overall integrity and reliability of user data segmentation workflows in the project architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Segmentation Platform/SegmentInfoDB/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Manages access control for the SegmentInfoDB within the segmentation platform, ensuring synchronized and exclusive modifications to segmentation data<br>- Facilitates safe concurrent operations by implementing locking mechanisms, thereby maintaining data integrity and consistency across the user data management system in the broader architecture.</td>
										</tr>
									</table>
								</blockquote>
							</details>
							<!-- SignalStorageConfigDB Submodule -->
							<details>
								<summary><b>SignalStorageConfigDB</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Segmentation Platform.SignalStorageConfigDB</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Segmentation Platform/SignalStorageConfigDB/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Stores and manages log data related to segmentation platform signal storage configurations, supporting the overall architecture by enabling efficient tracking and troubleshooting of signal processing activities within the user data management system<br>- Facilitates reliable logging for system monitoring, ensuring data integrity and aiding in diagnosing issues across the segmentation platforms storage components.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Segmentation Platform/SignalStorageConfigDB/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Manages access control and synchronization for the Signal Storage Configuration database within the Segmentation Platform, ensuring safe concurrent operations<br>- Facilitates reliable configuration updates and consistent data integrity across the platform’s user data management system, supporting seamless segmentation processes and stable platform performance.</td>
										</tr>
									</table>
								</blockquote>
							</details>
							<!-- SignalDB Submodule -->
							<details>
								<summary><b>SignalDB</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Segmentation Platform.SignalDB</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Segmentation Platform/SignalDB/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Facilitates logging of segmentation platform signals within the user data management system, ensuring accurate tracking and storage of signal events<br>- Supports the overall architecture by maintaining organized logs that enable efficient analysis and debugging of segmentation-related processes, thereby enhancing the reliability and performance of the platforms data-driven decision-making capabilities.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Segmentation Platform/SignalDB/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Provides a locking mechanism to ensure data integrity during concurrent access within the SignalDB component of the Segmentation Platform<br>- It safeguards the consistency of user data by coordinating access to shared resources, supporting reliable data operations across the platforms architecture<br>- This lock file plays a critical role in maintaining stable and synchronized data management processes.</td>
										</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- Cache Submodule -->
					<details>
						<summary><b>Cache</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Cache</b></code>
							<!-- Cache_Data Submodule -->
							<details>
								<summary><b>Cache_Data</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Cache.Cache_Data</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/82074dd32816c679_0'>82074dd32816c679_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/3bb01aa0d9da6a7b_0'>3bb01aa0d9da6a7b_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/61b8030a84897a1d_0'>61b8030a84897a1d_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis file appears to serve as a cache data component within the user data storage architecture, specifically related to the default cache layer<br>- Its primary purpose is to facilitate quick access and retrieval of user-specific data, thereby enhancing overall system performance and responsiveness<br>- By integrating into the broader cache management system, it helps optimize data handling and reduce latency across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/3883a5f22355dd0a_0'>3883a5f22355dd0a_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/ee70863f6f8af7ba_0'>ee70863f6f8af7ba_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for user-specific assets, enabling efficient retrieval and display within the application<br>- Supports seamless access to visual resources like team logos, ensuring quick load times and reducing network overhead across the overall system architecture<br>- Facilitates optimized user experience by maintaining readily available media assets in the cache.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/328ef90f7eab380d_0'>328ef90f7eab380d_0</a></b></td>
											<td style='padding: 8px;'>- Cache Data File SummaryThis file serves as a cached data store within the user data architecture, specifically holding temporary or persistent information related to user interactions or external data sources<br>- Its primary purpose is to optimize data retrieval and reduce redundant network requests, thereby enhancing overall system performance<br>- Positioned within the cache hierarchy, it supports the broader architecture by enabling quick access to frequently used data, contributing to a more efficient and responsive user experience across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/7f82f5c0c50d1415_0'>7f82f5c0c50d1415_0</a></b></td>
											<td style='padding: 8px;'>- Cache Module SummaryThis code file implements the core caching mechanism responsible for storing and retrieving user data efficiently within the application<br>- It plays a critical role in optimizing performance by minimizing redundant data fetches and ensuring quick access to user-specific information<br>- As part of the overall architecture, this cache module supports seamless data management across different components, contributing to a responsive and scalable user experience.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/6f4e7f8a797d6a8b_0'>6f4e7f8a797d6a8b_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data related to user interactions with statmuse.com, including JavaScript assets and security certificates<br>- Facilitates efficient data retrieval and secure communication within the applications architecture, supporting seamless user experience and reliable content delivery across the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/dffdbfdada8b5861_0'>dffdbfdada8b5861_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/9326246c08f824cf_0'>9326246c08f824cf_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis code file manages cached user data within the applications data architecture, specifically handling storage and retrieval operations for user-specific information<br>- It plays a crucial role in optimizing performance by providing quick access to user data, thereby reducing latency and minimizing redundant data fetches from primary data sources<br>- As part of the broader caching layer, it supports the system's goal of delivering a responsive user experience while maintaining data consistency across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/848cf0972f4facae_0'>848cf0972f4facae_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for efficient retrieval within the application, supporting quick access to visual assets such as team logos<br>- Integrates seamlessly into the broader architecture by enabling optimized content delivery and reducing load times, thereby enhancing user experience and system performance.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/12678018876fe5b2_0'>12678018876fe5b2_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or specify its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/35f0ecba16e8fa9b_0'>35f0ecba16e8fa9b_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached geolocation data and HTTP response metadata to facilitate efficient location-based decision-making within the system<br>- Enhances user experience by enabling rapid access to geographic information, supporting targeted content delivery, and optimizing network interactions across the broader architecture<br>- Ensures data consistency and reduces latency in location-dependent functionalities.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/51619d87874d6155_0'>51619d87874d6155_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure or additional context if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/a40e38aed3182791_0'>a40e38aed3182791_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure details if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/e9f0670ec6ec87b4_0'>e9f0670ec6ec87b4_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript and HTTP response data related to statmuse.com, supporting efficient content delivery and performance optimization within the overall architecture<br>- Facilitates quick access to static assets and response metadata, ensuring reliable and fast user experiences by reducing load times and server requests.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/9cb2a7736d4cd148_0'>9cb2a7736d4cd148_0</a></b></td>
											<td style='padding: 8px;'>- Cache Module SummaryThis code file implements the core caching mechanism responsible for storing and retrieving user data efficiently within the applications architecture<br>- It plays a critical role in optimizing performance by reducing redundant data fetches and ensuring quick access to user-specific information<br>- As a central component of the data management layer, it supports the overall system's responsiveness and scalability by maintaining a consistent and reliable cache state across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1e72de3c6d801a55_0'>1e72de3c6d801a55_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/094f8ab3ae1975b6_0'>094f8ab3ae1975b6_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis file appears to serve as a minimal or placeholder cache entry within the user data cache architecture<br>- Its primary purpose is to facilitate efficient data retrieval and storage by acting as a lightweight cache component, supporting the overall data management and performance optimization strategies of the system<br>- Given its placement within the cache directory, it contributes to the broader architectures goal of maintaining quick access to user-specific data while minimizing redundant data processing.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/6787a93610f118e9_0'>6787a93610f118e9_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/6739d52b2f8f65cb_0'>6739d52b2f8f65cb_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/43736dc5f480ca1b_0'>43736dc5f480ca1b_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1aa05da2b8639791_0'>1aa05da2b8639791_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached, encrypted data related to user interactions and external resource references within the application architecture<br>- Facilitates efficient data retrieval and security by storing session-specific information, ensuring quick access to frequently used assets, and maintaining data integrity across distributed systems<br>- Supports overall system performance and reliability in managing user data and external dependencies.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/ab2dd1a2aa6479e1_0'>ab2dd1a2aa6479e1_0</a></b></td>
											<td style='padding: 8px;'>- Provides client-side rendering logic for dynamic component insertion and slot management within a web application, ensuring seamless hydration and unmounting of components<br>- Integrates with server-side rendering processes to facilitate efficient, interactive user interfaces, supporting the overall architectures focus on modular, responsive, and performant web experiences.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/194fab980a97ecd9_0'>194fab980a97ecd9_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data representing a WebP image retrieved from a remote server, facilitating efficient image loading within the application<br>- Serves as a storage point for quick access to frequently used visual assets, supporting the overall architectures focus on performance optimization and seamless user experience.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/331814da2f1246a4_0'>331814da2f1246a4_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached user data related to network activity and security, supporting efficient data retrieval and validation within the broader system architecture<br>- Facilitates quick access to user-specific information, enhances security protocols, and ensures seamless integration with external services such as domain validation and certificate authorities, thereby maintaining system integrity and performance.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/33fbfad35c0e1fed_0'>33fbfad35c0e1fed_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached, encrypted, and optimized data related to user interactions and external resource references for the statmuse.com platform<br>- Facilitates efficient data retrieval and secure access within the applications architecture, supporting seamless user experience and reliable content delivery across distributed systems.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/f9308e5d38547a6b_0'>f9308e5d38547a6b_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/78f4ef6a30e10ae9_0'>78f4ef6a30e10ae9_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file located at <code>user_data/Default/Cache/C</code> so I can generate an accurate and succinct summary based on its purpose within the overall project architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/f0f97dced4cf13e6_0'>f0f97dced4cf13e6_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/40632ff201e4f643_0'>40632ff201e4f643_0</a></b></td>
											<td style='padding: 8px;'>- Provides core utility functions for managing and processing collections of data, enabling efficient handling of asynchronous operations, deletions, and transformations within the broader application architecture<br>- Facilitates seamless data manipulation and synchronization, supporting the systems caching and data retrieval mechanisms to ensure optimal performance and consistency across the codebase.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/b9b26b321428c0fb_0'>b9b26b321428c0fb_0</a></b></td>
											<td style='padding: 8px;'>- Manages in-memory caching of user-related data, enabling efficient retrieval and storage based on domain and game identifiers<br>- Facilitates quick access to user-specific information within the broader application architecture, supporting performance optimization and data consistency across user sessions<br>- Serves as a core component for maintaining state and reducing redundant data fetches.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/27b8f12a2302363a_0'>27b8f12a2302363a_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/23366a78de74142f_0'>23366a78de74142f_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file <code>user_d</code> or its relevant snippets so I can generate an accurate and succinct summary based on its purpose within the overall project architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/72be7049ca723494_0'>72be7049ca723494_0</a></b></td>
											<td style='padding: 8px;'>- Caches user-specific data to optimize performance and reduce redundant network requests within the application<br>- It stores essential metadata and resource references, enabling faster access and improved responsiveness across user sessions<br>- This component plays a vital role in maintaining efficient data retrieval, supporting the overall architectures goal of delivering a seamless user experience.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/6c9e3a45e0a97c73_0'>6c9e3a45e0a97c73_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/691b724ff422edca_0'>691b724ff422edca_0</a></b></td>
											<td style='padding: 8px;'>- This code file appears to serve as a cache data storage component within the user data architecture, specifically holding temporary or persistent data related to user interactions or session information<br>- Its primary purpose is to facilitate quick data retrieval and efficient management of cached information, thereby supporting the overall systems performance and responsiveness<br>- In the context of the broader codebase, it functions as a crucial element for optimizing data access patterns and maintaining seamless user experiences.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/4a99b18b523729dd_0'>4a99b18b523729dd_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/c1adc40c6b4084e6_0'>c1adc40c6b4084e6_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to analyze, and Ill generate a succinct summary based on the context and project structure you've shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/e6d3c41997144169_0'>e6d3c41997144169_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/a89f4c24e9068118_0'>a89f4c24e9068118_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript helper functions integral to the applications module management and interoperability<br>- Facilitates efficient module loading and compatibility across different environments, supporting the overall architectures modularity and performance<br>- Ensures smooth execution of client-side scripts, contributing to the robustness and responsiveness of the web platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/8ebb8084f6d6f595_0'>8ebb8084f6d6f595_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file located at <code>user_data/Default/Cache</code>, or upload the file so I can review it and generate an accurate summary based on the context and overall project architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/ab51d56190431dc3_0'>ab51d56190431dc3_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data and metadata for user-specific information, facilitating efficient retrieval and offline access within the applications architecture<br>- Ensures quick load times and data consistency by storing pre-fetched content, supporting seamless user experience across sessions<br>- Acts as a crucial component for managing persistent user data in the overall system design.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/5190002dfc6f29b5_0'>5190002dfc6f29b5_0</a></b></td>
											<td style='padding: 8px;'>- Stores cached image and metadata data related to user interactions with statmuse.com, optimizing load times and reducing redundant network requests<br>- Integrates seamlessly into the broader architecture by providing quick access to frequently requested assets, enhancing user experience through efficient data retrieval and caching strategies.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/90e1705dfbb15ffd_0'>90e1705dfbb15ffd_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for user-specific assets, primarily related to visual representations such as team logos<br>- Integrates with the broader system to optimize image retrieval and display, supporting efficient content delivery within the applications architecture<br>- Ensures quick access to frequently used images, enhancing user experience and reducing load times across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/2eed2c674cfce95d_0'>2eed2c674cfce95d_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for user profile assets, optimizing load times and reducing network requests within the application<br>- Integrates seamlessly into the broader architecture by serving pre-fetched visual content, enhancing user experience through faster rendering of images such as team logos and profile pictures<br>- Supports efficient content delivery and caching strategies across the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/e5b1a2252fe06591_0'>e5b1a2252fe06591_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript data related to statistical web resources, supporting efficient data retrieval and performance optimization within the broader application architecture<br>- Facilitates quick access to external scripts and resources, ensuring seamless user experience and reducing latency in data-driven interactions across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/193abfef9d81ceb5_0'>193abfef9d81ceb5_0</a></b></td>
											<td style='padding: 8px;'>- Provides a cached JavaScript utility function for array operations, specifically for finding an index based on a condition<br>- Integrates into the broader codebase by supporting efficient data processing and lookup functionalities, enhancing performance in client-side scripting for the project’s web interface<br>- This component contributes to optimized data handling within the overall architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/18cc3a92bd47e023_0'>18cc3a92bd47e023_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis file serves as a cache data component within the user data management system, specifically storing temporary or persistent user-related information to optimize data retrieval and reduce latency<br>- It plays a crucial role in the overall architecture by enabling efficient access to user data, thereby enhancing the performance and responsiveness of the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/4441db0e5aa1d671_0'>4441db0e5aa1d671_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its key details so I can craft an accurate and succinct summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/8146fa3a22c94a7d_0'>8146fa3a22c94a7d_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/cb55d55ea9aa5a01_0'>cb55d55ea9aa5a01_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis file appears to serve as a cache data artifact within the user data storage system, likely used to optimize data retrieval and improve performance across the application<br>- Positioned within the cache directory, it contributes to the overall architecture by enabling quick access to user-specific data, thereby reducing latency and minimizing redundant data processing throughout the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/944ecacd227cab96_0'>944ecacd227cab96_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached, encrypted, and optimized data for user interactions with statmuse.com, supporting efficient content delivery and reducing load times<br>- Integrates seamlessly within the broader architecture to enhance performance and reliability by serving pre-fetched assets and secure communication channels, ensuring a smooth user experience across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/cbd8ceb9f571cf54_0'>cbd8ceb9f571cf54_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/597be79a9ce6bfea_0'>597be79a9ce6bfea_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data related to user interactions and statistical queries on statmuse.com, supporting efficient data retrieval and offline access within the applications architecture<br>- Enhances performance by minimizing redundant network requests and ensuring quick access to frequently used data, thereby improving user experience and system responsiveness.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/246e5692c5880258_0'>246e5692c5880258_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its key details so I can craft an accurate and succinct summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/8d676452832b58d0_0'>8d676452832b58d0_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/d82ea26b4cbc4cd7_0'>d82ea26b4cbc4cd7_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/0a770eb90824a5f2_0'>0a770eb90824a5f2_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached network response data, including HTTP headers and JSON payloads, to facilitate efficient data retrieval and reduce latency within the applications architecture<br>- Serves as a local storage layer that supports quick access to frequently requested resources, enhancing overall performance and reliability of the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/c20787cea99da4e6_0'>c20787cea99da4e6_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/44494056c333b5b3_0'>44494056c333b5b3_0</a></b></td>
											<td style='padding: 8px;'>- Cache Data File SummaryThis file stores cached user data associated with a specific user session or entity within the applications data architecture<br>- Its primary purpose is to facilitate quick data retrieval and improve overall system performance by temporarily holding relevant user information<br>- Positioned within the cache layer of the project, it supports efficient data access patterns and contributes to the seamless operation of user-related functionalities across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/86f3a575ef8053ea_0'>86f3a575ef8053ea_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/365895fe86d5e1d6_0'>365895fe86d5e1d6_0</a></b></td>
											<td style='padding: 8px;'>- Cache_Data File SummaryThe <code>Cache_Data</code> file within the <code>user_data/Default/Cache</code> directory serves as a centralized storage component responsible for managing cached user data<br>- Its primary purpose is to facilitate quick data retrieval and improve application performance by temporarily storing user-specific information<br>- This file plays a crucial role in the overall architecture by ensuring efficient data access, reducing latency, and maintaining a seamless user experience across the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/14d41de0e9a55aef_0'>14d41de0e9a55aef_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/a97fa0e9713e1b66_0'>a97fa0e9713e1b66_0</a></b></td>
											<td style='padding: 8px;'>- Stores cached image data and metadata for quick retrieval, optimizing performance and reducing redundant network requests within the overall architecture<br>- It facilitates efficient access to visual assets, such as team logos, by maintaining persistent cache entries, thereby enhancing user experience and system responsiveness across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/0640b04e9de42ff6_0'>0640b04e9de42ff6_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data for user-specific information, enabling efficient retrieval and reducing latency within the overall architecture<br>- Facilitates quick access to user data by storing pre-fetched content, thereby optimizing performance and minimizing external requests across the system<br>- Serves as a foundational component for maintaining state and ensuring seamless user experience in the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/dc674b3059c899be_0'>dc674b3059c899be_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/cb48bb60e6a715e0_0'>cb48bb60e6a715e0_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/80b3c46abafcb4d9_0'>80b3c46abafcb4d9_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/99aec3def998c381_0'>99aec3def998c381_0</a></b></td>
											<td style='padding: 8px;'>- Provides JavaScript functions for animating UI elements through opacity and transform transitions, supporting smooth visual effects within the applications interface<br>- Integrates with the overall architecture by enabling dynamic, animated interactions that enhance user experience, aligning with the projects focus on responsive and engaging frontend behavior.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/9f1fd0fec675bd7f_0'>9f1fd0fec675bd7f_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data for user-specific information, likely enhancing performance and reducing latency within the overall architecture<br>- It stores pre-fetched or processed user data, enabling quick access and efficient data retrieval across the system<br>- This component plays a crucial role in optimizing user experience by minimizing redundant data fetches and streamlining data management.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/d9dd443120380922_0'>d9dd443120380922_0</a></b></td>
											<td style='padding: 8px;'>- Cache Data File SummaryThis file serves as a cached data artifact within the user data storage architecture, specifically under the default cache directory<br>- Its primary purpose is to store temporary or pre-processed data related to user information, enabling efficient data retrieval and reducing redundant computations across the application<br>- As part of the overall system, it contributes to optimized performance and streamlined data management within the user data caching layer.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/a62ab64d50522a11_0'>a62ab64d50522a11_0</a></b></td>
											<td style='padding: 8px;'>- Stores cached web content and metadata related to user interactions with statmuse.com, optimizing data retrieval and reducing latency<br>- Facilitates efficient access to frequently requested images and web resources, supporting the applications architecture by enhancing performance and scalability through local cache management.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/e9d423ef625c3e4e_0'>e9d423ef625c3e4e_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis file appears to serve as a cache data component within the user data storage architecture, specifically located in the default cache directory<br>- Its primary purpose is to facilitate efficient data retrieval and storage by temporarily holding user-related information, thereby optimizing performance and reducing redundant data processing across the system<br>- As part of the broader codebase, it contributes to the overall data management strategy, ensuring quick access to user data and supporting seamless user experiences.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/2bc29f7d3ff92d0b_0'>2bc29f7d3ff92d0b_0</a></b></td>
											<td style='padding: 8px;'>- Manages user game state synchronization within the applications architecture by updating and resetting game data in response to state changes<br>- Facilitates seamless data flow between the user interface and backend services, ensuring real-time accuracy of game-related information across the platform<br>- Supports overall system stability and user experience by maintaining consistent state management.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/ab69b23f8a739bc5_0'>ab69b23f8a739bc5_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached OpenSearch description data for StatMuse, enabling efficient search integration within the broader system architecture<br>- Facilitates quick access to sports statistics and related content by storing metadata and search templates, supporting seamless user queries and enhancing the applications search capabilities.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/0acd042b1e029902_0'>0acd042b1e029902_0</a></b></td>
											<td style='padding: 8px;'>- Cache Module SummaryThis code file implements the core caching mechanism within the user data management system<br>- It is responsible for efficiently storing, retrieving, and invalidating user-related data to optimize performance and reduce redundant data fetches<br>- As a central component of the overall architecture, it ensures quick access to user information while maintaining data consistency across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/65c024248d61a30a_0'>65c024248d61a30a_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis file appears to serve as a placeholder or a minimal cache data entry within the user data cache architecture<br>- Its primary purpose is to facilitate efficient data retrieval and storage by acting as a cache node, thereby optimizing performance and reducing redundant data processing across the system<br>- In the context of the overall codebase, it contributes to the caching layer that supports quick access to user-specific data, ensuring a smoother and more responsive user experience.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1c8a766885f9dfdc_0'>1c8a766885f9dfdc_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file youd like summarized, or specify its main functionality if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/5fc501a2e4be2441_0'>5fc501a2e4be2441_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis code file serves as a critical component within the user data caching subsystem, responsible for managing and storing user-specific information efficiently<br>- Its primary purpose is to facilitate quick access and retrieval of user data, thereby enhancing overall system performance and responsiveness<br>- Positioned within the cache directory of the user data architecture, it supports the broader goal of maintaining a scalable and performant user data management framework across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1966a7c2a0fe2301_0'>1966a7c2a0fe2301_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/78c84d2ee914a50c_0'>78c84d2ee914a50c_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data related to user interactions and configuration settings for Amazon ad services, supporting efficient retrieval and management of ad-related information within the broader system architecture<br>- Facilitates quick access to ad configurations, country data, and security certificates, ensuring seamless ad delivery and compliance across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/472d5f5bf3da94a9_0'>472d5f5bf3da94a9_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure details if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/6793282fb9bbebe2_0'>6793282fb9bbebe2_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached network response data related to user interactions with Google services, including content from content-autofill and video platforms<br>- Facilitates efficient retrieval of previously fetched data, reducing latency and network load within the applications architecture<br>- Supports seamless user experience by enabling quick access to frequently accessed external resources.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/01a013e479e06845_0'>01a013e479e06845_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure if necessary.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1513b95e5715d6be_0'>1513b95e5715d6be_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/25de9ff6a50c6565_0'>25de9ff6a50c6565_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for user profile visuals, optimizing load times and reducing external requests within the overall system architecture<br>- Facilitates efficient retrieval and display of user-related images, supporting seamless user experience and performance in the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1ff22ce1e0a6d9ed_0'>1ff22ce1e0a6d9ed_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/88f14d623dff9c4e_0'>88f14d623dff9c4e_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached network response data related to user interactions and API calls within the application<br>- It supports efficient data retrieval and reduces latency by storing frequently accessed information, thereby enhancing overall system performance and user experience across the architecture<br>- This cache file plays a crucial role in maintaining quick access to dynamic content and external service integrations.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/db3d55161bdd0d99_0'>db3d55161bdd0d99_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis code file functions as a critical component within the user data caching layer, responsible for storing and retrieving user-specific data efficiently<br>- It plays a key role in maintaining quick access to user information, thereby enhancing overall system performance and responsiveness<br>- Positioned within the broader architecture, it supports seamless data management and contributes to the scalability of the applications data handling capabilities.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/19ed9cfa7a603149_0'>19ed9cfa7a603149_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached network response data related to user interactions with statmuse.com and Amazon ad systems, supporting efficient data retrieval and reducing latency within the overall architecture<br>- Facilitates seamless user experience by storing relevant HTTP responses and security credentials, ensuring quick access to frequently requested resources across the applications distributed components.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/f83ded245c6fe280_0'>f83ded245c6fe280_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/6f2ba2e9f084f6d5_0'>6f2ba2e9f084f6d5_0</a></b></td>
											<td style='padding: 8px;'>- Caches user data and associated metadata to optimize retrieval and reduce latency within the application architecture<br>- It stores session-specific information, including user preferences and resource references, facilitating efficient access and seamless user experience across sessions<br>- This component plays a vital role in maintaining quick data access and supporting scalable, responsive interactions.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/a1596122373d0584_0'>a1596122373d0584_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure or additional context if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/a3cacfc824f227ff_0'>a3cacfc824f227ff_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis file manages cached user data within the application's architecture, serving as a key component for efficient data retrieval and storage<br>- It ensures quick access to user-specific information, reducing latency and minimizing redundant data processing across the system<br>- By integrating with the broader cache management strategy, this code helps maintain optimal performance and data consistency throughout the platform.---If you can provide the actual content of the file, I can tailor the summary even more precisely.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/510fceb75ab8676d_0'>510fceb75ab8676d_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure or any additional context if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/015e20f6b078d48f_0'>015e20f6b078d48f_0</a></b></td>
											<td style='padding: 8px;'>- Cache Management for User DataThis code file is responsible for handling caching operations within the user data module, specifically managing cached information stored in the <code>user_data/Default/Cache</code> directory<br>- Its primary purpose is to facilitate efficient data retrieval and storage, reducing latency and minimizing redundant data processing across the application<br>- By managing cached user data, it ensures faster access and improved overall performance within the broader system architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/54e37847a5aa84e0_0'>54e37847a5aa84e0_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/056174357a977a45_0'>056174357a977a45_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/e402127384141db5_0'>e402127384141db5_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/bcc0781534e3cc6e_0'>bcc0781534e3cc6e_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file youd like me to summarize.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/5bf4e4eaf2cbc47b_0'>5bf4e4eaf2cbc47b_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript assets and metadata essential for efficient client-side rendering and performance optimization within the overall architecture<br>- Facilitates quick access to static resources, supports secure connections, and ensures content integrity, thereby enhancing user experience and system reliability across the project’s web interface.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/89d4bef5732fcce8_0'>89d4bef5732fcce8_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file located at <code>user_data/Default/Cache/C</code> so I can generate an accurate and succinct summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/c9e50ba76d3b2816_0'>c9e50ba76d3b2816_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/e94db8afecde3a15_0'>e94db8afecde3a15_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to analyze, or specify its content, so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/7d118f1d6f4542c3_0'>7d118f1d6f4542c3_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/7e611d3bdaf84cf3_0'>7e611d3bdaf84cf3_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for user-specific content, enabling efficient retrieval and display within the applications architecture<br>- Facilitates quick access to visual assets associated with user data, supporting seamless user experience and reducing load times across the platform<br>- Serves as a crucial component in managing media assets within the overall system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/b33802e687036815_0'>b33802e687036815_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for user profile visuals, specifically related to NBA team branding<br>- Integrates with the broader data architecture to optimize image retrieval and display, ensuring efficient access to visual assets within the application<br>- Supports seamless user experience by reducing load times and network requests for frequently accessed images.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/3454742852a58f03_0'>3454742852a58f03_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached analytics and configuration data for user session management and third-party integrations within the broader architecture<br>- Facilitates efficient retrieval of user-specific settings, tracking parameters, and external service configurations, supporting seamless data collection, privacy compliance, and system performance optimization across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/c2ff808b234b0d1b_0'>c2ff808b234b0d1b_0</a></b></td>
											<td style='padding: 8px;'>- Provides client-side identity verification functionality for the project, enabling secure user authentication and session management<br>- Integrates with external identity services to ensure reliable user validation, supporting the overall architectures focus on secure data access and personalized user experiences within the application ecosystem.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/caec6afad98ca569_0'>caec6afad98ca569_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/ddbbcd0a03df3324_0'>ddbbcd0a03df3324_0</a></b></td>
											<td style='padding: 8px;'>- Cache Module SummaryThis code file implements the core caching mechanism within the user data management system<br>- It is responsible for efficiently storing, retrieving, and invalidating user-related data to optimize performance and reduce redundant data fetches<br>- As a central component of the overall architecture, it ensures quick access to user information while maintaining data consistency across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/f5d7d8ac3f99eb74_0'>f5d7d8ac3f99eb74_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data for user information, optimizing retrieval efficiency within the overall architecture<br>- Facilitates quick access to user-specific data stored locally, reducing latency and server load, thereby enhancing the responsiveness and scalability of the system<br>- Serves as a foundational component for managing user session and profile data across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/821d791d7edffb36_0'>821d791d7edffb36_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/7934268ce43ad193_0'>7934268ce43ad193_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached and encrypted user data related to network requests and configurations, supporting efficient data retrieval and security within the overall architecture<br>- Facilitates quick access to user-specific information, enhances performance through caching strategies, and ensures secure communication with external services, thereby maintaining the integrity and responsiveness of the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/c4067c3ba7f3fb3a_0'>c4067c3ba7f3fb3a_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript assets and related metadata for statmuse.com, ensuring efficient content delivery and optimized performance within the overall web architecture<br>- Facilitates quick access to essential frontend resources, supporting seamless user interactions and reducing load times across the platform<br>- Acts as a crucial component in the content delivery network, enhancing reliability and scalability.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/8534110f8a5465f6_0'>8534110f8a5465f6_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached user session data and HTTP response metadata for efficient retrieval and validation within the applications data management layer<br>- Facilitates quick access to user authentication status, preferences, and session validity, supporting seamless user experience and security in the overall system architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/25301c63e6167c61_0'>25301c63e6167c61_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/e5af16060c5902f2_0'>e5af16060c5902f2_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript and metadata for statmuse.com, supporting efficient content delivery and performance optimization within the overall architecture<br>- Ensures quick access to static resources, maintains data integrity, and facilitates secure, scalable distribution through CDN infrastructure, contributing to a seamless user experience and robust system performance.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/2ee99d275cfac12b_0'>2ee99d275cfac12b_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached, minified JavaScript data essential for client-side operations within the project architecture<br>- Facilitates efficient retrieval of utility functions and configuration details, supporting seamless integration and performance optimization across the applications components<br>- Ensures quick access to necessary scripts, contributing to overall system responsiveness and stability.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/5220581b675c3d9f_0'>5220581b675c3d9f_0</a></b></td>
											<td style='padding: 8px;'>- Provides a utility function to determine if a specific event plan is enabled based on configuration settings<br>- Integral to feature flag management within the broader application architecture, it supports dynamic feature toggling and conditional behavior, enhancing flexibility and control over user experience and feature rollout strategies.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/d3387ed37c9684f1_0'>d3387ed37c9684f1_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached, encrypted data related to user interactions and session information for the statmuse.com platform<br>- Facilitates quick data retrieval and offline access, supporting overall architecture by enhancing performance, reducing server load, and ensuring data integrity within the client-side caching system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/05faabcd0c5d9370_0'>05faabcd0c5d9370_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached, encrypted metadata and resource references for efficient access and validation within the broader system architecture<br>- Facilitates quick retrieval of essential data such as URLs, security certificates, and response headers, supporting secure and performant interactions with external services like statmuse.com<br>- Ensures data integrity and caching consistency across distributed components.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/da8ba6e6b6ad1256_0'>da8ba6e6b6ad1256_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data related to user interactions and session information within the project architecture<br>- It supports efficient data retrieval and state management, ensuring quick access to user-specific details and enhancing overall system performance<br>- This component plays a crucial role in maintaining persistent user data across sessions, contributing to a seamless user experience.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/7dbbf72a6d39ee8f_0'>7dbbf72a6d39ee8f_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for statmuse.com, enabling efficient retrieval and display of visual assets within the application<br>- Supports seamless user experience by reducing load times and network requests through pre-stored image resources, integrating into the broader architecture of content delivery and caching strategies.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/44b8a3ffa5d79419_0'>44b8a3ffa5d79419_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1ce84af3db7d5b07_0'>1ce84af3db7d5b07_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached user data and associated metadata for efficient retrieval within the system architecture<br>- Facilitates quick access to user-specific information, session details, and security certificates, supporting seamless user experience and secure communication across services<br>- Ensures data consistency and performance optimization in the broader application infrastructure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/47c21a3ba6035716_0'>47c21a3ba6035716_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached, encrypted data related to user interactions and third-party integrations, supporting efficient retrieval and security within the overall architecture<br>- Facilitates quick access to session-specific information and external resource references, ensuring seamless user experience and data integrity across distributed components<br>- Acts as a foundational element for managing persistent user state and external dependencies.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/861bc21641994667_0'>861bc21641994667_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/746543d2160ebefd_0'>746543d2160ebefd_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached network response data, including HTTP headers and encrypted payload, to facilitate efficient data retrieval and offline access within the applications architecture<br>- Supports seamless integration with the broader system by storing essential response metadata and content, enabling optimized performance and reduced latency during subsequent data requests.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1a57a72f30c4b6b6_0'>1a57a72f30c4b6b6_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data related to user interactions and external resource references, supporting efficient data retrieval and offline access within the broader system architecture<br>- Facilitates quick access to user-specific information and external dependencies, ensuring seamless performance and reducing latency across the application<br>- Acts as a foundational component for managing persistent user data and resource caching strategies.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/284985fab2218232_0'>284985fab2218232_0</a></b></td>
											<td style='padding: 8px;'>- Cache Module OverviewThis code file implements the core caching mechanism within the user data management system<br>- Its primary purpose is to efficiently store, retrieve, and manage user data to optimize performance and reduce redundant data processing<br>- Serving as a critical component of the overall architecture, it ensures quick access to frequently used data, thereby enhancing the responsiveness and scalability of the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/8e1f692a92cdb6a3_0'>8e1f692a92cdb6a3_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/cc51259a929823ca_0'>cc51259a929823ca_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript data and metadata for statmuse.com, supporting efficient content delivery and performance optimization within the overall architecture<br>- Facilitates quick access to static resources, ensuring reliable and fast user experiences by leveraging CDN caching strategies and secure content delivery mechanisms<br>- Integral to maintaining the website’s responsiveness and scalability.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/0835285022616013_0'>0835285022616013_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached network response data related to user interactions with various Google services, including content autofill and video uploads<br>- Facilitates efficient data retrieval and reduces latency by storing frequently accessed information locally within the applications cache architecture<br>- Supports seamless user experience through quick access to previously fetched data across multiple Google platforms.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/5e7548fa9e58dc34_0'>5e7548fa9e58dc34_0</a></b></td>
											<td style='padding: 8px;'>- Provides client-side logic for tracking and displaying live game scores within the broader sports analytics platform<br>- Integrates real-time data updates with user interface components, enabling dynamic score visualization based on domain, game ID, and team parameters<br>- Supports seamless user experience by ensuring score data remains current and accurately reflects ongoing game events.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/556e93140de2a344_0'>556e93140de2a344_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript and metadata for statmuse.com, enabling efficient content delivery and reducing load times<br>- Supports secure, fast access to static resources, ensuring reliable website performance and optimal user experience within the overall architecture<br>- Facilitates seamless integration of external scripts and assets, contributing to the sites responsiveness and stability.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/6df0736120e80522_0'>6df0736120e80522_0</a></b></td>
											<td style='padding: 8px;'>- Caches user-specific data to optimize performance and reduce redundant network requests within the application<br>- It stores encrypted response envelopes from external services, facilitating quick data retrieval and seamless user experience<br>- This component is integral to the architecture by ensuring efficient data access and maintaining privacy standards across the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/f0fab48f325d4d95_0'>f0fab48f325d4d95_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached response data and metadata related to user interactions, network requests, and geolocation information<br>- Facilitates efficient retrieval of previously fetched data, supporting performance optimization and seamless user experience within the broader system architecture<br>- Ensures quick access to relevant user context and network responses, contributing to the applications responsiveness and data consistency.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/bb866dbeddd92d8f_0'>bb866dbeddd92d8f_0</a></b></td>
											<td style='padding: 8px;'>- Cache Data File SummaryThis file serves as a cached data store within the user data architecture, specifically holding temporary or persistent data related to user interactions with external resources such as StatMuse<br>- Its primary purpose is to facilitate quick data retrieval and reduce redundant network requests, thereby enhancing overall system performance and responsiveness<br>- Positioned within the cache hierarchy, it supports the broader architectures goal of efficient data management and seamless user experience.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/8ec88ae5f82c2520_0'>8ec88ae5f82c2520_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for user profile visuals, specifically related to NBA team branding<br>- Integrates seamlessly within the broader data architecture to optimize image retrieval and reduce latency, supporting efficient rendering of user interface elements across the application<br>- Enhances overall performance by leveraging cached assets for quick access and display.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/decaf82e725c3d74_0'>decaf82e725c3d74_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript asset data for efficient retrieval within the project’s architecture<br>- Facilitates quick access to static resources, reducing load times and server requests, thereby enhancing overall performance and user experience<br>- Integrates seamlessly with the broader caching strategy to optimize resource delivery across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1c083c798fef3be9_0'>1c083c798fef3be9_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file or its content so I can generate the appropriate summary based on the project context.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/0ac53c891fb7f350_0'>0ac53c891fb7f350_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/e6c885a889b243e8_0'>e6c885a889b243e8_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached data related to user interactions and external resource references within the application<br>- Facilitates efficient data retrieval and reduces latency by storing frequently accessed information, supporting seamless integration with third-party services and ensuring quick access to user-specific and resource-related data across the system architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/fff94d4d419df7db_0'>fff94d4d419df7db_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/500b04e632814b64_0'>500b04e632814b64_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/b8f385e9bcb02b13_0'>b8f385e9bcb02b13_0</a></b></td>
											<td style='padding: 8px;'>- Cache_D File OverviewThis file serves as a critical component within the user data caching subsystem, responsible for managing and storing user-specific data efficiently<br>- It plays a key role in optimizing data retrieval times and reducing redundant data processing across the application, thereby enhancing overall system performance and responsiveness.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/67d5cd9c761754a3_0'>67d5cd9c761754a3_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/d51cfb237fb0c607_0'>d51cfb237fb0c607_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached image data and metadata for user-specific content, enabling efficient retrieval and display within the application<br>- Supports quick access to visual assets like team logos and related images, contributing to optimized performance and seamless user experience across the platforms architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/fb67e85229ac1ad1_0'>fb67e85229ac1ad1_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/79367018e0ec7caf_0'>79367018e0ec7caf_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript data related to user interactions on statmuse.com, supporting efficient content delivery and performance optimization within the broader web architecture<br>- Facilitates quick access to static resources, ensuring seamless user experience and reducing server load through effective caching strategies<br>- Integral to maintaining fast, reliable access to essential frontend assets across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/2d79fddf9276e1aa_0'>2d79fddf9276e1aa_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/776999992487e149_0'>776999992487e149_0</a></b></td>
											<td style='padding: 8px;'>- Implements a reactive data management system to facilitate real-time updates and event-driven interactions within the application<br>- It enables efficient state sharing and synchronization across components, supporting dynamic user experiences<br>- This core mechanism underpins the architectures responsiveness, ensuring seamless data flow and consistent UI behavior throughout the project.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/96fb81ffd5d6d5bc_0'>96fb81ffd5d6d5bc_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/e62713a0a531cf3e_0'>e62713a0a531cf3e_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript utilities for string conversion and object handling, supporting efficient data processing within the broader architecture<br>- Facilitates consistent data serialization and deserialization, enhancing performance and reliability across client-server interactions in the project’s web-based environment<br>- Integral to maintaining optimized data flow and reducing redundant computations in the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/4ab2aaa10b68aa5f_0'>4ab2aaa10b68aa5f_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis file appears to serve as a cache data artifact within the user data storage architecture, specifically located under the <code>user_data/Default/Cache/Cache_Data</code> directory<br>- Its primary purpose is to facilitate quick data retrieval and improve performance by temporarily storing user-specific information<br>- As part of the overall system, it contributes to efficient data management and seamless user experience by minimizing redundant data processing.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/bd2590d03038058e_0'>bd2590d03038058e_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/67b23fc32f41f2fe_0'>67b23fc32f41f2fe_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/8a4cfc35cc1f7f62_0'>8a4cfc35cc1f7f62_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/ed3434361b27fc2e_0'>ed3434361b27fc2e_0</a></b></td>
											<td style='padding: 8px;'>- Cache_Data File OverviewThis file serves as a core component of the caching layer within the user data management system<br>- Its primary purpose is to efficiently store and retrieve user-specific data, enabling faster access and reducing redundant data processing across the application<br>- By integrating this cache, the overall architecture benefits from improved performance and scalability, ensuring that user data operations are optimized for responsiveness and resource utilization.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/bc14bdb0c098560c_0'>bc14bdb0c098560c_0</a></b></td>
											<td style='padding: 8px;'>- Caches API response data related to revenue source mappings for quick retrieval and reduced latency<br>- It supports efficient data access within the overall architecture by minimizing external API calls, ensuring faster response times and improved performance for revenue-related functionalities<br>- This cache file plays a vital role in maintaining data consistency and optimizing resource utilization across the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/index'>index</a></b></td>
											<td style='padding: 8px;'>- Stores and manages cached user data to optimize retrieval efficiency within the overall system architecture<br>- By maintaining quick access to user-specific information, it supports seamless user experiences and reduces latency across the application<br>- Positioned within the user data cache hierarchy, it plays a vital role in ensuring data consistency and performance in the broader project ecosystem.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/7efa59dd2078ed8f_0'>7efa59dd2078ed8f_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached JavaScript assets related to theme switching for the statmuse.com website, supporting efficient loading and consistent user experience<br>- Integrates theme toggle functionality within the broader web application architecture, ensuring seamless visual customization across sessions<br>- Acts as a static resource to optimize performance and maintainability of the sites frontend interface.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/cf1546f4201d97ea_0'>cf1546f4201d97ea_0</a></b></td>
											<td style='padding: 8px;'>- Provides cached, encrypted data related to user interactions and external resource references for statmuse.com<br>- Facilitates efficient data retrieval and offline access within the broader application architecture, supporting seamless user experience and reducing load times by storing essential assets and metadata locally.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/453f73307e95b3f3_0'>453f73307e95b3f3_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its relevant snippets so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/f154076baa8ac027_0'>f154076baa8ac027_0</a></b></td>
											<td style='padding: 8px;'>- Provides a JavaScript utility to convert floating-point numbers to integers, ensuring precise numerical operations within the broader data processing architecture<br>- Facilitates consistent data transformations across the codebase, supporting accurate calculations and data integrity in client-side or server-side computations related to user analytics or content rendering.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/26ec60a3199e09e7_0'>26ec60a3199e09e7_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file youd like a summary for, or specify its main functionality if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/1b642d685d2885ec_0'>1b642d685d2885ec_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure or additional context if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/40ce3b3aae7a7bb6_0'>40ce3b3aae7a7bb6_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis code file is responsible for managing cached user data within the applications architecture<br>- It plays a crucial role in optimizing data retrieval and storage efficiency by handling user-specific information locally<br>- As part of the broader system, it ensures quick access to user data, reducing latency and server load, thereby enhancing overall performance and user experience.</td>
										</tr>
									</table>
									<!-- index-dir Submodule -->
									<details>
										<summary><b>index-dir</b></summary>
										<blockquote>
											<div class='directory-path' style='padding: 8px 0; color: #666;'>
												<code><b>⦿ user_data.Default.Cache.Cache_Data.index-dir</b></code>
											<table style='width: 100%; border-collapse: collapse;'>
											<thead>
												<tr style='background-color: #f8f9fa;'>
													<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
													<th style='text-align: left; padding: 8px;'>Summary</th>
												</tr>
											</thead>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Cache/Cache_Data/index-dir/the-real-index'>the-real-index</a></b></td>
													<td style='padding: 8px;'>- Provides a key component of the caching mechanism within the project’s architecture, enabling efficient data retrieval and storage<br>- By maintaining an index directory, it facilitates quick access to cached user data, supporting overall system performance and responsiveness<br>- This file plays a crucial role in organizing and managing cached information to optimize data handling across the application.</td>
												</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- GCM Store Submodule -->
					<details>
						<summary><b>GCM Store</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.GCM Store</b></code>
							<!-- Encryption Submodule -->
							<details>
								<summary><b>Encryption</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.GCM Store.Encryption</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/GCM Store/Encryption/MANIFEST-000001'>MANIFEST-000001</a></b></td>
											<td style='padding: 8px;'>- Defines the structure and comparison logic for data stored within the LevelDB database used in the GCM Store encryption layer<br>- It ensures consistent bytewise ordering of encrypted user data, facilitating efficient storage, retrieval, and integrity verification within the overall data management architecture<br>- This component is essential for maintaining reliable and performant encrypted data operations.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/GCM Store/Encryption/CURRENT'>CURRENT</a></b></td>
											<td style='padding: 8px;'>- Provides a manifest reference for the current encryption state within the GCM Store, ensuring data integrity and version control<br>- It plays a crucial role in maintaining consistent encryption configurations across the user data management system, supporting secure data storage and retrieval processes within the overall architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/GCM Store/Encryption/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Manages encryption-related database initialization and maintenance within the GCM Store component, ensuring secure storage of sensitive data<br>- It verifies the existence of necessary directories and database files, creating them if absent, and maintains logs of these operations to support reliable data encryption workflows integral to the overall security architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/GCM Store/Encryption/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Provides a secure encryption lock mechanism for user data within the GCM Store, ensuring data confidentiality and integrity<br>- It plays a critical role in safeguarding sensitive user information by managing encryption keys and enforcing access controls, thereby maintaining the overall security architecture of the data storage system.</td>
										</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- AutofillStrikeDatabase Submodule -->
					<details>
						<summary><b>AutofillStrikeDatabase</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.AutofillStrikeDatabase</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/AutofillStrikeDatabase/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Logs user autofill activity within the AutofillStrikeDatabase, capturing events and interactions related to user data input<br>- Serves as a crucial component for monitoring, troubleshooting, and analyzing autofill performance and security, thereby supporting the overall integrity and reliability of the user data management system in the project architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/AutofillStrikeDatabase/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manages synchronization and access control for the AutofillStrikeDatabase, ensuring data integrity during concurrent operations<br>- It functions as a lock mechanism within the user data storage architecture, preventing conflicts and maintaining consistency across user autofill data interactions<br>- This component is essential for coordinating safe database modifications in the overall system.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- shared_proto_db Submodule -->
					<details>
						<summary><b>shared_proto_db</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.shared_proto_db</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/shared_proto_db/MANIFEST-000001'>MANIFEST-000001</a></b></td>
									<td style='padding: 8px;'>- Defines the structure and versioning information for the shared protocol database within the user data management system<br>- It ensures consistent data comparison and ordering across the application, facilitating reliable storage and retrieval of user-related information<br>- This manifest file plays a crucial role in maintaining data integrity and compatibility within the overall database architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/shared_proto_db/CURRENT'>CURRENT</a></b></td>
									<td style='padding: 8px;'>- Defines the current state of shared user data schemas within the project, serving as a manifest that tracks the latest protocol buffer versions<br>- Facilitates consistent data serialization and interoperability across components, ensuring seamless integration and data management within the overall architecture<br>- Acts as a reference point for maintaining schema version control and synchronization.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/shared_proto_db/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Manages database initialization and access within the project, ensuring the shared protocol buffer database is created if missing and reusing existing database files<br>- Facilitates reliable data storage and retrieval for the sports betting AI system, supporting seamless data management across different components of the architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/shared_proto_db/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manage access control and synchronization for shared user data within the database system<br>- Ensures that concurrent operations on user data are properly coordinated, maintaining data integrity and consistency across distributed components<br>- Integral to the overall architecture by facilitating safe, reliable interactions with user-specific information stored in the shared proto database.</td>
								</tr>
							</table>
							<!-- metadata Submodule -->
							<details>
								<summary><b>metadata</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.shared_proto_db.metadata</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/shared_proto_db/metadata/MANIFEST-000001'>MANIFEST-000001</a></b></td>
											<td style='padding: 8px;'>- Defines the metadata for the shared protocol database within the user data module, establishing the structure and comparison logic used for efficient data storage and retrieval<br>- Serves as a foundational component that ensures consistent data organization across the database, facilitating reliable access and integrity within the overall architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/shared_proto_db/metadata/CURRENT'>CURRENT</a></b></td>
											<td style='padding: 8px;'>- Defines the current state of the shared protocol database metadata, serving as a versioned manifest that tracks the latest schema and configuration updates within the user data architecture<br>- It ensures consistent access to protocol definitions across the system, facilitating reliable data synchronization and integrity within the overall project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/shared_proto_db/metadata/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Establishes and manages the metadata storage for the shared protocol database, ensuring the creation and reuse of essential database files<br>- Facilitates consistent access to metadata information, supporting the overall data integrity and operational stability of the project’s database layer within the sports betting AI system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/shared_proto_db/metadata/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Defines a synchronization lock mechanism to coordinate access to shared metadata resources within the user data database<br>- Ensures data integrity and consistency during concurrent operations by preventing conflicting modifications, thereby supporting reliable multi-process interactions in the overall system architecture.</td>
										</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- optimization_guide_hint_cache_store Submodule -->
					<details>
						<summary><b>optimization_guide_hint_cache_store</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.optimization_guide_hint_cache_store</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/optimization_guide_hint_cache_store/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Stores cached optimization hints related to user data to enhance the efficiency of the optimization guide<br>- It facilitates quick retrieval and management of hint data, supporting the overall architectures goal of delivering personalized and performant user experiences<br>- By maintaining this cache, the system reduces latency and improves responsiveness in optimization-related operations.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/optimization_guide_hint_cache_store/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manages synchronization for the hint cache store within the user data optimization framework, ensuring safe concurrent access during cache updates<br>- Facilitates consistent and reliable cache state management, supporting efficient retrieval and storage of optimization hints across multiple processes<br>- Integral to maintaining data integrity and performance in the overall architecture of the optimization system.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Download Service Submodule -->
					<details>
						<summary><b>Download Service</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Download Service</b></code>
							<!-- EntryDB Submodule -->
							<details>
								<summary><b>EntryDB</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Download Service.EntryDB</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Download Service/EntryDB/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Logs user download activities and system events related to the EntryDB component within the Download Service<br>- It facilitates monitoring, troubleshooting, and auditing of data access and transfer processes, ensuring operational transparency and aiding in maintaining system integrity across the user data management architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Download Service/EntryDB/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Manages access control and synchronization for user data within the Download Service, ensuring consistent and secure interactions with the EntryDB<br>- Facilitates coordinated access to the database, preventing conflicts and maintaining data integrity across concurrent operations in the user data management workflow.</td>
										</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- Extension State Submodule -->
					<details>
						<summary><b>Extension State</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Extension State</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension State/MANIFEST-000001'>MANIFEST-000001</a></b></td>
									<td style='padding: 8px;'>- Defines the extension state metadata within the user data storage, facilitating efficient data comparison and retrieval through a bytewise comparator<br>- Serves as a crucial component for maintaining consistent and optimized data handling in the overall database architecture, ensuring reliable persistence and synchronization of user-specific extension information.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension State/CURRENT'>CURRENT</a></b></td>
									<td style='padding: 8px;'>- Provides a manifest reference for the current extension state, serving as a crucial component in tracking and managing user extension configurations within the broader system architecture<br>- Ensures consistency and integrity of extension data, facilitating seamless synchronization and state restoration across user sessions and updates<br>- Acts as a foundational element supporting reliable extension management in the overall project ecosystem.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension State/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Logs the creation and reuse of the user data database within the extensions persistent storage, ensuring data integrity and continuity<br>- It tracks database initialization events, confirming when the database is generated or when an existing manifest is reused, supporting reliable state management across sessions in the overall extension architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension State/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manages the persistent storage of extension state data, ensuring user preferences and session information are retained across application restarts<br>- Integrates seamlessly within the broader architecture by maintaining consistent state management, facilitating a smooth user experience, and supporting reliable synchronization of extension settings across different environments.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Sync Data Submodule -->
					<details>
						<summary><b>Sync Data</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Sync Data</b></code>
							<!-- LevelDB Submodule -->
							<details>
								<summary><b>LevelDB</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Sync Data.LevelDB</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Sync Data/LevelDB/MANIFEST-000001'>MANIFEST-000001</a></b></td>
											<td style='padding: 8px;'>- Defines the structure and metadata for the LevelDB database, specifically managing the manifest file that tracks the databases state and organization<br>- It ensures proper versioning, data consistency, and efficient access within the overall data storage architecture, facilitating reliable synchronization and retrieval of user data across the system.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Sync Data/LevelDB/CURRENT'>CURRENT</a></b></td>
											<td style='padding: 8px;'>- Manages the synchronization state of user data within the LevelDB storage system, ensuring data consistency and integrity across different sessions<br>- It maintains metadata about database versions and updates, facilitating reliable data retrieval and storage operations in the broader application architecture<br>- This component is essential for coordinating data persistence and recovery processes in the project.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Sync Data/LevelDB/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Logs the initialization process of the LevelDB database within the user data synchronization system, indicating whether the database was created anew or reused<br>- It supports the overall architecture by ensuring reliable data storage and retrieval for user-specific synchronization tasks, facilitating efficient management of user data across the application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Sync Data/LevelDB/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Manages synchronization control for LevelDB operations by preventing concurrent access conflicts<br>- Ensures data integrity during read and write processes within the user data synchronization framework, supporting reliable and consistent data storage<br>- Integral to maintaining stable database interactions in the overall architecture, facilitating seamless data management across user sessions.</td>
										</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- BudgetDatabase Submodule -->
					<details>
						<summary><b>BudgetDatabase</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.BudgetDatabase</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/BudgetDatabase/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Logs budget-related activities and transactions within the default user data database, supporting audit trails and troubleshooting<br>- Facilitates tracking of financial operations, ensuring data integrity and accountability across the overall budgeting system<br>- Enhances transparency and reliability in managing user-specific financial information within the broader application architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/BudgetDatabase/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manage access control and ensure data consistency within the BudgetDatabase by implementing locking mechanisms<br>- The LOCK file coordinates concurrent operations, preventing conflicts and maintaining integrity across user data interactions<br>- It plays a crucial role in safeguarding the stability and reliability of the overall budget management system.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Extension Scripts Submodule -->
					<details>
						<summary><b>Extension Scripts</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Extension Scripts</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension Scripts/MANIFEST-000001'>MANIFEST-000001</a></b></td>
									<td style='padding: 8px;'>- Defines the bytewise comparator used by the LevelDB database within the project, ensuring consistent key ordering and efficient data retrieval<br>- Integral to the databases architecture, it supports optimized storage and access patterns across the applications data layer, contributing to overall system performance and reliability.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension Scripts/CURRENT'>CURRENT</a></b></td>
									<td style='padding: 8px;'>- Defines the primary structure and metadata for the user data extension, ensuring proper integration and recognition within the broader system architecture<br>- Facilitates seamless deployment and management of user-specific configurations by establishing essential references and versioning details, thereby supporting consistent extension handling across the project environment.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension Scripts/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Logs the creation and reuse of the user data database within the extension scripts directory, ensuring persistent storage for user-specific information<br>- Facilitates data management by initializing the database when missing and maintaining consistency through manifest reuse, supporting the overall architectures goal of reliable, organized data handling for the sports betting AI project.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension Scripts/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Facilitates the management and enforcement of user data access restrictions within the application<br>- Integrates with extension scripts to ensure security protocols are consistently applied, supporting the overall architectures goal of safeguarding user information and maintaining controlled interactions across the system.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- parcel_tracking_db Submodule -->
					<details>
						<summary><b>parcel_tracking_db</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.parcel_tracking_db</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/parcel_tracking_db/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Logs parcel tracking activities within the database, capturing operational events and system interactions<br>- It supports monitoring, troubleshooting, and auditing by recording detailed records of parcel status updates and system processes, thereby ensuring data integrity and facilitating efficient management of parcel tracking information within the overall architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/parcel_tracking_db/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Ensures data integrity by managing access to the parcel tracking database during critical operations<br>- It functions as a lock mechanism within the database directory, preventing concurrent modifications that could compromise data consistency<br>- This component is vital for maintaining reliable parcel tracking information within the overall system architecture.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Local Storage Submodule -->
					<details>
						<summary><b>Local Storage</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Local Storage</b></code>
							<!-- leveldb Submodule -->
							<details>
								<summary><b>leveldb</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Local Storage.leveldb</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Local Storage/leveldb/MANIFEST-000001'>MANIFEST-000001</a></b></td>
											<td style='padding: 8px;'>- Provides metadata for the LevelDB database, specifically the manifest file that tracks the structure and state of stored data<br>- It ensures data integrity and consistency by maintaining references to data blocks and their organization within the database<br>- This file is essential for database recovery, version management, and efficient data retrieval within the overall storage architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Local Storage/leveldb/CURRENT'>CURRENT</a></b></td>
											<td style='padding: 8px;'>- Manages the current state and metadata of the LevelDB database within the user data storage system<br>- It ensures proper tracking of database versions and consistency by referencing the manifest file, facilitating reliable data retrieval and updates across the applications architecture<br>- This component is essential for maintaining data integrity and coordinating database operations within the overall project.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Local Storage/leveldb/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Manages persistent local storage for user data within the sports betting AI application by initializing and maintaining a LevelDB database<br>- Ensures efficient data retrieval and storage, supporting seamless user experience and data consistency across sessions<br>- This component is integral to the overall architecture, enabling reliable data management for personalized betting insights and AI-driven features.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Local Storage/leveldb/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Manages synchronization and access control for the LevelDB database within user data storage, ensuring data integrity and consistency during read and write operations<br>- Integral to maintaining reliable local data persistence, it supports the overall architecture by coordinating concurrent database interactions and safeguarding user data in the applications storage layer.</td>
										</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- Session Storage Submodule -->
					<details>
						<summary><b>Session Storage</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Session Storage</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Session Storage/MANIFEST-000001'>MANIFEST-000001</a></b></td>
									<td style='padding: 8px;'>- Provides a manifest for session storage data within the user data directory, facilitating efficient retrieval and management of session information<br>- It integrates with the underlying database structure to ensure data consistency and quick access, supporting the overall architectures goal of maintaining seamless user session continuity across application usage.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Session Storage/CURRENT'>CURRENT</a></b></td>
									<td style='padding: 8px;'>- Stores the current user session state within the session storage manifest, enabling persistent user data management across sessions<br>- It ensures seamless user experience by maintaining session continuity, supporting the overall architectures goal of reliable, stateful interactions within the application<br>- This component plays a crucial role in preserving user context and session integrity throughout the system.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Session Storage/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Tracks session storage activities, including creation and reuse of database files within user data management<br>- Ensures persistent storage of session information, facilitating seamless user experience and data integrity across sessions in the sports betting AI application<br>- Serves as a log for monitoring storage operations, supporting reliable data handling within the overall architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Session Storage/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manages session locking mechanisms to ensure data integrity and prevent concurrent access conflicts within user data storage<br>- Facilitates safe session handling by controlling access to user-specific session data, thereby maintaining consistency and security across user interactions in the overall system architecture.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Extension Rules Submodule -->
					<details>
						<summary><b>Extension Rules</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Extension Rules</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension Rules/MANIFEST-000001'>MANIFEST-000001</a></b></td>
									<td style='padding: 8px;'>- Defines the extension rules for user data management within the project, facilitating consistent data comparison and ordering through a bytewise comparator<br>- Integral to the overall architecture, it ensures reliable storage and retrieval operations by establishing standardized data handling protocols in the underlying database system<br>- This configuration supports efficient data processing and integrity across the applications components.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension Rules/CURRENT'>CURRENT</a></b></td>
									<td style='padding: 8px;'>- Defines the core extension rules for user data management within the current configuration, ensuring consistent application of policies across user profiles<br>- Facilitates the integration and enforcement of specific behaviors or restrictions, contributing to the overall architecture by maintaining standardized extension behaviors and supporting seamless user data handling.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension Rules/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Logs the creation and management of the user-specific extension rules database, ensuring proper initialization and reuse of existing data structures<br>- Facilitates persistent storage for user-defined rules, supporting the overall architectures goal of personalized and adaptable betting strategies within the sports betting AI system.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Extension Rules/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Defines and enforces specific extension rules for user data management within the default profile, ensuring consistent application behavior and security standards across the system<br>- Integrates with the broader architecture to maintain standardized extension handling, contributing to reliable user data processing and streamlined configuration management across the project.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Feature Engagement Tracker Submodule -->
					<details>
						<summary><b>Feature Engagement Tracker</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Feature Engagement Tracker</b></code>
							<!-- AvailabilityDB Submodule -->
							<details>
								<summary><b>AvailabilityDB</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Feature Engagement Tracker.AvailabilityDB</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Feature Engagement Tracker/AvailabilityDB/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Logs user engagement activity related to feature availability, supporting monitoring and analysis of feature usage patterns within the system<br>- Facilitates tracking of user interactions over time, enabling data-driven decisions to optimize feature deployment and improve overall user experience across the platform<br>- Integral to maintaining system reliability and understanding engagement trends in the broader architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Feature Engagement Tracker/AvailabilityDB/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Manages synchronization and access control for the feature engagement tracking database, ensuring data integrity during concurrent operations<br>- Integral to maintaining consistent availability states within the feature engagement system, it supports reliable tracking and analysis of user interactions across the platform<br>- This lock mechanism is essential for preserving data accuracy in the overall architecture of the feature engagement infrastructure.</td>
										</tr>
									</table>
								</blockquote>
							</details>
							<!-- EventDB Submodule -->
							<details>
								<summary><b>EventDB</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Feature Engagement Tracker.EventDB</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Feature Engagement Tracker/EventDB/LOG'>LOG</a></b></td>
											<td style='padding: 8px;'>- Logs user engagement events related to feature interactions, supporting the tracking and analysis of user behavior within the feature engagement system<br>- It ensures accurate recording of event data, facilitating insights into feature usage patterns and enabling data-driven decisions to enhance user experience across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Feature Engagement Tracker/EventDB/LOCK'>LOCK</a></b></td>
											<td style='padding: 8px;'>- Ensures exclusive access to the event database by managing lock states, preventing concurrent modifications that could compromise data integrity<br>- Integral to maintaining consistent event tracking within the feature engagement system, it supports reliable data operations across the broader architecture, safeguarding the accuracy and stability of user engagement analytics.</td>
										</tr>
									</table>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- WebStorage Submodule -->
					<details>
						<summary><b>WebStorage</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.WebStorage</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/WebStorage/QuotaManager-journal'>QuotaManager-journal</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure if necessary.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/WebStorage/QuotaManager'>QuotaManager</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- discounts_db Submodule -->
					<details>
						<summary><b>discounts_db</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.discounts_db</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/discounts_db/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Logs user discount transactions and updates within the discounts database, supporting accurate tracking and auditing of discount activities<br>- Ensures data integrity and facilitates troubleshooting by recording detailed event histories related to user discounts, thereby maintaining reliable discount management within the overall system architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/discounts_db/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manages synchronization and access control for the discounts database, ensuring data integrity during concurrent operations<br>- Integral to maintaining consistent discount information within the user data system, it supports reliable transaction handling and prevents conflicts, thereby safeguarding the accuracy and stability of discount-related data across the entire application architecture.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- commerce_subscription_db Submodule -->
					<details>
						<summary><b>commerce_subscription_db</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.commerce_subscription_db</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/commerce_subscription_db/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Logs subscription-related activities and system events within the commerce subscription database, facilitating monitoring, troubleshooting, and auditing of user subscription data<br>- Serves as a vital component for maintaining data integrity and operational transparency across the broader e-commerce platform architecture.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/commerce_subscription_db/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manage concurrency control for the commerce subscription database by implementing locking mechanisms to ensure data integrity during simultaneous access<br>- This file plays a critical role in maintaining consistent subscription data states within the overall system architecture, preventing conflicts and ensuring reliable transaction processing across the user data management layer.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Sessions Submodule -->
					<details>
						<summary><b>Sessions</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Sessions</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Sessions/Session_13383012923468750'>Session_13383012923468750</a></b></td>
									<td style='padding: 8px;'>- Session Management ModuleThis code file is responsible for handling user session data within the application<br>- It manages the lifecycle and state of user sessions, ensuring secure and efficient tracking of user interactions<br>- As a core component of the user data architecture, it facilitates seamless user experiences by maintaining session continuity and supporting session-related operations across the system.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Site Characteristics Database Submodule -->
					<details>
						<summary><b>Site Characteristics Database</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Site Characteristics Database</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Site Characteristics Database/MANIFEST-000001'>MANIFEST-000001</a></b></td>
									<td style='padding: 8px;'>- Defines the structure and metadata for the Site Characteristics Database within the project, facilitating efficient data organization and retrieval<br>- Serves as a manifest that guides the databases integration into the overall architecture, ensuring consistent access to site-specific information essential for application functionality and data management.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Site Characteristics Database/CURRENT'>CURRENT</a></b></td>
									<td style='padding: 8px;'>- Provides a comprehensive overview of site characteristics data stored within the database, facilitating efficient access and management of key site attributes<br>- Supports the broader data architecture by ensuring consistent, organized, and up-to-date information critical for analysis, reporting, and decision-making processes across the project<br>- Enhances data integrity and retrieval efficiency within the overall system.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Site Characteristics Database/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Tracks and logs the creation and reuse of the Site Characteristics Database, ensuring proper initialization within the project’s data management system<br>- It maintains records of database setup events, facilitating reliable data storage and retrieval for site-specific analytics, which supports the overall architecture of managing and analyzing sports betting site data efficiently.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Site Characteristics Database/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Provides a locking mechanism to ensure data integrity and synchronized access within the Site Characteristics Database<br>- It manages concurrent modifications, preventing conflicts and maintaining consistency across user data interactions<br>- Integral to the databases stability, it supports reliable data operations and preserves the integrity of site characteristic records in the overall architecture.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Code Cache Submodule -->
					<details>
						<summary><b>Code Cache</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Code Cache</b></code>
							<!-- js Submodule -->
							<details>
								<summary><b>js</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Code Cache.js</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/14606eb139d4551e_0'>14606eb139d4551e_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates user engagement through a subscription widget integrated into the web interface<br>- Manages form submissions, validates email addresses, and handles successful signups to enhance user acquisition<br>- Supports seamless interaction with the external sg-widget-v2.js script, contributing to the overall architecture by enabling dynamic, responsive user subscription experiences.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/49cafb5576b7ef16_0'>49cafb5576b7ef16_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/d5a92eda3616d58d_0'>d5a92eda3616d58d_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates dynamic user data management and tracking within the broader application architecture by loading external scripts and resources<br>- Supports seamless integration of third-party analytics and content delivery services, ensuring efficient data collection and user interaction monitoring across the platform<br>- Enhances overall system responsiveness and data accuracy for improved user experience insights.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/ffb82a3d6d23a1db_0'>ffb82a3d6d23a1db_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient management and retrieval of user data within the applications caching system, supporting seamless integration with ad services and analytics platforms<br>- Ensures quick access to user-specific information, enabling personalized experiences and optimized ad delivery across the platforms architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/45d0181a693f62c7_0'>45d0181a693f62c7_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates dynamic ad content loading and tracking within the broader web platform architecture<br>- Integrates third-party ad scripts to enable targeted advertising and analytics, supporting revenue generation and user engagement strategies across the site<br>- Ensures seamless ad delivery by managing script references and data collection points aligned with the overall content delivery framework.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/8a4c09c86c852fe0_0'>8a4c09c86c852fe0_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/e620ec29a6bebeda_0'>e620ec29a6bebeda_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, or specify its content, so I can generate an accurate and succinct description based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/abe8945022aba13c_0'>abe8945022aba13c_0</a></b></td>
											<td style='padding: 8px;'>- Provides a cached JavaScript resource linked to the statmuse.com platform, likely serving as a core component for dynamic content rendering or data visualization<br>- Facilitates efficient loading and execution of client-side scripts essential for user interactions and data presentation within the broader architecture<br>- Ensures seamless integration of external assets to support the applications interactive features.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/bfe356c93d9b5af8_0'>bfe356c93d9b5af8_0</a></b></td>
											<td style='padding: 8px;'>- Implements client-side typeahead search functionality, enabling real-time suggestions based on user input<br>- Integrates with the broader search architecture to enhance user experience by providing quick, relevant results, and manages interactions such as resetting suggestions and handling user selections within the applications search interface.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/899448f0c3245c07_0'>899448f0c3245c07_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates user authentication and session management within the application by integrating with external services<br>- Supports secure access control, enabling seamless login experiences and maintaining user state across the platform<br>- Contributes to the overall architecture by ensuring reliable and consistent user identity handling, which is essential for personalized features and protected data access.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/6b0e5688e954fb03_0'>6b0e5688e954fb03_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure or any additional context if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/0b2e860ce1a2f105_0'>0b2e860ce1a2f105_0</a></b></td>
											<td style='padding: 8px;'>- Provides a cached JavaScript resource related to error tracking and analytics, integrating external services such as Raven.js for error monitoring and StatMuse for analytics<br>- It supports the overall architecture by enabling client-side error reporting and user activity tracking, contributing to system stability, performance insights, and user behavior analysis within the broader application ecosystem.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/7c80bd5e0624c238_0'>7c80bd5e0624c238_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure that youd like me to incorporate.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/48d045b8da088d2e_0'>48d045b8da088d2e_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates real-time data retrieval and dynamic content updates by managing cached JavaScript resources<br>- Supports seamless user interactions with live statistics and visualizations on the platform, ensuring efficient loading and execution of essential scripts<br>- Integrates with external data sources to deliver up-to-date information, enhancing the overall responsiveness and interactivity of the web application.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/29ec735fdcdca62b_0'>29ec735fdcdca62b_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file or its content, as well as the project structure details, so I can craft an accurate and succinct summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/0fa78bcce7742a68_0'>0fa78bcce7742a68_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the project structure details, so I can craft an accurate and succinct summary that highlights its purpose within the overall architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/2ba973ceb6f99075_0'>2ba973ceb6f99075_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure details if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/6ac6944aeeb166bd_0'>6ac6944aeeb166bd_0</a></b></td>
											<td style='padding: 8px;'>- SummaryThis code file appears to serve as a cached or intermediary component within the user data directory, likely related to JavaScript execution or data handling<br>- Its primary purpose is to facilitate efficient access or processing of user-specific data, supporting the overall architecture by enabling quick retrieval or execution of scripts<br>- This contributes to the applications performance and responsiveness, particularly in managing user sessions or dynamic content.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/b145e51e598626b5_0'>b145e51e598626b5_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to analyze, or specify its contents, so I can generate the appropriate summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/d7309fcfb620265a_0'>d7309fcfb620265a_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to analyze, and Ill generate a succinct summary based on the context and project structure you've shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/09f1d20dda1485d3_0'>09f1d20dda1485d3_0</a></b></td>
											<td style='padding: 8px;'>- Summary of <code>user_data/Default/Code Cache/js/09f1d20dda1485d3_0</code>This file serves as a cached JavaScript resource within the applications code cache, primarily facilitating faster load times and improved runtime performance<br>- It plays a crucial role in the overall architecture by storing pre-compiled or pre-processed code snippets that are dynamically executed during user interactions<br>- This caching mechanism helps optimize the application's responsiveness and efficiency, ensuring a smoother user experience across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/a5601506e3b05868_0'>a5601506e3b05868_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional project context details, so I can craft an accurate and succinct summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/5d68152db6284fa8_0'>5d68152db6284fa8_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/72c9ff799db774b3_0'>72c9ff799db774b3_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure details if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/bdb1d163330a7336_0'>bdb1d163330a7336_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient retrieval and management of user-specific data within the applications caching layer, supporting seamless access to personalized content<br>- Integrates with external resources to enhance user experience and optimize performance across the platform<br>- Serves as a critical component in maintaining quick data access, ensuring smooth operation of user interactions and content delivery.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/4a25c08a7e898b03_0'>4a25c08a7e898b03_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient retrieval and management of user-specific data within the applications caching system<br>- Integrates timestamp validation to ensure data freshness and consistency, supporting seamless user experience<br>- Serves as a crucial component in maintaining optimal performance and data integrity across the overall architecture by handling cached JavaScript resources dynamically.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/43b5ee8c0f5287f9_0'>43b5ee8c0f5287f9_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates the loading and execution of third-party advertisements and tracking scripts within the web application<br>- Integrates external ad services to support monetization and user engagement analytics, contributing to the overall architecture by enabling seamless ad delivery and data collection without disrupting core functionality.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/2088ff5d8a2f18ac_0'>2088ff5d8a2f18ac_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file or its content, as well as the project structure details, so I can generate an accurate and succinct summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/0c33901efd64d971_0'>0c33901efd64d971_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure or additional context if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/84c572e933885b2e_0'>84c572e933885b2e_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient retrieval and management of user-specific data within the applications caching system<br>- Supports seamless access to personalized information, enhancing user experience and performance by reducing load times and server requests<br>- Integrates into the broader architecture to ensure quick, reliable data access tailored to individual user sessions.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/d3f4e14d1800908d_0'>d3f4e14d1800908d_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/2e613ca1ee8c215a_0'>2e613ca1ee8c215a_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the project structure details, so I can craft an accurate and succinct summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/def1787b77acfd3d_0'>def1787b77acfd3d_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or specify its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/e6aff5b86eabb879_0'>e6aff5b86eabb879_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient retrieval and processing of user-specific data within the applications caching system, supporting seamless data access and performance optimization<br>- Integrates with core modules to enable quick lookups and data iteration, ensuring smooth user interactions and maintaining overall system responsiveness in the broader architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/7efe38685a2821d1_0'>7efe38685a2821d1_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or specify its filename within the <code>user_data/</code> directory so I can generate an accurate and succinct summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/7b0883dc8174f848_0'>7b0883dc8174f848_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its relevant snippets so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/60ba16b3897980df_0'>60ba16b3897980df_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file <code>user_d</code> or its relevant snippets so I can generate an accurate and succinct summary based on its purpose within the overall project architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/d8b268117f335248_0'>d8b268117f335248_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates the integration of third-party advertising and analytics modules within the broader web application architecture<br>- It manages dynamic script loading and configuration, enabling seamless extension of functionalities such as user tracking, ad delivery, and data collection<br>- This component ensures modularity and flexibility in incorporating external services into the platform’s ecosystem.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/032f6fcade4c6c80_0'>032f6fcade4c6c80_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient management and retrieval of user-specific data within the applications caching system, supporting seamless user experience and performance optimization<br>- Integrates external ad services and tracking scripts to enable targeted advertising and analytics, contributing to monetization strategies<br>- Overall, it plays a crucial role in maintaining data integrity and enhancing the applications responsiveness across the codebase architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/53e3d3b406efafec_0'>53e3d3b406efafec_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure or additional context if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/01d58cc9c37bf3b4_0'>01d58cc9c37bf3b4_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates client-side caching and retrieval of user-specific data within the web application, enhancing performance and user experience<br>- Integrates seamlessly into the overall architecture by managing temporary data storage, ensuring quick access to user preferences and session information, and supporting efficient data handling across different components of the project.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/552a9b2cadf0abb2_0'>552a9b2cadf0abb2_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the project structure details, so I can craft an accurate and succinct summary for you.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/3591d905fbf25aec_0'>3591d905fbf25aec_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient retrieval and caching of user-specific data within the applications JavaScript environment<br>- Integrates seamlessly into the broader architecture to optimize performance and ensure quick access to user information, supporting dynamic content rendering and personalized experiences across the platform<br>- Enhances overall responsiveness by managing data flow between client-side components and backend services.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/86d7ac905c6ca883_0'>86d7ac905c6ca883_0</a></b></td>
											<td style='padding: 8px;'>- Implements client-side cookie consent management within the project architecture, ensuring user preferences are respected and integrated across the applications components<br>- Facilitates compliance with privacy regulations by tracking and storing user consent status, contributing to a cohesive and user-centric data handling framework.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/1f7d7ccd24630230_0'>1f7d7ccd24630230_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/6688cc37d4b97ce3_0'>6688cc37d4b97ce3_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient caching and retrieval of user-specific data within the applications JavaScript environment<br>- Integrates seamlessly into the broader architecture to optimize performance and user experience by managing temporary data storage, ensuring quick access to frequently used information during user interactions<br>- Supports the overall systems goal of delivering responsive and personalized content.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/c3af00268111cd1c_0'>c3af00268111cd1c_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to consider.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/f2f848229dcf5e7d_0'>f2f848229dcf5e7d_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that youd like me to incorporate.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/90272da7208ee107_0'>90272da7208ee107_0</a></b></td>
											<td style='padding: 8px;'>- Provides client-side caching and data retrieval mechanisms to optimize user data access within the application<br>- Facilitates efficient management of user preferences, selections, and interactions, supporting seamless user experience and reducing server load<br>- Integrates with core application workflows to ensure consistent state management across different user sessions and interface components.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/c33dea8d27047528_0'>c33dea8d27047528_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the content of the code file or its filename so I can generate an accurate and succinct summary based on the context and project structure.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/8a9332cabb9e6dc8_0'>8a9332cabb9e6dc8_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates user data management within the applications architecture by handling cached JavaScript resources related to consent management and tracking<br>- Supports seamless integration of third-party scripts, ensuring compliance and user privacy preferences are maintained across sessions<br>- Enhances overall system efficiency by preloading essential scripts, contributing to a smoother user experience and reliable data collection.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/fefcb33848da5187_0'>fefcb33848da5187_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure details if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/ca1fb78b49d27c13_0'>ca1fb78b49d27c13_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure details if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/1857b7e028270157_0'>1857b7e028270157_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates integration of advertising and analytics scripts within the web application, enabling dynamic ad bidding and tracking<br>- Supports seamless communication with external ad services, ensuring efficient ad delivery and data collection<br>- Contributes to the overall architecture by managing third-party script loading and execution, optimizing monetization and user engagement tracking across the platform.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/67b922a46830982d_0'>67b922a46830982d_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/d5227ea359a157fd_0'>d5227ea359a157fd_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/13f32378be7873f0_0'>13f32378be7873f0_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to analyze, or specify its contents, so I can generate an accurate and succinct summary based on the context and project structure youve shared.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/73f4f890093b4a75_0'>73f4f890093b4a75_0</a></b></td>
											<td style='padding: 8px;'>- Implements user agent detection and filtering mechanisms to identify and manage various client devices and bots accessing the platform<br>- Enhances security and analytics accuracy by recognizing legitimate traffic and blocking unwanted automated agents, thereby supporting the overall architectures goal of maintaining optimal performance, security, and accurate user insights.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/index'>index</a></b></td>
											<td style='padding: 8px;'>- Facilitates the management and caching of user-specific JavaScript data within the applications local storage<br>- It ensures efficient retrieval and storage of user preferences or session information, supporting seamless user experience and performance optimization across the broader codebase architecture.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/fb2afb4a352b39ba_0'>fb2afb4a352b39ba_0</a></b></td>
											<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with the project structure or additional context if available.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/c4792655eea7f194_0'>c4792655eea7f194_0</a></b></td>
											<td style='padding: 8px;'>- Provides a mechanism for managing user data and event tracking within the application, integrating schema filtering, user agent detection, and remote plugin support<br>- Facilitates seamless data collection and processing to enhance user insights, analytics, and feature enablement across the platforms architecture<br>- Ensures consistent data handling aligned with project standards and external integrations.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/2c983f7aa669ac12_0'>2c983f7aa669ac12_0</a></b></td>
											<td style='padding: 8px;'>- Summary of <code>user_data/Default/Code Cache/js/2c983f7aa669ac12_0</code>This code file appears to serve as a cached JavaScript resource within the applications user data directory<br>- Its primary purpose is to facilitate efficient retrieval and execution of dynamic content or scripts related to user choices or preferences, as indicated by the embedded URL referencing a choice management endpoint<br>- Within the broader architecture, this file contributes to the application's ability to personalize user experiences and optimize performance by caching relevant scripts locally, reducing load times and network requests during runtime.</td>
										</tr>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/e1354aaeae4d0624_0'>e1354aaeae4d0624_0</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient retrieval and caching of user-specific data within the applications client-side environment<br>- Supports seamless access to personalized content by managing data storage and retrieval processes, thereby enhancing user experience and performance across the platform<br>- Integrates with the broader architecture to ensure quick, reliable access to user information during interactions.</td>
										</tr>
									</table>
									<!-- index-dir Submodule -->
									<details>
										<summary><b>index-dir</b></summary>
										<blockquote>
											<div class='directory-path' style='padding: 8px 0; color: #666;'>
												<code><b>⦿ user_data.Default.Code Cache.js.index-dir</b></code>
											<table style='width: 100%; border-collapse: collapse;'>
											<thead>
												<tr style='background-color: #f8f9fa;'>
													<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
													<th style='text-align: left; padding: 8px;'>Summary</th>
												</tr>
											</thead>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/js/index-dir/the-real-index'>the-real-index</a></b></td>
													<td style='padding: 8px;'>- Facilitates efficient retrieval and management of user-specific data within the applications caching system<br>- Integrates seamlessly into the overall architecture to optimize data access speed and reduce latency, supporting smooth user interactions and enhancing performance across the platform<br>- Ensures that user data remains readily available, contributing to a responsive and scalable user experience.</td>
												</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<!-- wasm Submodule -->
							<details>
								<summary><b>wasm</b></summary>
								<blockquote>
									<div class='directory-path' style='padding: 8px 0; color: #666;'>
										<code><b>⦿ user_data.Default.Code Cache.wasm</b></code>
									<table style='width: 100%; border-collapse: collapse;'>
									<thead>
										<tr style='background-color: #f8f9fa;'>
											<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
											<th style='text-align: left; padding: 8px;'>Summary</th>
										</tr>
									</thead>
										<tr style='border-bottom: 1px solid #eee;'>
											<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/wasm/index'>index</a></b></td>
											<td style='padding: 8px;'>- Facilitates efficient access and management of WebAssembly modules within the user data cache, enabling seamless integration and execution of WASM components in the broader application architecture<br>- Enhances performance by optimizing module retrieval, supporting dynamic loading, and ensuring smooth interoperability between native code and WebAssembly environments across the system.</td>
										</tr>
									</table>
									<!-- index-dir Submodule -->
									<details>
										<summary><b>index-dir</b></summary>
										<blockquote>
											<div class='directory-path' style='padding: 8px 0; color: #666;'>
												<code><b>⦿ user_data.Default.Code Cache.wasm.index-dir</b></code>
											<table style='width: 100%; border-collapse: collapse;'>
											<thead>
												<tr style='background-color: #f8f9fa;'>
													<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
													<th style='text-align: left; padding: 8px;'>Summary</th>
												</tr>
											</thead>
												<tr style='border-bottom: 1px solid #eee;'>
													<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Code Cache/wasm/index-dir/the-real-index'>the-real-index</a></b></td>
													<td style='padding: 8px;'>- Facilitates efficient retrieval and indexing of user data within the WebAssembly cache, supporting rapid access to stored information<br>- Integrates seamlessly into the broader data management architecture, ensuring quick lookup capabilities and optimized performance for user-specific data operations across the system<br>- Enhances overall responsiveness by maintaining a structured index for user data access.</td>
												</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
						</blockquote>
					</details>
					<!-- DawnGraphiteCache Submodule -->
					<details>
						<summary><b>DawnGraphiteCache</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.DawnGraphiteCache</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnGraphiteCache/data_2'>data_2</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnGraphiteCache/data_0'>data_0</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnGraphiteCache/data_1'>data_1</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with any additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnGraphiteCache/data_3'>data_3</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file or its content so I can generate the appropriate summary based on the context and project structure.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnGraphiteCache/index'>index</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- DawnWebGPUCache Submodule -->
					<details>
						<summary><b>DawnWebGPUCache</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.DawnWebGPUCache</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnWebGPUCache/data_2'>data_2</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to incorporate.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnWebGPUCache/data_0'>data_0</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure if available.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnWebGPUCache/data_1'>data_1</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnWebGPUCache/data_3'>data_3</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure if available.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/DawnWebGPUCache/index'>index</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- ClientCertificates Submodule -->
					<details>
						<summary><b>ClientCertificates</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.ClientCertificates</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/ClientCertificates/LOG'>LOG</a></b></td>
									<td style='padding: 8px;'>- Facilitates the logging and management of client certificate activities within the user data directory, supporting secure client authentication processes<br>- Integrates into the broader architecture by ensuring proper recording of certificate-related events, aiding in troubleshooting, compliance, and security auditing across the system<br>- Enhances overall security posture through systematic tracking of client certificate usage.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/ClientCertificates/LOCK'>LOCK</a></b></td>
									<td style='padding: 8px;'>- Manage client certificate access within the user data directory, ensuring secure handling and storage of authentication credentials<br>- Facilitates streamlined certificate management for client authentication processes, supporting the overall security architecture of the application<br>- Integrates seamlessly into the broader system to maintain trusted connections and safeguard sensitive user data.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- Shared Dictionary Submodule -->
					<details>
						<summary><b>Shared Dictionary</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.Shared Dictionary</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Shared Dictionary/db-journal'>db-journal</a></b></td>
									<td style='padding: 8px;'>- Facilitates reliable data persistence by managing journal entries within the shared dictionary database<br>- Ensures transactional integrity and durability of user data operations, supporting the overall architectures focus on consistent and fault-tolerant data handling across the system<br>- This component is essential for maintaining data consistency during concurrent access and system recoveries.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/Shared Dictionary/db'>db</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional project context details, so I can craft an accurate and succinct summary for you.</td>
								</tr>
							</table>
						</blockquote>
					</details>
					<!-- GPUCache Submodule -->
					<details>
						<summary><b>GPUCache</b></summary>
						<blockquote>
							<div class='directory-path' style='padding: 8px 0; color: #666;'>
								<code><b>⦿ user_data.Default.GPUCache</b></code>
							<table style='width: 100%; border-collapse: collapse;'>
							<thead>
								<tr style='background-color: #f8f9fa;'>
									<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
									<th style='text-align: left; padding: 8px;'>Summary</th>
								</tr>
							</thead>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/GPUCache/data_2'>data_2</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to incorporate.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/GPUCache/data_0'>data_0</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to incorporate.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/GPUCache/data_1'>data_1</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/GPUCache/data_3'>data_3</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
								</tr>
								<tr style='border-bottom: 1px solid #eee;'>
									<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/Default/GPUCache/index'>index</a></b></td>
									<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with any additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
								</tr>
							</table>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<!-- ShaderCache Submodule -->
			<details>
				<summary><b>ShaderCache</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ user_data.ShaderCache</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/ShaderCache/data_2'>data_2</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/ShaderCache/data_0'>data_0</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/ShaderCache/data_1'>data_1</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional project context details, so I can craft an accurate and succinct summary for you.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/ShaderCache/data_3'>data_3</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to incorporate.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/ShaderCache/index'>index</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- GraphiteDawnCache Submodule -->
			<details>
				<summary><b>GraphiteDawnCache</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ user_data.GraphiteDawnCache</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GraphiteDawnCache/data_2'>data_2</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GraphiteDawnCache/data_0'>data_0</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to incorporate.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GraphiteDawnCache/data_1'>data_1</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GraphiteDawnCache/data_3'>data_3</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project structure that youd like me to incorporate.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/GraphiteDawnCache/index'>index</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file or its content, along with the additional context details about the project, so I can craft an accurate and succinct summary for you.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- segmentation_platform Submodule -->
			<details>
				<summary><b>segmentation_platform</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ user_data.segmentation_platform</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/segmentation_platform/ukm_db-journal'>ukm_db-journal</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or project details youd like me to consider.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/user_data/segmentation_platform/ukm_db'>ukm_db</a></b></td>
							<td style='padding: 8px;'>Certainly! Please provide the code file youd like me to summarize, along with any additional context or details about the project that can help tailor the summary effectively.</td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- Proxy_testing Submodule -->
	<details>
		<summary><b>Proxy_testing</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ Proxy_testing</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Proxy_testing/proxy_test.py'>proxy_test.py</a></b></td>
					<td style='padding: 8px;'>- Performs asynchronous validation of a list of proxy servers by testing their connectivity to a designated URL, and identifies those that are functional<br>- Successfully tested proxies are saved for future use, facilitating reliable proxy management within the broader system architecture<br>- This ensures efficient and automated proxy health checks, supporting robust network operations.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Proxy_testing/proxyscrape_premium_http_proxies.txt'>proxyscrape_premium_http_proxies.txt</a></b></td>
					<td style='padding: 8px;'>- The file <code>Proxy_testing/proxyscrape_premium_http_proxies.txt</code> serves as a repository of premium HTTP proxy addresses used within the project<br>- Its primary purpose is to provide a curated list of proxy endpoints that facilitate network requests through different IP addresses, enhancing privacy, testing, or data scraping capabilities<br>- This component integrates into the broader architecture by enabling the system to route traffic via these proxies, supporting functionalities such as proxy validation, load balancing, or anonymized data collection across the codebase.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- MLB_Dashboard Submodule -->
	<details>
		<summary><b>MLB_Dashboard</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ MLB_Dashboard</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Dashboard/utils.py'>utils.py</a></b></td>
					<td style='padding: 8px;'>- Provides utility functions for loading and analyzing MLB prediction data, supporting the overall dashboard architecture<br>- Facilitates retrieval of model tracking and prediction results, and computes key performance metrics, enabling insights into prediction accuracy across models, prop types, and recent outcomes within the MLB analytics ecosystem.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Dashboard/config.py'>config.py</a></b></td>
					<td style='padding: 8px;'>- Defines essential configuration settings for the MLB_Dashboard application, including directory paths for data storage and model tracking, as well as Flask server parameters<br>- Facilitates organized access to project resources and ensures consistent environment setup, supporting smooth integration and deployment within the overall architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Dashboard/app.py'>app.py</a></b></td>
					<td style='padding: 8px;'>- Provides a Flask-based API and web interface for a baseball analytics dashboard, aggregating recent prediction accuracy metrics, historical performance data, and top player prop predictions<br>- Facilitates real-time insights into model performance and prediction quality, supporting data-driven decision-making within the broader MLB analytics architecture.</td>
				</tr>
			</table>
			<!-- templates Submodule -->
			<details>
				<summary><b>templates</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ MLB_Dashboard.templates</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Dashboard/templates/dashboard.html'>dashboard.html</a></b></td>
							<td style='padding: 8px;'>- Provides the user interface for the MLB Model Dashboard, visualizing key performance metrics, historical data, and recent high-confidence predictions<br>- Facilitates real-time monitoring and comparison of multiple models accuracy, agreement, and prop type performance, enabling users to assess model effectiveness and prediction reliability within the overall architecture.</td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- app Submodule -->
	<details>
		<summary><b>app</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ app</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/app/models.py'>models.py</a></b></td>
					<td style='padding: 8px;'>- Defines the user data model within the applications architecture, enabling user account management and authentication<br>- Facilitates secure storage of user credentials and supports password verification, forming a core component for user-related functionalities and access control across the system.</td>
				</tr>
			</table>
			<!-- routes Submodule -->
			<details>
				<summary><b>routes</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ app.routes</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/app/routes/routes.py'>routes.py</a></b></td>
							<td style='padding: 8px;'>- Defines the main web routes for the application, serving static pages and providing an API endpoint to retrieve NBA player props data<br>- Integrates data from CSV files, enriches it with player IDs and headshot URLs, and supplies dynamic content for frontend components, supporting the overall architecture of a sports analytics platform.</td>
						</tr>
					</table>
				</blockquote>
			</details>
			<!-- templates Submodule -->
			<details>
				<summary><b>templates</b></summary>
				<blockquote>
					<div class='directory-path' style='padding: 8px 0; color: #666;'>
						<code><b>⦿ app.templates</b></code>
					<table style='width: 100%; border-collapse: collapse;'>
					<thead>
						<tr style='background-color: #f8f9fa;'>
							<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
							<th style='text-align: left; padding: 8px;'>Summary</th>
						</tr>
					</thead>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/app/templates/features.html'>features.html</a></b></td>
							<td style='padding: 8px;'>- Defines the webpage layout for the Features section of PropPilot AI, showcasing key functionalities such as Prop Picks, Data Display, and Line Tracking<br>- It guides users through the platforms capabilities, emphasizing real-time insights and AI-driven recommendations to enhance prop betting strategies, ultimately encouraging engagement and onboarding.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/app/templates/home.html'>home.html</a></b></td>
							<td style='padding: 8px;'>- Provides the landing page interface for PropPilot AI, showcasing its core value propositions through engaging visuals, animated text, and interactive elements<br>- It introduces users to the platforms AI-driven insights, data transparency, and real-time line tracking, guiding visitors to learn more about the service, explore features, and subscribe to the affordable Pro plan, thereby supporting user engagement and conversion.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/app/templates/whyus.html'>whyus.html</a></b></td>
							<td style='padding: 8px;'>- Provides the webpage layout for the Why PropPilot AI section, showcasing the platform's value proposition, operational methodology, and benefits<br>- It effectively communicates PropPilot AI’s data-driven approach to sports betting predictions, emphasizing transparency, accuracy, and real-time insights, while encouraging user engagement through a call-to-action<br>- This page plays a key role in marketing and user onboarding within the overall site architecture.</td>
						</tr>
						<tr style='border-bottom: 1px solid #eee;'>
							<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/app/templates/base.html'>base.html</a></b></td>
							<td style='padding: 8px;'>- Defines the foundational HTML template for PropPilot AI, establishing a consistent layout and styling across the web application<br>- It incorporates navigation, footer, and responsive design elements, serving as the backbone for rendering dynamic content and ensuring a cohesive user interface within the overall project architecture.</td>
						</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
	<!-- MLB_Data_Extraction Submodule -->
	<details>
		<summary><b>MLB_Data_Extraction</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ MLB_Data_Extraction</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_pitchers_stats.py'>mlb_pitchers_stats.py</a></b></td>
					<td style='padding: 8px;'>- Fetches and processes MLB pitcher season-to-date statistics from StatMuse, filtering out inactive players<br>- Integrates data from an input CSV, scrapes individual player stats asynchronously, and outputs a cleaned, consolidated CSV with key pitching metrics<br>- Supports comprehensive analysis of pitcher performance trends across the season within the broader data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_rhp_avg.py'>mlb_rhp_avg.py</a></b></td>
					<td style='padding: 8px;'>- Fetches season-specific against-right-handed-pitcher stats for non-pitcher MLB players listed in mlb_prizepicks.csv, extracting key performance metrics such as G, AB, H, HR, RBI, PA, AVG, OBP, SLG, and OPS<br>- Outputs the compiled data into mlb_vs_rhp_avg.csv, supporting analysis of player performance against right-handed pitchers within the broader data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_rhp_last15.py'>mlb_rhp_last15.py</a></b></td>
					<td style='padding: 8px;'>- Fetches recent performance metrics for non-pitcher players from StatMuse, focusing on last 15 games against right-handed pitchers<br>- Processes player data from CSV, scrapes relevant stats, and outputs a summarized dataset<br>- Facilitates analysis of hitter performance trends, supporting strategic decision-making within the broader MLB data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_hitter_pitcher_hotzones.py'>mlb_hitter_pitcher_hotzones.py</a></b></td>
					<td style='padding: 8px;'>- Generates detailed hot-zone profiles for MLB hitters and pitchers by aggregating swing and pitch data from BaseballSavant for the 2025 season<br>- Facilitates strategic analysis of player tendencies and tendencies, supporting advanced scouting, player evaluation, and matchup planning within the broader data architecture<br>- Outputs are stored as CSV files for integration with other analytical components.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_rhp_last5.py'>mlb_rhp_last5.py</a></b></td>
					<td style='padding: 8px;'>- Fetches recent performance metrics for non-pitcher players from StatMuse, focusing on last five games against right-handed pitchers<br>- Processes player data from CSV, scrapes relevant stats, and outputs a summarized dataset with key batting metrics<br>- Integrates seamlessly into the broader MLB data pipeline to enhance player performance analysis and betting insights.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_lhp_last5.py'>mlb_lhp_last5.py</a></b></td>
					<td style='padding: 8px;'>- Fetches recent performance metrics against left-handed pitchers for non-pitcher players listed in mlb_prizepicks.csv<br>- Extracts key batting statistics from StatMuse for the last five games, then compiles and saves the data into mlb_vs_lhp_last5.csv<br>- Facilitates targeted player analysis by providing recent matchup insights within the broader MLB data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_pitcher_advanced_stats.py'>mlb_pitcher_advanced_stats.py</a></b></td>
					<td style='padding: 8px;'>- Fetches and processes advanced MLB pitching statistics from FanGraphs for players listed in PrizePicks, focusing on the 2025 MLB season<br>- Integrates player identifiers, filters relevant data, and outputs a consolidated CSV with key pitching metrics to support player analysis and betting insights within the broader data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/hitter_stats_merge.py'>hitter_stats_merge.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates and cleans comprehensive MLB hitter data from multiple sources, integrating player stats, matchup details, weather, park factors, and advanced metrics into a unified dataset<br>- Facilitates in-depth analysis of hitter performance, contextualized by opposing pitchers, environmental conditions, and ballpark influences, supporting data-driven insights for player evaluation and strategic decision-making within the broader baseball analytics architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_prizepicks.py'>mlb_prizepicks.py</a></b></td>
					<td style='padding: 8px;'>- Fetches live MLB prop lines from PrizePicks and exports them to a CSV file for analysis or betting insights<br>- Integrates player and game metadata, filters for current-day, relevant props, and handles special cases like Shohei Ohtanis dual roles<br>- Supports real-time data updates within the broader data pipeline for MLB sports analytics.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/pitcher_stats_merge.py'>pitcher_stats_merge.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates and cleans comprehensive MLB pitcher data from multiple sources into a unified dataset for analysis or modeling<br>- It merges player stats, advanced metrics, pitch usage, hot zones, and recent performance trends, ensuring consistent naming conventions<br>- The resulting master dataset supports in-depth pitcher performance evaluation, predictive modeling, and strategic insights within the broader baseball analytics architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_lhp_last15.py'>mlb_lhp_last15.py</a></b></td>
					<td style='padding: 8px;'>- Fetches recent performance metrics for non-pitcher MLB players from StatMuse, focusing on last 15 games against left-handed pitchers<br>- Processes player data from a CSV, scrapes relevant stats, and outputs a summarized dataset<br>- Facilitates advanced analysis of player performance trends, supporting strategic decision-making within the broader baseball data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_statcast_stats.py'>mlb_statcast_stats.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates and processes MLB player Statcast data from FanGraphs, focusing on 2025 season metrics relevant to betting and analysis<br>- It filters players based on existing CSV data, fetches detailed stats, and compiles key performance indicators such as exit velocity, barrel rate, and expected batting averages into a streamlined CSV output for further use in predictive modeling or scouting.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/prepare_mlb_predictions.py'>prepare_mlb_predictions.py</a></b></td>
					<td style='padding: 8px;'>- The <code>prepare_mlb_predictions.py</code> script serves as a foundational component within the overall MLB data pipeline, focusing on aggregating and preparing diverse datasets essential for accurate baseball game predictions<br>- It consolidates player statistics, weather conditions, and park factors into a structured format, ensuring that downstream modeling processes have access to clean, organized, and comprehensive data<br>- By orchestrating data collection and preprocessing, this module underpins the predictive analytics framework, enabling more informed and reliable MLB game outcome forecasts.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/MLB_Main.py'>MLB_Main.py</a></b></td>
					<td style='padding: 8px;'>- Orchestrates the sequential execution of various data extraction and processing scripts within the MLB data pipeline, ensuring proper order and handling dependencies<br>- Facilitates automated running of individual scripts, manages error logging, and provides a comprehensive overview of execution success, thereby streamlining the overall data collection and transformation process for MLB analytics.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_lhp_last10.py'>mlb_lhp_last10.py</a></b></td>
					<td style='padding: 8px;'>- Fetches recent performance metrics for non-pitcher players from MLB data, focusing on their last 10 games against left-handed pitchers<br>- Processes player data from a CSV, scrapes relevant statistics from StatMuse, and outputs a summarized CSV with key performance indicators, supporting advanced analysis and betting insights within the broader MLB data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_daily_lineups.py'>mlb_daily_lineups.py</a></b></td>
					<td style='padding: 8px;'>- Provides daily MLB starting lineups by scraping MLB.com, extracting player details, positions, and handedness<br>- Generates a structured CSV file for integration into broader data workflows, supporting analysis of team compositions and player matchups<br>- Facilitates real-time updates of lineup data to enhance predictive models and strategic decision-making within the overall architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_rhp_last10.py'>mlb_rhp_last10.py</a></b></td>
					<td style='padding: 8px;'>- Fetches recent performance metrics for non-pitcher players from StatMuse, focusing on last 10 games against right-handed pitchers<br>- Processes player data from CSV, scrapes relevant stats, and outputs a summarized dataset for analysis or modeling within the MLB data architecture<br>- Facilitates targeted player performance insights to support sports analytics and betting strategies.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_hitter_advanced_stats.py'>mlb_hitter_advanced_stats.py</a></b></td>
					<td style='padding: 8px;'>- Extracts advanced MLB hitting statistics against left-and right-handed pitchers by scraping FanGraphs data for specified players<br>- Facilitates analysis of player performance splits, generating separate CSV files for each handedness, which support deeper insights into hitter tendencies and matchup-specific strengths within the broader data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_pitcher_pitch_usage.py'>mlb_pitcher_pitch_usage.py</a></b></td>
					<td style='padding: 8px;'>- Extracts and compiles pitcher pitch usage data from MLB Savant profiles by scraping web pages, matching players via CSV mappings, and aggregating the information into a structured CSV report<br>- This process supports analysis of pitcher tendencies and pitch distribution, integrating data sources to enhance understanding of player profiles within the broader baseball analytics architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_pitcher_last15_last30.py'>mlb_pitcher_last15_last30.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates pitcher performance metrics over the last 15 and 30 days using Statcast data, focusing on key pitching and batted-ball statistics<br>- Outputs CSV files with summarized, rounded metrics for each pitcher listed in the PrizePicks export, facilitating data-driven insights for player analysis and betting strategies within the broader MLB data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_utils.py'>mlb_utils.py</a></b></td>
					<td style='padding: 8px;'>- Provides utility functions for data extraction, normalization, and analysis within the MLB data pipeline<br>- Facilitates web scraping with proxy rotation, parses game schedules and weather forecasts, normalizes player names, and extracts pitching zone statistics<br>- Supports robust data collection and preprocessing essential for comprehensive baseball analytics and insights across the project architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_hitter_vs_pitches.py'>mlb_hitter_vs_pitches.py</a></b></td>
					<td style='padding: 8px;'>- Extracts and analyzes MLB hitter performance against various pitch types using Baseball Savant data<br>- It cross-references a list of players from PrizePicks, retrieves pitch arsenal statistics, and generates a comprehensive CSV report detailing each hitter’s performance metrics such as run value, wOBA, expected wOBA, and hard-hit percentage<br>- This facilitates targeted insights into hitter-pitch interactions within the broader data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_stadium_weather.py'>mlb_stadium_weather.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates and analyzes weather forecast data for MLB home games, focusing on stadium-specific wind conditions and their potential impact on gameplay<br>- Integrates schedule, stadium orientation, and team data to produce a comprehensive weather summary, aiding strategic insights for players and fans<br>- Outputs a CSV report with weather details and wind effects at game time.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/temp.py'>temp.py</a></b></td>
					<td style='padding: 8px;'>- Generates comprehensive training datasets for MLB hitters and pitchers by integrating master records with box score results<br>- Ensures data completeness and consistency, preparing structured CSV files for model development or analysis<br>- Facilitates seamless data merging and validation, supporting the broader architecture of predictive modeling and performance analysis within the MLB data pipeline.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/mlb_lhp_avg.py'>mlb_lhp_avg.py</a></b></td>
					<td style='padding: 8px;'>- Fetches and processes season-specific vs-LHP batting statistics for non-pitcher players listed in mlb_prizepicks.csv<br>- Extracted metrics include G, AB, H, HR, RBI, PA, AVG, OBP, SLG, and OPS, and outputs the summarized data into mlb_vs_lhp_avg.csv<br>- Facilitates targeted player performance analysis against left-handed pitchers within the broader MLB data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/MLB_Data_Extraction/create_training_data.py'>create_training_data.py</a></b></td>
					<td style='padding: 8px;'>- Generates comprehensive training datasets for MLB hitters and pitchers by merging master player data with box score results, ensuring all necessary features are included<br>- Facilitates model training for player performance prediction by preparing structured, enriched datasets tailored for machine learning applications within the broader data pipeline.</td>
				</tr>
			</table>
		</blockquote>
	</details>
	<!-- Data_Extraction Submodule -->
	<details>
		<summary><b>Data_Extraction</b></summary>
		<blockquote>
			<div class='directory-path' style='padding: 8px 0; color: #666;'>
				<code><b>⦿ Data_Extraction</b></code>
			<table style='width: 100%; border-collapse: collapse;'>
			<thead>
				<tr style='background-color: #f8f9fa;'>
					<th style='width: 30%; text-align: left; padding: 8px;'>File Name</th>
					<th style='text-align: left; padding: 8px;'>Summary</th>
				</tr>
			</thead>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Season_Stats.py'>Season_Stats.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates NBA player season statistics by scraping data from StatMuse based on input CSV, then processes and saves the compiled data into a structured CSV file<br>- Facilitates seamless integration of up-to-date player performance metrics into the broader data pipeline, supporting analysis, modeling, or visualization within the overall project architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/utils.py'>utils.py</a></b></td>
					<td style='padding: 8px;'>- Facilitates robust web data extraction by asynchronously fetching and parsing HTML content using rotating proxies, while managing rate limits and detecting no-result scenarios<br>- Provides utility functions for proxy management and sanitizing player names, supporting scalable, resilient scraping workflows within the broader data collection architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Stats_Without_Injured_Starter.py'>Stats_Without_Injured_Starter.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates and analyzes NBA player performance data excluding injured starters, focusing on healthy players stats in games without injured teammates<br>- Facilitates insights into player contributions under specific team conditions by fetching injury reports, matching players, and retrieving season statistics, ultimately generating a comprehensive CSV report for strategic analysis within the broader data architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Merge_Data.py'>Merge_Data.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates and cleans diverse sports data sources to produce a comprehensive, unified dataset for player performance analysis<br>- Merges various CSV files related to player stats, opponent ratings, game context, and historical matchups, ensuring data consistency and accuracy<br>- Facilitates advanced analytics and decision-making by providing a structured, enriched dataset for modeling or reporting within the broader project architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Did_Prop_Hit.py'>Did_Prop_Hit.py</a></b></td>
					<td style='padding: 8px;'>- Fetches and parses NBA player box scores from Statmuse to update local CSV datasets, enabling validation of betting props against actual game performance<br>- Automates data retrieval, extraction, and comparison processes, supporting accurate tracking of prop outcomes and enhancing the overall data integrity within the sports analytics architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Last_10_Season.py'>Last_10_Season.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates last 10-game average player statistics from external sources and updates the dataset accordingly<br>- Facilitates data enrichment by fetching, parsing, and consolidating recent performance metrics, enabling more accurate analysis and modeling within the broader sports analytics architecture<br>- Ensures data consistency and readiness for downstream insights or predictive tasks.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Last_10_Hit_Percentage.py'>Last_10_Hit_Percentage.py</a></b></td>
					<td style='padding: 8px;'>- Calculates and exports the last 10 game matchup hit percentage for NBA players props by scraping data from StatMuse<br>- Integrates seamlessly into the data pipeline, enriching player performance insights and prop analysis within the broader sports analytics architecture<br>- Facilitates data-driven decision-making by providing recent performance trends for betting or fantasy sports applications.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/get_current_player_ids.py'>get_current_player_ids.py</a></b></td>
					<td style='padding: 8px;'>- Generates a comprehensive CSV catalog of current NBA players with normalized names and unique identifiers, facilitating reliable player data referencing across the project<br>- This script supports data consistency and integration within the broader architecture, enabling accurate player identification for analytics, modeling, or further data processing tasks.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Season_Hit_Percentage.py'>Season_Hit_Percentage.py</a></b></td>
					<td style='padding: 8px;'>- Calculates and compiles season-long hit percentage metrics for NBA players based on prop data<br>- It integrates web scraping of StatMuse to determine the number of games a player hits specific props, correlates this with season game data, and outputs a comprehensive CSV report<br>- This functionality supports performance analysis and data-driven decision-making within the broader sports analytics architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Last_5_Season.py'>Last_5_Season.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates last five games player statistics from StatMuse, focusing on key performance metrics<br>- Facilitates data extraction, cleaning, and storage into CSV format for further analysis or modeling<br>- Supports project architecture by providing up-to-date, summarized player performance data essential for sports analytics, betting insights, or fantasy sports decision-making.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Opponent_Defensive_Rating.py'>Opponent_Defensive_Rating.py</a></b></td>
					<td style='padding: 8px;'>- Fetches and compiles opponent team defensive ratings from StatMuse, integrating data from PrizePicks to enrich player performance analysis<br>- It automates web scraping, processes team data, and outputs a CSV with defensive metrics, supporting strategic insights within the broader sports analytics architecture.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Main.py'>Main.py</a></b></td>
					<td style='padding: 8px;'>- Orchestrates the sequential execution of data extraction and processing scripts within the project, ensuring comprehensive collection and merging of sports-related data<br>- Facilitates automated data pipeline flow, starting with scraping, followed by targeted data retrieval, and culminating in data consolidation, supporting the overall architecture of data-driven insights for sports analytics and predictions.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Home_or_Away.py'>Home_or_Away.py</a></b></td>
					<td style='padding: 8px;'>- Provides real-time mapping of NBA players to their home or away status by fetching the current schedule from StatMuse, integrating it with existing player data, and outputting an updated CSV<br>- Enhances the overall data architecture by enabling context-aware analysis of player performance relative to game location, supporting more accurate insights and decision-making within the sports analytics pipeline.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Last_10_H2H.py'>Last_10_H2H.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates recent head-to-head performance data for NBA players against specific opponents by scraping StatMuse<br>- Facilitates analysis of player form over the last 10 matchups, enriching datasets with detailed statistics<br>- Integrates seamlessly into the broader data pipeline, supporting advanced sports analytics and predictive modeling efforts.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/Processing_Data.py'>Processing_Data.py</a></b></td>
					<td style='padding: 8px;'>- Performs comprehensive data cleaning and feature engineering on a basketball dataset, including removing irrelevant columns, handling missing values, encoding categorical variables, and standardizing team identifiers<br>- Produces a refined dataset optimized for predictive modeling or analysis, ensuring consistency and readiness for downstream machine learning tasks within the overall data processing pipeline.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/H2H_CurrentSeason.py'>H2H_CurrentSeason.py</a></b></td>
					<td style='padding: 8px;'>- Aggregates head-to-head season statistics for NBA players against specific opponents by scraping data from Statmuse<br>- It processes input CSV data, retrieves relevant matchup details, and outputs structured performance metrics, enabling comparative analysis of player performance within the broader data architecture<br>- This module enhances insights into player matchups for strategic decision-making.</td>
				</tr>
				<tr style='border-bottom: 1px solid #eee;'>
					<td style='padding: 8px;'><b><a href='https://github.com/willh3518/Sports-betting-AI/blob/master/Data_Extraction/PrizePicks_Scraper.py'>PrizePicks_Scraper.py</a></b></td>
					<td style='padding: 8px;'>- Fetches and processes real-time PrizePicks player projections, filtering for todays relevant data<br>- Generates a structured CSV with player details, game info, and prop statistics, supporting analysis of current betting opportunities<br>- Integrates API data with internal mappings to ensure accurate, up-to-date insights aligned with the overall data extraction and analysis architecture.</td>
				</tr>
			</table>
		</blockquote>
	</details>
</details>

---

## Getting Started

### Prerequisites

This project requires the following dependencies:

- **Programming Language:** Python
- **Package Manager:** Conda

### Installation

Build Sports-betting-AI from the source and install dependencies:

1. **Clone the repository:**

    ```sh
    ❯ git clone https://github.com/willh3518/Sports-betting-AI
    ```

2. **Navigate to the project directory:**

    ```sh
    ❯ cd Sports-betting-AI
    ```

3. **Install the dependencies:**

**Using [conda](https://docs.conda.io/):**

```sh
❯ conda env create -f conda.yml
```

### Usage

Run the project with:

**Using [conda](https://docs.conda.io/):**

```sh
conda activate {venv}
python {entrypoint}
```

### Testing

Sports-betting-ai uses the {__test_framework__} test framework. Run the test suite with:

**Using [conda](https://docs.conda.io/):**

```sh
conda activate {venv}
pytest
```

---

## Contributing

- **💬 [Join the Discussions](https://github.com/willh3518/Sports-betting-AI/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/willh3518/Sports-betting-AI/issues)**: Submit bugs found or log feature requests for the `Sports-betting-AI` project.
- **💡 [Submit Pull Requests](https://github.com/willh3518/Sports-betting-AI/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/willh3518/Sports-betting-AI
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/willh3518/Sports-betting-AI/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=willh3518/Sports-betting-AI">
   </a>
</p>
</details>

---

## Acknowledgments

- Credit `contributors`, `inspiration`, `references`, etc.

<div align="left"><a href="#top">⬆ Return</a></div>

---

# MLB_Dashboard/config.py
import os

# Base directory of the MLB_Dashboard
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Path to the parent directory (main project)
PARENT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))

# Paths to data directories
MLB_RESULTS_DIR = os.path.join(PARENT_DIR, 'MLB_Results')
MODEL_TRACKING_FILE = os.path.join(PARENT_DIR, 'model_tracking.csv')

# Flask configuration
DEBUG = True
PORT = 5001  # Use a different port than your main app
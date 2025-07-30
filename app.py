import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="Omniscience MLB Dashboard", layout="wide")

# Load API key securely
API_KEY = st.secrets["API_KEY"]
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Define API endpoints
BASE_URL = "https://api.yoursportsdata.com"  # Replace with actual
MLB_COMPETITION_ID = 1

# ---- Functions ----
def fetch_historic_odds(date):
    """Get historic MLB odds for a specific date."""
    url = f"{BASE_URL}/odds/historic"
    params = {
        "competition_id": MLB_COMPETITION_ID,
        "date": date.strftime("%Y-%m-%d")
    }
    res = requests.get(url, headers=HEADERS, params=params)
    return res.json()

def fetch_live_odds():
    """Get live MLB odds (today only)."""
    url = f"{BASE_URL}/odds/live"
    params = {
        "competition_id": MLB_COMPETITION_ID
    }
    res = requests.get(url, headers=HEADERS, params=params)
    return res.json()

def run_fibonacci_analysis(odds_data):
    """Mock Fibonacci range analysis."""
    results = []
    for game in odds_data:
        opener = game.get("open_spread", 0)
        closer = game.get("close_spread", 0)
        diff = closer - opener
        fib_levels = {
            "23.6%": opener + diff * 0.236,
            "38.2%": opener + diff * 0.382,
            "61.8%": opener + diff * 0.618,
        }
        results.append({
            "Matchup": game["matchup"],
            "Open": opener,
            "Close": closer,
            "Fib Levels": fib_levels
        })
    return results

def render_analysis(analysis_type, odds_data):
    if analysis_type == "Fibonacci Ranges":
        fib_results = run_fibonacci_analysis(odds_data)
        for row in fib_results:
            st.markdown(f"**{row['Matchup']}**")
            st.write(f"📈 Open: {row['Open']} → Close: {row['Close']}")
            st.json(row["Fib Levels"])
            st.markdown("---")
    else:
        st.info("Other analysis types coming soon.")

# ---- UI ----
st.title("🧠 Omniscience MLB Price Dashboard")
st.markdown("Manual control. MLB only. Full Fibonacci and price action layer active.")

# Date picker
target_date = st.date_input("Select a slate date:", value=datetime.now().date())
data_source = st.radio("Choose Data Source:", ["Live Odds", "Historic Odds"])

# Manual fetch buttons
if data_source == "Live Odds":
    if st.button("📡 Call Live Odds Now"):
        odds_data = fetch_live_odds()
    else:
        odds_data = []
else:
    if st.button("📜 Call Historic Odds Now"):
        odds_data = fetch_historic_odds(target_date)
    else:
        odds_data = []

# If data is loaded
if odds_data:
    st.success(f"{len(odds_data)} games loaded.")
    analysis_type = st.selectbox("Choose analysis engine:", [
        "Fibonacci Ranges",
        "Line Movement",
        "Steam Moves",
        "Convergence Flags"
    ])
    render_analysis(analysis_type, odds_data)
else:
    st.warning("No data loaded yet. Please call the API above.")

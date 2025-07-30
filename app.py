import streamlit as st
import requests
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="Omniscience MLB Dashboard", layout="wide")

API_KEY = st.secrets["API_KEY"]
API_BASE = "https://v1.baseball.api-sports.io/"

# Headers for API requests
HEADERS = {
    "x-apisports-key": API_KEY
}

# Visual status placeholder
status_placeholder = st.empty()

# --- Sidebar controls ---
st.sidebar.title("Controls")

date_selected = st.sidebar.date_input(
    "Select Date to View Slate",
    value=datetime.today()
)

analysis_type = st.sidebar.selectbox(
    "Select Analysis Type",
    options=["None", "Fibonacci Retracement", "Price Movement", "Oscillators"]
)

call_type = st.sidebar.radio(
    "Select Data Call Type",
    options=["Historical Odds", "Live Odds"]
)

fetch_button = st.sidebar.button("📥 Fetch Data")

# Function to fetch MLB odds for a date (historical or live)
def fetch_odds(date_str, call_type):
    if call_type == "Historical Odds":
        # Historical odds require league & season - using MLB league id=1 & season year
        year = int(date_str[:4])
        url = f"{API_BASE}odds"
        params = {
            "league": 1,
            "season": year,
            "date": date_str
        }
    else:
        # Live odds call, no season param
        url = f"{API_BASE}odds"
        params = {
            "league": 1,
            "date": date_str
        }
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API request failed: {e}")
        return None

# Analysis placeholders — implement your Fibonacci & other logic here
def analyze_odds(odds_data, analysis_type):
    if not odds_data or "response" not in odds_data:
        return "No odds data to analyze."

    games = odds_data["response"]
    analysis_results = []

    # Placeholder example: just list game matchups and odds
    for game in games:
        teams = f"{game['teams']['home']['name']} vs {game['teams']['away']['name']}"
        try:
            odds = game["bookmakers"][0]["markets"][0]["outcomes"]
            odds_str = ", ".join([f"{o['name']}: {o['price']}" for o in odds])
        except (IndexError, KeyError):
            odds_str = "Odds unavailable"
        analysis_results.append(f"Game: {teams}\nOdds: {odds_str}")

    # Dummy explanation - replace with Fibonacci etc logic
    explanation = f"Analysis Type: {analysis_type}\n\n" + "\n\n".join(analysis_results)
    return explanation

# --- Main UI ---
st.title("Omniscience MLB Dashboard")

if fetch_button:
    status_placeholder.info("🔄 Fetching data...")
    date_str = date_selected.strftime("%Y-%m-%d")
    data = fetch_odds(date_str, call_type)

    if data:
        status_placeholder.success(f"✅ Data fetched for {date_str} ({call_type})")

        st.subheader(f"MLB Games on {date_str}")
        if data["response"]:
            for game in data["response"]:
                st.markdown(f"**{game['teams']['home']['name']}** vs **{game['teams']['away']['name']}**")
                st.write(f"Date/Time: {game['fixture']['date']}")
                # Show odds from first bookmaker if available
                try:
                    odds = game["bookmakers"][0]["markets"][0]["outcomes"]
                    odds_display = ", ".join([f"{o['name']}: {o['price']}" for o in odds])
                    st.write(f"Odds: {odds_display}")
                except (IndexError, KeyError):
                    st.write("Odds: Unavailable")
                st.write("---")
        else:
            st.warning("No games found for this date.")

        st.subheader("Analysis & Explanation")
        explanation_text = analyze_odds(data, analysis_type)
        st.text_area("Details", explanation_text, height=300)
    else:
        status_placeholder.error("❌ Failed to fetch data.")
else:
    status_placeholder.info("🟡 Waiting for manual data fetch...")

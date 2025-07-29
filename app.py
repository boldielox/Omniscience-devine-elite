import streamlit as st
import requests
from datetime import datetime

# App title
st.set_page_config(page_title="Omniscience Control Center", layout="wide")
st.title("🧠 Omniscience Sports Betting Dashboard")

# 🔐 Securely fetch API key from Streamlit secrets
API_KEY = st.secrets["api_sports"]["key"]
BASE_URL = "https://v3.football.api-sports.io"  # Example; update per sport

# ✅ Status Light Indicator
status_placeholder = st.empty()

def show_status(color="yellow", message="Ingesting data..."):
    status_placeholder.markdown(
        f"<div style='background-color:{color};padding:10px;border-radius:10px;text-align:center;color:white;font-weight:bold;'>"
        f"🔄 {message}</div>",
        unsafe_allow_html=True
    )

# 🔄 Ingest Data Function
@st.cache_data(ttl=600)
def fetch_games():
    show_status("yellow", "Fetching live data...")
    headers = {
        "x-apisports-key": API_KEY
    }

    try:
        # Example endpoint: Today's fixtures (adjust for NBA/MLB/WNBA later)
        today = datetime.now().strftime('%Y-%m-%d')
        url = f"{BASE_URL}/games?date={today}"

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        show_status("green", "✅ Data ingested successfully.")
        return data
    except Exception as e:
        show_status("red", f"❌ Failed to ingest: {e}")
        return None

# 🔃 Run ingestion
games_data = fetch_games()

# 🧠 Command Center UI
st.subheader("🛠 Command Center")

with st.expander("🔍 Data Preview"):
    st.write(games_data if games_data else "No data available.")

# ⏳ Placeholder: Add slate rendering, dropdowns, flags here
st.markdown("---")
st.info("Slate and betting analysis modules coming next.")

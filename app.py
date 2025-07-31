import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from dateutil import parser

# Get API key from Streamlit secrets
API_KEY = st.secrets["api_sports"]["key"]
HEADERS = {"x-apisports-key": API_KEY}

# Constants
MLB_COMPETITION_ID = 1
SEASONS = {
    "2022": {"start": "2022-02-26", "end": "2022-11-06"},
    "2023": {"start": "2023-02-24", "end": "2023-11-02"},
    "2024": {"start": "2024-02-22", "end": "2024-10-31"},
    "2025": {"start": "2025-03-18", "end": "2025-09-23"},
}

st.set_page_config(page_title="Omniscience MLB Dashboard", layout="wide")
st.title("⚾ Omniscience MLB Control Center")

# Sidebar: Season & Date Picker
season = st.sidebar.selectbox("Select MLB Season", list(SEASONS.keys()), index=3)
date = st.sidebar.date_input("Select Date", datetime.today())

# Data Pull Trigger
if st.sidebar.button("🔄 Call Data"):
    with st.spinner("Fetching data..."):
        try:
            # Format Date
            game_date = date.strftime("%Y-%m-%d")
            url = "https://v1.baseball.api-sports.io/games"
            params = {
                "league": MLB_COMPETITION_ID,
                "season": season,
                "date": game_date,
            }

            response = requests.get(url, headers=HEADERS, params=params)
            response.raise_for_status()
            games = response.json().get("response", [])

            if not games:
                st.warning("No games found for that date.")
            else:
                df = pd.DataFrame([
                    {
                        "Date": g["date"][:10],
                        "Home": g["teams"]["home"]["name"],
                        "Away": g["teams"]["away"]["name"],
                        "Status": g["status"]["long"],
                        "Score Home": g["scores"]["home"]["total"],
                        "Score Away": g["scores"]["away"]["total"],
                        "Venue": g["venue"]["name"],
                    }
                    for g in games
                ])
                st.success(f"✅ Loaded {len(df)} games.")
                st.dataframe(df)

                # Save to session state for further analysis
                st.session_state["games_df"] = df

        except requests.exceptions.ConnectionError as e:
            st.error("❌ Network error — check internet or API access.")
            st.exception(e)
        except Exception as e:
            st.error("❌ Failed to load data.")
            st.exception(e)

# If Data Already Loaded
if "games_df" in st.session_state:
    df = st.session_state["games_df"]
    st.subheader("📊 Full Game Breakdown")

    # Simple Analysis Examples (Extend as Needed)
    st.write("### 🔍 Matchup Summaries")
    for i, row in df.iterrows():
        st.markdown(f"""
        **{row['Away']} @ {row['Home']}**
        - 🏟 Venue: {row['Venue']}
        - 🕒 Status: {row['Status']}
        - 🔢 Score: {row['Score Away']} - {row['Score Home']}
        """)
        st.markdown("---")

    




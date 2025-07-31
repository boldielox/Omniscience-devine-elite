import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from dateutil import parser

# --- CONFIG ---
st.set_page_config(page_title="⚾ Omniscience MLB Dashboard", layout="wide")
st.title("⚾ Omniscience MLB Control Center")

# --- API Setup ---
API_KEY = st.secrets["api_sports"]["key"]
HEADERS = {"x-apisports-key": API_KEY}
API_URL = "https://v1.baseball.api-sports.io/games"
MLB_COMPETITION_ID = 1  # Confirm via API-Sports docs if needed

# --- Constants ---
SEASONS = {
    "2022": {"start": "2022-02-26", "end": "2022-11-06"},
    "2023": {"start": "2023-02-24", "end": "2023-11-02"},
    "2024": {"start": "2024-02-22", "end": "2024-10-31"},
    "2025": {"start": "2025-03-18", "end": "2025-09-23"},
}

# --- Sidebar: Season & Date ---
season = st.sidebar.selectbox("Select MLB Season", list(SEASONS.keys()), index=3)
min_date = datetime.strptime(SEASONS[season]["start"], "%Y-%m-%d").date()
max_date = datetime.strptime(SEASONS[season]["end"], "%Y-%m-%d").date()

date = st.sidebar.date_input("Select Date", value=datetime.today(), min_value=min_date, max_value=max_date)

# --- Fetch Button ---
if st.sidebar.button("🔄 Call Data"):
    with st.spinner("Fetching MLB game data..."):
        try:
            params = {
                "league": MLB_COMPETITION_ID,
                "season": season,
                "date": date.strftime("%Y-%m-%d")
            }

            response = requests.get(API_URL, headers=HEADERS, params=params)
            response.raise_for_status()
            games = response.json().get("response", [])

            if not games:
                st.warning(f"No games found for {date}.")
            else:
                df = pd.DataFrame([
                    {
                        "Date": g["date"][:10],
                        "Home": g["teams"]["home"]["name"],
                        "Away": g["teams"]["away"]["name"],
                        "Status": g["status"]["long"],
                        "Score Home": g["scores"]["home"]["total"] if g["scores"]["home"]["total"] is not None else "—",
                        "Score Away": g["scores"]["away"]["total"] if g["scores"]["away"]["total"] is not None else "—",
                        "Venue": g["venue"]["name"] if g["venue"] else "N/A"
                    }
                    for g in games
                ])

                st.session_state["games_df"] = df
                st.success(f"✅ Loaded {len(df)} games.")
                st.dataframe(df)

        except requests.exceptions.RequestException as e:
            st.error("❌ Network/API error occurred.")
            st.exception(e)
        except Exception as e:
            st.error("❌ An unexpected error occurred.")
            st.exception(e)

# --- Post-Fetch Display ---
if "games_df" in st.session_state:
    df = st.session_state["games_df"]
    st.subheader("📊 Full Game Breakdown")

    st.write("### 🔍 Matchup Summaries")
    for _, row in df.iterrows():
        st.markdown(f"""
        **{row['Away']} @ {row['Home']}**
        - 🏟 **Venue**: {row['Venue']}
        - 🕒 **Status**: {row['Status']}
        - 🔢 **Score**: {row['Score Away']} - {row['Score Home']}
        """)
        st.markdown("---")

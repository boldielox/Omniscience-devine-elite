import streamlit as st
import requests
from datetime import datetime
import time

st.set_page_config(page_title="Omniscience Dashboard", layout="wide")

# Visual indicator light for data ingestion status
status_placeholder = st.empty()
button_clicked = st.button("📥 Call Data (Manual Ingestion)")

# Function to fetch data from the API
def fetch_odds_data(year_start, year_end):
    url = "https://v3.football.api-sports.io/odds"
    headers = {
        "x-apisports-key": st.secrets["api_sports"]["key"]
    }

    mlb_competition_id = 1
    seasons = [
        {"year": 2022, "from": "2022-02-26", "to": "2022-11-06"},
        {"year": 2023, "from": "2023-02-24", "to": "2023-11-02"},
        {"year": 2024, "from": "2024-02-22", "to": "2024-10-31"},
        {"year": 2025, "from": "2025-03-18", "to": "2025-09-22"},
    ]

    all_data = []
    for season in seasons:
        if season["year"] < year_start or season["year"] > year_end:
            continue

        query = {
            "league": mlb_competition_id,
            "season": season["year"],
            "date_from": season["from"],
            "date_to": season["to"]
        }

        with st.spinner(f"Fetching {season['year']} odds..."):
            response = requests.get(url, headers=headers, params=query)
            if response.status_code == 200:
                all_data.append(response.json())
            else:
                st.error(f"Failed to fetch for {season['year']}: {response.status_code}")
            time.sleep(1.5)  # avoid rate limits

    return all_data

# Manual trigger
if button_clicked:
    status_placeholder.markdown("🔄 Ingesting data...")
    data = fetch_odds_data(2022, 2025)

    if data:
        st.success("✅ Data ingestion completed.")
        status_placeholder.markdown("🟢 Ready")
    else:
        st.error("❌ No data returned.")
        status_placeholder.markdown("🔴 Failed")
else:
    status_placeholder.markdown("🟡 Awaiting ingestion...")

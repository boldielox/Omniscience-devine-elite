import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Omniscience MLB Odds Dashboard", layout="wide")

API_KEY = st.secrets["api_sports"]["key"]

st.title("Omniscience MLB Odds Dashboard")

# Date input for the slate (default to today)
game_date = st.date_input("Select game date", datetime.today())

# Dropdown for analysis type (expand as you build more)
analysis_type = st.selectbox("Select Analysis Type", ["Price Analytics", "Fibonacci Analysis", "Other (coming soon)"])

# Manual trigger button
if st.button("Fetch MLB Odds Data"):
    with st.spinner("Fetching MLB odds data..."):
        url = "https://v3.baseball.api-sports.io/odds"
        headers = {"x-apisports-key": API_KEY}
        params = {"date": game_date.strftime("%Y-%m-%d")}

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            # Basic sanity check
            if data.get("response"):
                st.success(f"Fetched {len(data['response'])} games for {game_date}")
                
                # Display simple table of games and odds (example)
                games = []
                for game in data["response"]:
                    fixture = game["fixture"]
                    teams = game["teams"]
                    bookmakers = game.get("bookmakers", [])
                    # Show matchup and first bookmaker's moneyline odds if available
                    if bookmakers:
                        odds = bookmakers[0]["markets"][0]["outcomes"]
                        ml_teams = {o["name"]: o["price"] for o in odds}
                        games.append({
                            "Home": teams["home"]["name"],
                            "Away": teams["away"]["name"],
                            "Home ML": ml_teams.get(teams["home"]["name"], "N/A"),
                            "Away ML": ml_teams.get(teams["away"]["name"], "N/A"),
                            "Date": fixture["date"][:10]
                        })
                st.table(games)

                # Show analysis placeholder
                st.markdown(f"### Analysis: {analysis_type}")
                st.info("Analysis engine coming soon — this will show Fibonacci retracement and price analytics based on odds data.")
            else:
                st.error("No games found for this date.")
        else:
            st.error(f"API error: {response.status_code} - {response.text}")

else:
    st.info("Select a date and analysis type, then press the button to fetch data.")

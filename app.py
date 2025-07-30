import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Omniscience: MLB Price Analytics", layout="wide")

st.sidebar.title("Omniscience Control Panel")

odds_mode = st.sidebar.radio("Data Source", ["Historic Odds", "Live Odds"])
selected_date = st.sidebar.date_input("Select Date", value=datetime(2025, 7, 29))

target_date = selected_date.strftime("%Y-%m-%d")
competition_id = 1  # MLB

call_data = st.sidebar.button("📡 Call Data")

st.title("🧠 Omniscience: MLB Price Analytics Dashboard")
st.subheader(f"🎯 Target Date: {target_date} | Mode: {odds_mode}")

if call_data:
    st.info("Calling data... please wait.")
    
    api_key = st.secrets["api_sports"]["key"]

    if odds_mode == "Historic Odds":
        endpoint = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds-history/?date={target_date}&regions=us&markets=h2h,spreads,totals&apiKey={api_key}"
    else:
        endpoint = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?regions=us&markets=h2h,spreads,totals&apiKey={api_key}"

    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            games = response.json()
            if not games:
                st.warning("No games found for the selected date.")
            else:
                for game in games:
                    teams = f"{game['home_team']} vs {game['away_team']}"
                    commence = datetime.fromisoformat(game['commence_time'].replace("Z", "+00:00"))
                    st.markdown(f"### {teams}  —  🕒 {commence.strftime('%I:%M %p')}")

                    for bookmaker in game.get("bookmakers", []):
                        st.markdown(f"**{bookmaker['title']}**")
                        for market in bookmaker.get("markets", []):
                            st.markdown(f"*{market['key']}*")
                            for outcome in market["outcomes"]:
                                st.write(f"{outcome['name']}: {outcome['price']}")
                        st.markdown("---")
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")

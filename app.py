import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# Load API key securely from Streamlit secrets
API_KEY = st.secrets["API_KEY"]

# Title
st.set_page_config(page_title="Omniscience Price Engine", layout="wide")
st.title("⚾ Omniscience MLB Price Intelligence")

# Sidebar controls
st.sidebar.header("🔌 Data Source Controls")
data_mode = st.sidebar.radio("Select Data Type", ["Historic Odds", "Live Odds"])
date_input = st.sidebar.date_input("Target Date", datetime.today()).strftime("%Y-%m-%d")

trigger = st.sidebar.button("📡 Call Data")

# Placeholder for results
status_box = st.empty()
result_box = st.container()

# --- Define analysis functions ---
def get_data(data_mode, date):
    if data_mode == "Historic Odds":
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds-history/?regions=us&date={date}&apikey={API_KEY}"
    else:
        url = f"https://api.the-odds-api.com/v4/sports/baseball_mlb/odds/?regions=us&markets=h2h,spreads,totals&date={date}&apikey={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        raise ValueError(f"API Error {response.status_code}: {response.text}")
    return response.json()

def fib_levels(high, low):
    diff = high - low
    return {
        "0.0%": high,
        "23.6%": high - 0.236 * diff,
        "38.2%": high - 0.382 * diff,
        "50.0%": high - 0.5 * diff,
        "61.8%": high - 0.618 * diff,
        "78.6%": high - 0.786 * diff,
        "100.0%": low,
    }

def apply_fibonacci(df):
    fib_results = []
    for _, row in df.iterrows():
        try:
            prices = [float(row['home_price']), float(row['away_price'])]
            high = max(prices)
            low = min(prices)
            fib = fib_levels(high, low)
            fib_results.append({**row, **fib})
        except:
            continue
    return pd.DataFrame(fib_results)

def oscillator(df):
    df["avg_price"] = (df["home_price"] + df["away_price"]) / 2
    df["oscillator"] = df["avg_price"].rolling(window=3).mean() - df["avg_price"].rolling(window=6).mean()
    return df

# --- On Trigger ---
if trigger:
    try:
        status_box.info("⏳ Fetching and analyzing data...")
        raw_data = get_data(data_mode, date_input)

        extracted = []
        for game in raw_data:
            home = game.get("home_team", "NA")
            away = game.get("away_team", "NA")
            for bookmaker in game.get("bookmakers", []):
                for market in bookmaker.get("markets", []):
                    if market["key"] == "h2h":
                        try:
                            prices = {o["name"]: o["price"] for o in market["outcomes"]}
                            extracted.append({
                                "matchup": f"{away} @ {home}",
                                "home_team": home,
                                "away_team": away,
                                "book": bookmaker["title"],
                                "home_price": prices.get(home, None),
                                "away_price": prices.get(away, None),
                                "last_update": market["last_update"]
                            })
                        except:
                            continue

        df = pd.DataFrame(extracted)
        df = df.dropna(subset=["home_price", "away_price"])

        df = apply_fibonacci(df)
        df = oscillator(df)

        result_box.subheader("📊 Price Analysis Engine Output")
        st.dataframe(df.style.format(subset=["home_price", "away_price", "oscillator"], formatter="{:.2f}"))

        status_box.success(f"✅ {len(df)} matchups analyzed for {date_input}")
    except Exception as e:
        status_box.error(f"⚠️ Error: {str(e)}")

import streamlit as st import requests from datetime import datetime

Set up page config

st.set_page_config(page_title="Omniscience Control Center", layout="wide") st.title("Omniscience MLB Ingestion Dashboard")

Ingestion status indicator

if "ingestion_status" not in st.session_state: st.session_state.ingestion_status = "idle"

status_color = { "idle": "gray", "loading": "orange", "success": "green", "error": "red" }

st.markdown( f""" <div style='width:20px;height:20px;border-radius:50%;background-color:{status_color[st.session_state.ingestion_status]};display:inline-block;margin-right:10px'></div> <span style='font-size:18px'>Ingestion Status: <strong>{st.session_state.ingestion_status.upper()}</strong></span> """, unsafe_allow_html=True )

API Key from secrets

API_KEY = st.secrets["api_sports_key"] HEADERS = { "x-apisports-key": API_KEY }

Season data

SEASONS = [ {"year": 2022, "from": "2022-02-26", "to": "2022-11-06"}, {"year": 2023, "from": "2023-02-24", "to": "2023-11-02"}, {"year": 2024, "from": "2024-02-22", "to": "2024-10-31"}, {"year": 2025, "from": "2025-03-18", "to": "2025-09-22"}, ]

COMPETITION_ID = 1

Manual ingestion trigger

if st.button("Call Data"): st.session_state.ingestion_status = "loading" try: for season in SEASONS: url = ( f"https://v3.american-api.com/baseball/fixtures?" f"league={COMPETITION_ID}&season={season['year']}" f"&from={season['from']}&to={season['to']}" ) response = requests.get(url, headers=HEADERS) if response.status_code != 200: raise Exception(f"Error in {season['year']} call: {response.status_code}") st.success(f"Ingested season {season['year']}") st.session_state.ingestion_status = "success" except Exception as e: st.session_state.ingestion_status = "error" st.error(f"Ingestion failed: {e}")

st.write("\n---\n") st.markdown("## Next: Add Command Center, Slate Display, and Analysis")


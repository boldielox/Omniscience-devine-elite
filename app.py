import streamlit as st

st.set_page_config(page_title="Omniscience", layout="wide")

st.title("🔮 Omniscience Sports Betting Control Center")

st.write("Welcome to the Omniscience Model Dashboard. Choose your operation below.")

menu = st.selectbox("Select Mode", ["Flag High-Confidence Picks", "Input Betting Lines", "Run Simulation", "View Logs"])

if menu == "Flag High-Confidence Picks":
    st.success("📌 High-confidence picks will be listed here.")
elif menu == "Input Betting Lines":
    st.text_input("Paste today's lines here (or upload file):")
    st.file_uploader("Upload screenshot or CSV", type=["png", "jpg", "csv"])
elif menu == "Run Simulation":
    st.info("Simulations and projections will be generated here.")
elif menu == "View Logs":
    st.code("Fetching historical logs and bet tracking...")

st.caption("Omniscience v1.0 — Streamlit Deployment")

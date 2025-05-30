from fcl_dashboard import fcl_dashboard
import streamlit as st

selected_dashboard = st.sidebar.selectbox(
    "SELECT DASHBOARD",
    ["FCL DASHBOARD", "SBC DASHBOARD"]
)
if selected_dashboard == "FCL DASHBOARD":
    fcl_dashboard()

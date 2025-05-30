import streamlit as st
# Download this first: pip install xlwt streamlit pyodbc xlrd xlsxwriter sqlalchemy pymysql matplotlib plotly

st.set_page_config(
    page_title="Campaign Automations",
    layout="wide",
    initial_sidebar_state="expanded"
)

pages = {"PAGES": [
        st.Page("dashboard.py", icon="📊", title="DASHBOARD"),
        st.Page("automations.py", icon ="🤖", title="AUTOMATIONS"),
        st.Page("reports.py", icon = "📑", title="REPORTS"),
        st.Page("history.py", icon = "📚", title="HISTORY")
    ],}

pg = st.navigation(pages)
pg.run() 
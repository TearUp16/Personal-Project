import streamlit as st
import time
from loader import show_loader
# Download this first: pip install xlwt streamlit pyodbc xlrd xlsxwriter sqlalchemy pymysql matplotlib plotly

st.set_page_config(
    page_title="Campaign Automations",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Show loader only on first visit in session
if 'loader_shown' not in st.session_state:
    loader_placeholder, loader_html = show_loader("Keep the Energy Alive in '25!")
    loader_placeholder.markdown(loader_html, unsafe_allow_html=True)
    import time
    time.sleep(10)  # Replace with actual loading logic if you wish
    loader_placeholder.empty()
    st.session_state['loader_shown'] = True

pages = {"PAGES": [
        st.Page("dashboard.py", icon="📊", title="DASHBOARD"),
        st.Page("automations.py", icon ="🔧", title="AUTOMATIONS"),
        st.Page("reports.py", icon = "📑", title="REPORTS"),
        st.Page("chatbot.py", icon = "🤖", title="CHATBOT"),
        st.Page("history.py", icon = "📚", title="HISTORY")
    ],}

pg = st.navigation(pages)
pg.run() 
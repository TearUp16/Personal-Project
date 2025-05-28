import streamlit as st
import pyodbc
import pandas as pd
from fcl_drive import fcl_drive_for_input
from fcl_drive2 import fcl_2nd_drive_for_input
from pif_mapping import pif_legal_mapping
from pif_web_import import pif_legal_website_import_file
from pif_autostat import autostat_fcl
from sbc_reshuff import sbc_reshuff


def read_sql_query(filename):
    with open(filename, 'r') as file:
        query = file.read()
    return query

conn_str = (
    "Driver={MySQL ODBC 5.1 Driver};"
    "Server=192.168.15.197;"
    "Database=bcrm;"
    "UID=abpineda;"
    "PWD=$5ws38DF29nzU;"
    )

conn = pyodbc.connect(conn_str)

# Sidebar Campaign Selection
st.sidebar.title("CAMPAIGN AUTOMATIONS")
selected_category = st.sidebar.selectbox(
    "SELECT CAMPAIGN",
    ["FORECLOSURE", "SBC HOMELOAN"]
)
selected_task = st.sidebar.selectbox(
    "SELECT TASK",
    ["ENDORSEMENT", "PULLOUTS", "PTP"]
)

if selected_task == "ENDORSEMENT":
    if selected_category == "FORECLOSURE":
        st.title("FORECLOSURE")
        fcl_page = st.selectbox(
            "SELECT AUTOMATION",
            [
                "FOR INPUT DATA IN FCL DRIVE",
                "FOR INPUT DATA IN 2ND FCL DRIVE",
                "PIF LEGAL MAPPING",
                "PIF LEGAL WEBSITE IMPORT FILE"
            ]
        )
        if fcl_page == "FOR INPUT DATA IN FCL DRIVE":
            fcl_drive_for_input()
        elif fcl_page == "FOR INPUT DATA IN 2ND FCL DRIVE":
            fcl_2nd_drive_for_input()
        elif fcl_page == "PIF LEGAL MAPPING":
            pif_legal_mapping()
        elif fcl_page == "PIF LEGAL WEBSITE IMPORT FILE":
            pif_legal_website_import_file()

    elif selected_category == "SBC HOMELOAN":
        st.title("SBC HOMELOAN")
        sbc_homeloan = st.selectbox("SELECT AUTOMATION", ["SBC ENDORSEMENT"])

elif selected_task == "PULLOUTS":
    if selected_category == "FORECLOSURE":
        st.title("FORECLOSURE")
        fcl_page = st.selectbox(
            "SELECT AUTOMATION",
            ["AUTOSTAT FOR FCL"]
        )
        if fcl_page == "AUTOSTAT FOR FCL":
            autostat_fcl()

    elif selected_category == "SBC HOMELOAN":
        st.title("SBC HOMELOAN")
        sbc_homeloan = st.selectbox(
            "SELECT AUTOMATION",
            ["FOR PULLOUT ACCOUNTS"]
        )
        if sbc_homeloan == "FOR PULLOUT ACCOUNTS":
            sbc_for_pouts_query = read_sql_query('queries/sbc_for_pouts.sql')
            sbc_for_pouts_remarks_df = pd.read_sql_query(sbc_for_pouts_query, conn)
            container = st.container(border=True)
            container.subheader("SBC HL DATABASE")
            container.dataframe(sbc_for_pouts_remarks_df)
            container.download_button(
                label="DOWNLOAD DATABASE",
                data=sbc_for_pouts_remarks_df.to_csv(index=False).encode('utf-8'),
                file_name='cbs_remarks.csv',
                mime='text/csv'
    )
            sbc_reshuff(sbc_for_pouts_remarks_df)

elif selected_task == "PTP":
    if selected_category == "FORECLOSURE":
        st.write("COMING SOON")

    elif selected_category == "SBC HOMELOAN":
        st.title("SBC HOMELOAN")
        st.write("COMING SOON")
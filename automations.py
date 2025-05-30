import streamlit as st
import pyodbc
import pandas as pd
from fcl_drive import fcl_drive_for_input
from fcl_drive2 import fcl_2nd_drive_for_input
from pif_mapping import pif_legal_mapping
from pif_web_import import pif_legal_website_import_file
from pif_autostat import autostat_fcl
from sbc_reshuff import sbc_reshuff
from sbc_autostat import sbc_autostat
from fcl_placement import fcl_placements

# CONNECTION TO QUERY------------------------------------------------------------------------------------------------
def read_sql_query(filename):
    with open(filename, 'r') as file:
        query = file.read()
    return query

# CREDENTIALS TO ODBC------------------------------------------------------------------------------------------------
conn_str = (
    "Driver={MySQL ODBC 5.1 Driver};"
    "Server=192.168.15.197;"
    "Database=bcrm;"
    "UID=abpineda;"
    "PWD=$5ws38DF29nzU;"
    )

conn = pyodbc.connect(conn_str)

# SIDEBAR CAMPAIGN SELECTION------------------------------------------------------------------------------------------------
st.sidebar.title("CAMPAIGN AUTOMATIONS")
selected_category = st.sidebar.selectbox(
    "SELECT CAMPAIGN",
    ["FORECLOSURE", "SBC HOMELOAN"]
)
selected_task = st.sidebar.selectbox(
    "SELECT TASK",
    ["ENDORSEMENT", "PULLOUTS", "PTP"]
)

# ENDORSEMENT FCL------------------------------------------------------------------------------------------------
if selected_task == "ENDORSEMENT":
    if selected_category == "FORECLOSURE":
        st.title("FORECLOSURE")
        fcl_page = st.selectbox(
            "SELECT AUTOMATION",
            [
                "PIF PLACEMENT",
                "FOR INPUT DATA IN FCL DRIVE",
                "FOR INPUT DATA IN 2ND FCL DRIVE",
                "PIF LEGAL MAPPING",
                "PIF LEGAL WEBSITE IMPORT FILE"  
            ]
        )
        if fcl_page == "PIF PLACEMENT":
            fcl_placements()
        elif fcl_page == "FOR INPUT DATA IN FCL DRIVE":
            fcl_drive_for_input()
        elif fcl_page == "FOR INPUT DATA IN 2ND FCL DRIVE":
            fcl_2nd_drive_for_input()
        elif fcl_page == "PIF LEGAL MAPPING":
            pif_legal_mapping()
        elif fcl_page == "PIF LEGAL WEBSITE IMPORT FILE":
            pif_legal_website_import_file()

# ENDORSEMENT SBC HOMELOAN------------------------------------------------------------------------------------------------
    elif selected_category == "SBC HOMELOAN":
        st.title("SBC HOMELOAN")
        sbc_homeloan = st.selectbox("SELECT AUTOMATION", ["SBC ENDORSEMENT"])

# PULLOUTS/AUTOSTATS FCL------------------------------------------------------------------------------------------------
elif selected_task == "PULLOUTS":
    if selected_category == "FORECLOSURE":
        st.title("FORECLOSURE")
        fcl_page = st.selectbox(
            "SELECT AUTOMATION",
            ["AUTOSTAT FOR FCL"]
        )
        if fcl_page == "AUTOSTAT FOR FCL":
            autostat_fcl()

# PULLOUTS/AUTOSTAT SBC HOMELOAN------------------------------------------------------------------------------------------------
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
    
            warning_needed = False

            # THIS CHECKS THE "FOR PULL OUT"------------------------------------------------------------------------------------------------
        if (sbc_for_pouts_remarks_df['Days Activ'] == 'FOR PULL OUT').any():
            warning_needed = True
        else:
            numeric_days = pd.to_numeric(sbc_for_pouts_remarks_df['Days Activ'], errors='coerce')
            if (numeric_days >= 16).any():
                warning_needed = True

        if warning_needed:
            container.warning("⚠️ NOTE: There are accounts with 16 days or more (FOR PULL OUT).")

        container.subheader("SBC HL DATABASE")
        container.dataframe(sbc_for_pouts_remarks_df)

        container.download_button(
            label="DOWNLOAD DATABASE",
            data=sbc_for_pouts_remarks_df.to_csv(index=False).encode('utf-8'),
            file_name='SBC_REPORT.csv',
            mime='text/csv'
        )
        sbc_reshuff(sbc_for_pouts_remarks_df)
        sbc_autostat(sbc_for_pouts_remarks_df)

# PTP FCL------------------------------------------------------------------------------------------------
elif selected_task == "PTP":
    if selected_category == "FORECLOSURE":
        st.write("COMING SOON")

#PTP SBC HOMELOAN------------------------------------------------------------------------------------------------
    elif selected_category == "SBC HOMELOAN":
        st.title("SBC HOMELOAN")
        st.write("COMING SOON")
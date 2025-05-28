import streamlit as st
import pyodbc
import pandas as pd

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

st.sidebar.title("DAILY REPORTS")
selected_client = st.sidebar.selectbox(
    "SELECT CLIENT",
    ["PIF","CBS","MASTERLIST"]
)
if selected_client == "PIF":
    container = st.container(border=True)
    container.title("PIF MASTERLIST")
    fcl_masterlist_query = read_sql_query('queries/fcl_masterlist.sql')
    fcl_masterlist_df = pd.read_sql_query(fcl_masterlist_query, conn)
    container.dataframe(fcl_masterlist_df)
    container.download_button(
        label="Download Report",
        data=fcl_masterlist_df.to_csv(index=False).encode('utf-8'),
        file_name='cbs_remarks.csv',
        mime='text/csv'
    )

elif selected_client == "CBS":
    st.title("CBS REMARKS")
    cbs_remarks_query = read_sql_query('queries/cbs_remarks.sql')
    cbs_remarks_df = pd.read_sql_query(cbs_remarks_query, conn)
    st.dataframe(cbs_remarks_df)
    st.download_button(
        label="Download Report",
        data=cbs_remarks_df.to_csv(index=False).encode('utf-8'),
        file_name='cbs_remarks.csv',
        mime='text/csv'
    )

elif selected_client == "MASTERLIST":
    st.title("MASTERLIST")
    masterlist_query = read_sql_query('queries/masterlist.sql')
    masterlist_df = pd.read_sql_query(masterlist_query, conn)
    st.dataframe(masterlist_df)
    st.download_button(
        label="Download Report",
        data=masterlist_df.to_csv(index=False).encode('utf-8'),
        file_name='masterlist.csv',
        mime='text/csv'
    )

import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px

def sbc_dashboard():
    # ODBC Connection
    conn_str = (
        "Driver={MySQL ODBC 5.1 Driver};"
        "Server=192.168.15.197;"
        "Database=bcrm;"
        "UID=abpineda;"
        "PWD=$5ws38DF29nzU;"
    )
    conn = pyodbc.connect(conn_str)

    # Read your query from a .sql file
    with open("queries/sbc_for_pouts.sql", "r") as f:
        query = f.read()

    # Query the database
    df = pd.read_sql_query(query, conn)
    conn.close()

    # --- Data cleaning/processing ---
    df['ENDO DATE'] = pd.to_datetime(df['ENDO DATE'], errors='coerce')
    df['PULL OUT DATE'] = pd.to_datetime(df['PULL OUT DATE'], errors='coerce')
    df['DateProcessed'] = pd.to_datetime(df['DateProcessed'], errors='coerce')
    df['Status'] = df['Days Activ'].apply(lambda x: 'FOR PULL OUT' if x == 'FOR PULL OUT' else 'Active')

    # --- Title with Logo ---
    col_img, col_title = st.columns([1, 7])
    with col_img:
        st.image("security-bank-logo.jpg", width=120)
    with col_title:
        st.markdown(
            """
            <h1 style='padding-top: 5px; margin-bottom:0px;'>SBC HOMELOAN</h1>
            """,
            unsafe_allow_html=True
        )
    st.markdown("---")

    # --- KPIs (all data) ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Accounts", f"{len(df):,}")
    col2.metric("Outstanding Balance", f"₱ {df['OUTSTANDING BALANCE'].sum():,.2f}")
    col3.metric("FOR PULL OUT", df[df['Status']=='FOR PULL OUT'].shape[0])

    st.markdown("---")

    # --- Visualizations (all data) ---
    st.subheader("Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        agent_leads = df['AGENT TAG'].value_counts().reset_index()
        agent_leads.columns = ['Agent Tag', 'Number of Leads']
        fig1 = px.bar(agent_leads, 
                      x='Agent Tag', 
                      y='Number of Leads', 
                      title='Leads by Agent', 
                      color_discrete_sequence=['#0072BC']
                      )
        
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        status_count = df['Status'].value_counts().reset_index()
        status_count.columns = ['Status', 'Count']
        fig2 = px.pie(status_count, 
                      names='Status', 
                      values='Count', 
                      title='Status Distribution',  
                      color_discrete_sequence=['#0072BC', '#D4DF55']
                      )
        st.plotly_chart(fig2, use_container_width=True)

    fig3 = px.histogram(
        df, 
        x='ENDO DATE', 
        nbins=30, 
        title="Leads Endorsed Over Time",
        color_discrete_sequence=['#D4DF55']
    )

    st.plotly_chart(fig3, use_container_width=True)

# If running as a standalone file, call the function
if __name__ == "__main__":
    sbc_dashboard()

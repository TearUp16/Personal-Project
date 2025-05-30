import streamlit as st
import pyodbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

def fcl_dashboard():
    # Centered title with border at the top
    st.markdown("""
        <h1 style="
            text-align: center; 
            border: 3px solid #2E2F3B;
            padding: 10px; 
            border-radius: 8px;
            color: white;
            background-color: #2E2F3B;
            font-family: Arial, sans-serif;
            ">
            DASHBOARD
        </h1>
    """, unsafe_allow_html=True)

    conn_str = (
        "Driver={MySQL ODBC 5.1 Driver};"
        "Server=192.168.15.197;"
        "Database=bcrm;"
        "UID=abpineda;"
        "PWD=$5ws38DF29nzU;"
    )
    conn = pyodbc.connect(conn_str)

    def read_sql_query(filepath):
        with open(filepath, 'r') as file:
            return file.read()

    query_masterlist = read_sql_query('queries/fcl_masterlist.sql')
    df_masterlist = pd.read_sql_query(query_masterlist, conn)

    # Only keep these ACCOUNT TYPEs
    allowed_types = ["FCL PEJF", "FCL NOF", "FCL 2ND", "FCL 3RD"]
    df_masterlist = df_masterlist[df_masterlist['ACCOUNT TYPE'].isin(allowed_types)]

    bg_color = '#2E2F3B'

    # Dropdown filter for ACCOUNT TYPE
    account_types = sorted(df_masterlist['ACCOUNT TYPE'].dropna().unique().tolist())
    selected_account_type = st.selectbox("ACCOUNT TYPE", ['All'] + account_types)

    # Metrics (filtered data or all)
    if selected_account_type == 'All':
        filtered_df = df_masterlist
    else:
        filtered_df = df_masterlist[df_masterlist['ACCOUNT TYPE'] == selected_account_type]

    num_accounts = filtered_df.shape[0]
    total_amount_due = filtered_df['AMOUNT DUE'].sum()
    total_out_balance = filtered_df['OUT BALANCE'].sum()

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown(f"""
            <div style="
                background-color: #2E2F3B; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center;">
                <h3 style='color: white; margin-bottom: 5px;'>Active Accounts</h3>
                <p style='font-size: 24px; color: #40E0D0; margin: 0;'>{num_accounts:,}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
            <div style="
                background-color: #2E2F3B; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center;">
                <h3 style='color: white; margin-bottom: 5px;'>Principal Balance</h3>
                <p style='font-size: 24px; color: #FFD700; margin: 0;'>₱ {total_amount_due:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)

    with col_c:
        st.markdown(f"""
            <div style="
                background-color: #2E2F3B; 
                padding: 20px; 
                border-radius: 8px; 
                text-align: center;">
                <h3 style='color: white; margin-bottom: 5px;'>Outstanding Balance</h3>
                <p style='font-size: 24px; color: #FF6347; margin: 0;'>₱ {total_out_balance:,.2f}</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

    # Prepare full data for charts (filtered only)
    summary_df = df_masterlist.groupby('ACCOUNT TYPE')['AMOUNT DUE'].sum().reset_index()
    out_balance_summary = df_masterlist.groupby('ACCOUNT TYPE')['OUT BALANCE'].sum().reset_index()
    out_balance_summary['OUT BALANCE (B)'] = out_balance_summary['OUT BALANCE'] / 1_000_000_000
    out_balance_summary['hover_text'] = out_balance_summary['OUT BALANCE (B)'].apply(lambda x: f"{x:,.2f}B")

    # Left Chart: line plot
    fig_left = px.line(
        summary_df,
        x='ACCOUNT TYPE',
        y='AMOUNT DUE',
        title='Principal Balance by Account Type',
        markers=True,
        template='plotly_dark',
        labels={'AMOUNT DUE': 'Principal Balance', 'ACCOUNT TYPE': 'Account Type'}
    )

    if selected_account_type == 'All':
        fig_left.update_traces(
            line=dict(color='#40E0D0', width=3),
            marker=dict(color='#FFD700', size=10, line=dict(color='#DAA520', width=2))
        )
    else:
        fig_left.update_traces(
            line=dict(color='#555555', width=2),
            marker=dict(color='#888888', size=8)
        )
        selected_row = summary_df[summary_df['ACCOUNT TYPE'] == selected_account_type]
        if not selected_row.empty:
            fig_left.add_trace(go.Scatter(
                x=selected_row['ACCOUNT TYPE'],
                y=selected_row['AMOUNT DUE'],
                mode='markers+lines',
                marker=dict(color='#FFD700', size=14, line=dict(color='#DAA520', width=3)),
                line=dict(color='#FFD700', width=5),
                showlegend=False
            ))

    fig_left.update_layout(
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color='white', size=12),
        xaxis_tickangle=45,
        height=350
    )

    # Right Chart: bar plot
    if selected_account_type == 'All':
        out_balance_summary['highlight'] = True
    else:
        out_balance_summary['highlight'] = out_balance_summary['ACCOUNT TYPE'] == selected_account_type

    fig_right = px.bar(
        out_balance_summary,
        x='ACCOUNT TYPE',
        y='OUT BALANCE (B)',
        color=out_balance_summary['highlight'].map({True: '#FF6347', False: '#444444'}),
        color_discrete_map='identity',
        title='Outstanding Balance by Account Type',
        template='plotly_dark',
        labels={'ACCOUNT TYPE': 'Account Type', 'OUT BALANCE (B)': 'OB'},
        height=350,
        hover_data={'OUT BALANCE (B)': False},
        custom_data=['hover_text']
    )

    fig_right.update_traces(
        hovertemplate='%{customdata[0]}<extra></extra>'
    )

    max_val = out_balance_summary['OUT BALANCE (B)'].max()
    tick_vals = np.linspace(0, max_val, num=5)
    tick_texts = [f"{int(round(v))}B" for v in tick_vals]

    fig_right.update_layout(
        yaxis=dict(
            tickmode='array',
            tickvals=tick_vals,
            ticktext=tick_texts,
        ),
        yaxis_title='Outstanding Balance',
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color='white', size=12),
        xaxis_tickangle=45,
        showlegend=False
    )

    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(fig_left, use_container_width=True)

    with col2:
        st.plotly_chart(fig_right, use_container_width=True)

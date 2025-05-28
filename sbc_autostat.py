import streamlit as st
import pandas as pd
import xlwt
from io import BytesIO
from datetime import datetime

def df_to_xls_download(df, container):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet1')

    # Write header
    for col_idx, col_name in enumerate(df.columns):
        ws.write(0, col_idx, col_name)

    # Write data rows
    for row_idx, row in enumerate(df.itertuples(index=False), start=1):
        for col_idx, value in enumerate(row):
            ws.write(row_idx, col_idx, value)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    today_str = datetime.today().strftime('%Y-%m-%d')
    filename = f'AUTO STATUS{today_str}.xls'

    container.download_button(
        label="DOWNLOAD AUTOSTAT",
        data=output,
        file_name=filename,
        mime="application/vnd.ms-excel"
    )

def sbc_autostat(main_df):
    container = st.container(border=True)

    with container:
        st.subheader("FOR AUTOSTAT")

    # Filter the main_df for pullout accounts (Days Activ == 'FOR PULL OUT' or >=16)
    # Convert Days Activ to numeric where possible for comparison
    days_col = main_df['Days Activ']
    mask_for_pullout = (days_col == 'FOR PULL OUT') | (pd.to_numeric(days_col, errors='coerce') >= 16)
    filtered = main_df[mask_for_pullout].copy()

    if filtered.empty:
        container.warning("No accounts with 'FOR PULL OUT' status found.")
        return

    # User picks the date for notes column
    user_date = container.date_input("SELECT DATE OF EXPIRATION:", datetime.today())

    # Create new DataFrame with requested headers and rules
    export_df = pd.DataFrame({
        'chcode': filtered['CH CODE'].values,
        'status': 'RETURNS',
        'substatus': 'PULLOUT',
        'amount': '',
        'start_date': '',
        'end_date': '',
        'or_number': '',
        'notes': f"END OF HANDLING PERIOD {user_date.strftime('%m/%d/%Y')}",
        'new_address': '',
        'new_contact': '',
        'agent': 'POUT',
        'barcode_date': datetime.now().strftime('%m/%d/%y %I:%M %p')
    })

    container.subheader("Export Data Preview")
    container.dataframe(export_df)

    df_to_xls_download(export_df, container)

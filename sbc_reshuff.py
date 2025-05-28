import streamlit as st
from io import BytesIO
import xlwt
from datetime import datetime

def df_to_xls_download(df, container):
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Sheet1')

    for row_idx, row in enumerate(df.itertuples(index=False)):
        for col_idx, value in enumerate(row):
            ws.write(row_idx, col_idx, value)

    output = BytesIO()
    wb.save(output)
    output.seek(0)

    today_str = datetime.today().strftime('%Y.%m.%d')
    filename = f'POUT {today_str}.xls'

    container.download_button(
        label="DOWNLOAD POUTS",
        data=output,
        file_name=filename,
        mime="application/vnd.ms-excel"
    )

def sbc_reshuff(df):
    container = st.container(border=True)
    container.subheader("FOR RESHUFF")
    filtered_df = df[df['Days Activ'] == 'FOR PULL OUT'].copy()

    if filtered_df.empty:
        container.warning("No accounts with 'FOR PULL OUT' status found.")
        return

    filtered_df['POUT'] = 'POUT'
    
    container.dataframe(filtered_df[['CH CODE', 'POUT']])
    df_to_xls_download(filtered_df[['CH CODE', 'POUT']], container)

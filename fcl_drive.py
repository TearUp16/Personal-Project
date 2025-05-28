import pandas as pd
import streamlit as st
import io
import os

COLUMNS_TO_COPY = [
    "AREA",
    "Ch Code",
    "HlidNo",
    "LastName",
    "FirstName",
    "MidName",
    "LastName, FirstName MidName",
    "ENDO DATE",
    "PROD TYPE",
    "BATCH_NO",
    "PresentAddress",
    "PermanentAddress",
    "Pri Area",
    "Pri City/Muni"
]
def fcl_drive_for_input():
    container = st.container(border=True) 
    container.subheader("FOR INPUT DATA IN FCL DRIVE")
    container.write("UPLOAD YOUR 'BCRM UPLOAD' FILE HERE")

    uploaded_file = container.file_uploader("Choose a file", type=["xls", "xlsx"], key="file_uploader")

    if uploaded_file:
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            if file_extension == ".xls":
                df = pd.read_excel(uploaded_file, engine="xlrd", index_col=False)
            else:
                df = pd.read_excel(uploaded_file, index_col=False)

            if "HlidNo" in df.columns:
                df["HlidNo"] = df["HlidNo"].astype(str)
                
        except Exception as e:
            container.error(f"Error reading Excel file: {e}")
        else:
            missing_cols = [col for col in COLUMNS_TO_COPY if col not in df.columns]
            if missing_cols:
                container.error(f"The following columns are missing in the uploaded file: {', '.join(missing_cols)}")
            else:
                cleaned_df = df[COLUMNS_TO_COPY]
                cleaned_df["MidName"] = cleaned_df["MidName"].astype(str).str[0]
                container.subheader("Cleaned Data")
                container.dataframe(cleaned_df)

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    cleaned_df.to_excel(writer, index=False, sheet_name="Cleaned Data")
                processed_data = output.getvalue()

                container.download_button(
                    label="Download File",
                    data=processed_data,
                    file_name="FOR INPUT IN FCL DRIVE.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
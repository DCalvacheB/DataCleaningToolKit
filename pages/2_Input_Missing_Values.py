import streamlit as st
from utils import data_managment as dm 
from data_cleaning_toolkit import missing_values as mv
import os

st.write("### Input Missing Values")

col1, col2 = st.columns(2)

uploaded_files = dm.get_uploaded_files()
sel_table = col1.selectbox('Tables', uploaded_files)

df = dm.read_file(sel_table)


df_misssum = mv.missing_values_summary(df)
col1.table(df_misssum)

inputation = col2.button("Input Missing Values")



if inputation:
    df1 = mv.fill_missing_values(df)
    dm.save_file(df1, os.path.basename(sel_table), 'output_data', msg=False)
    df_csv = dm.convert_for_download(df1)
    col2.success("Missing values have been inputed.")
    df1_missum = mv.missing_values_summary(df1)
    col2.table(df1_missum)
    col2.download_button(
        label="Download CSV",
        data=df_csv,
        file_name=os.path.basename(sel_table).replace('.csv','')+"_inputvalues.csv",
        mime="text/csv",
        icon=":material/download:",
    )
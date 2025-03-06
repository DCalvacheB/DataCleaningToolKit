import streamlit as st
from utils import data_managment as dm



st.write("### Data Profiler")
col1, col2 = st.columns(2)

def read_and_show():
    uploaded_files = dm.get_uploaded_files()
    sel_table = col1.selectbox('Tables', uploaded_files)

    df = dm.read_file(sel_table)

    show_table = col1.checkbox("Show Table", value=True)
    if show_table:
        col1.table(df.head())
    return df


df = read_and_show()
profile = col2.button('Profile Data')


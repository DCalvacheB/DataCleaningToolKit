import streamlit as st
from utils import data_managment as dm 
from data_cleaning_toolkit import missing_values as mv


st.write("### Missing Values")

col1, col2 = st.columns(2)

uploaded_files = dm.get_uploaded_files()
sel_table = col1.selectbox('Tables', uploaded_files)

df = dm.read_file(sel_table)

view_sel = col1.radio("View", ["Head", "Tail", "Sample"])

if view_sel == "Head":
    col1.table(df.head())
elif view_sel == "Tail":
    col1.table(df.tail())
elif view_sel == "Sample":
    n = col1.number_input("Number of samples", min_value=1, max_value=10, value=5)
    col1.table(df.sample(n).T)


df_misssum = mv.missing_values_summary(df)
col2.table(df_misssum)
missing_vals = df_misssum['Percentage'].sum().sum()!=0
if missing_vals:
    col2.warning("There are missing values in the data. It is recommended to clean the data before proceeding.")

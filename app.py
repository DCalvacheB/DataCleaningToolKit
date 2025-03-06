import streamlit as st
import pandas as pd
import os
from utils.data_managment import read_file, save_file



st.set_page_config(layout="wide")



# Streamlit UI
st.title("🛠 Data Cleaning Toolkit")

# File uploader
uploaded_files = st.sidebar.file_uploader("Upload a file", type=["csv", "xlsx"], 
                                         accept_multiple_files=True, key="uploaded_files")


for file in uploaded_files:
    df = read_file(file)
    st.table(df.head())
    save_file(df, file_name=file.name)
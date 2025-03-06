import pandas as pd
import streamlit as st
import os
import glob 



UPDATA_PATH = 'uploaded_data'

def convert_for_download(df):
    return df.to_csv().encode("utf-8")

def get_uploaded_files():
    """
    Get the list of uploaded files.

    Parameters:
    - None

    Returns:
    - list: The list of uploaded files
    """
    return glob.glob(f'{UPDATA_PATH}/*')

def read_file(file):
    """
    Read a CSV or Excel file into a DataFrame.

    Parameters:
    - file (file object): The file to read.

    Returns:
    - pd.DataFrame: The DataFrame created
    """
    csv = file.split('.')[-1].endswith('csv') if type(file)==str else file.name.endswith('.csv')
    if file is not None:
        if csv:
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        return df
    return None

def save_file(df:pd.DataFrame, file_name:str, path=UPDATA_PATH, msg=True, container=None):
    """
    Save a DataFrame to a CSV file.

    Parameters:
    - df (pd.DataFrame): The DataFrame to save.
    - file_name (str): The name of the file to save the DataFrame to.

    Returns:
    - None
    """
    if df is not None and not os.path.exists(f'{path}/{file_name}'):
        df.to_csv(f'{path}/{file_name}')
    if msg:
        if container is not None:
            container.success('File saved successfully.')
        else:
            st.success('File saved successfully.')
    return None
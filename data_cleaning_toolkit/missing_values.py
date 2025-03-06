import pandas as pd
from sklearn import datasets
import random



def fill_quant_cols(df, strategy:str, col:str)->pd.DataFrame:
    """
    Fill missing values in a quantitative column using a specified strategy.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - strategy (str): The strategy to use for filling missing values. Options are "mean", "median", or "mode".
    - col (str): The column to fill missing values in.

    Returns:
    - pd.DataFrame: A DataFrame with filled missing values.

    """
    if strategy == "mean":
        df.fillna({col: df[col].mean()}, inplace=True)  
    elif strategy == "median":
        df.fillna({col:df[col].median()}, inplace=True)
    elif strategy == "mode":
        df.fillna({col:df[col].mode()[0]}, inplace=True)
    return df

def fill_qual_cols(df, strategy:str, col:str)->pd.DataFrame:
    if strategy == "mode":
        df[col].fillna(df[col].mode()[0], inplace=True)
    elif strategy == "ffill":
        df[col].fillna(method="ffill", inplace=True)
    elif strategy == "bfill":
        df[col].fillna(method="bfill", inplace=True)
    return df

def fill_missing_values(df, strategy=["mean", 'bfill'], configs:dict=None):
    """
    Fill missing values in a DataFrame using a specified strategy.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - strategy (str): The strategy to use for filling missing values. Options are "mean", "median", "mode", "ffill", or "bfill".
    - columns (list, optional): List of column names to apply the strategy to. Defaults to all columns with missing values.

    Returns:
    - pd.DataFrame: A DataFrame with missing values filled.
    """
    if df.isnull().sum().sum()==0 and df.isna().sum().sum()==0:
        print('Data frame has no empty values.')
        return df
    quant_cols = [col for col in df.columns if df[col].dtype!='object']
    qual_cols = [col for col in df.columns if df[col].dtype=='object']

    for col in df.columns:
        if configs is None:
            configs = {}
        try:
            strategy_qan = configs.get(col, strategy[0]) if col in quant_cols else configs.get(col, strategy[0])
            strategy_qal = configs.get(col, strategy[1]) if col in quant_cols else configs.get(col, strategy[1])
        except IndexError:
            if len(strategy)==1:
                strategy_qan = configs.get(col, strategy[0]) if col in quant_cols else configs.get(col, strategy[0])
                strategy_qal = 'bfill'
        if col in quant_cols:
            df = fill_quant_cols(df=df, strategy=strategy_qan, col=col)
        if col in qual_cols:
            df = fill_qual_cols(df=df, strategy=strategy_qal, col=col)
    return df


def drop_missing_values(df, axis=0, threshold=0):
    """
    Drop rows or columns with missing values.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - axis (int): 0 to drop rows, 1 to drop columns.
    - threshold (int, optional): Minimum number of non-NA values required to keep the row or column. Defaults to None.

    Returns:
    - pd.DataFrame: A DataFrame with rows or columns dropped.
    """
    print('Dropping missing values...')
    print('df shape before dropping missing values:', df.shape)
    df1 = df.dropna(axis=axis, thresh=threshold)
    print('df shape after dropping missing values:', df1.shape)
    if df.shape[0] == df1.shape[0]:
        print('No rows dropped.')
    if df.shape[1] == df1.shape[1]:
        print('No columns dropped.')
    
    return df1


def missing_values_summary(df):
    """
    Generate a summary of missing values in the DataFrame.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: A summary with columns ['Column', 'Missing Values', 'Percentage'].
    """
    missing_summary = pd.DataFrame({
        "Column": df.columns,
        "Missing Values": df.isnull().sum(),
        "Percentage": round(df.isnull().mean() * 100, 4)
    })
    missing_summary.reset_index(inplace=True, drop=True)
    if not missing_summary.empty:
        return missing_summary


import pandas as pd

def fill_missing_values(df, strategy="mean", columns=None):
    """
    Fill missing values in a DataFrame using a specified strategy.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.
    - strategy (str): The strategy to use for filling missing values. Options are "mean", "median", "mode", "ffill", or "bfill".
    - columns (list, optional): List of column names to apply the strategy to. Defaults to all columns with missing values.

    Returns:
    - pd.DataFrame: A DataFrame with missing values filled.
    """
    if columns is None:
        columns = df.columns

    for col in columns:
        if col in df.columns and df[col].isnull().any():
            if strategy == "mean":
                df[col].fillna(df[col].mean(), inplace=True)
            elif strategy == "median":
                df[col].fillna(df[col].median(), inplace=True)
            elif strategy == "mode":
                df[col].fillna(df[col].mode()[0], inplace=True)
            elif strategy == "ffill":
                df[col].fillna(method="ffill", inplace=True)
            elif strategy == "bfill":
                df[col].fillna(method="bfill", inplace=True)
            else:
                raise ValueError(f"Unknown strategy: {strategy}")
    return df





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
        "Percentage": (df.isnull().mean() * 100)
    })
    if not missing_summary.empty:
        return missing_summary[missing_summary["Missing Values"] > 0].reset_index(drop=True)
    print('Data frame has no empty values')
    return None

import streamlit as st
from utils import data_managment as dm
import pandas as pd
import numpy as np
from functools import reduce


check, check1, check3, rename_now = False, False, False, False

st.write("### Merge Tables")

tables_to_merge = st.number_input('How many tables do you want to merge?', min_value=2, max_value=5, value=2)

def read_sel_files():
    cols = st.columns(tables_to_merge)
    uploaded_files = dm.get_uploaded_files()

    tables, dfs = [],[]
    for n, col in enumerate(cols):
        tables.append(col.selectbox('Tables', uploaded_files, key=f'{col}_{n}'))

    if len(tables)!=len(set(tables)):
        st.warning("Please select different tables to merge.")
        return None, None
    else:
        for num, table in enumerate(tables):
            df = dm.read_file(table)
            cols[num].table(df.head())
            dfs.append(df)
        
    return dfs, tables


def show_columns(dfs):
    if dfs is None:
        return
    st.write("### Columns in each table")
    cols = st.columns(tables_to_merge)
    for num, df in enumerate(dfs):
        cols[num].table(df.columns)


def rename_cols_menu(dfs:list, rename=st):
    if dfs is None:
        return
    
    new_names = []

    cols = rename.columns(tables_to_merge)
    for num, df in enumerate(dfs):
        cols_names = pd.DataFrame(df.columns, columns=['Original Name'])
        cols_names['New Name'] = ''
        tab = cols[num].data_editor(cols_names, key=f'editor_{num}')
        pairs = np.reshape([j for i in tab.to_dict(orient='records') for j in i.values()], (-1, 2))
        new_names.append({i[0]: i[1] for i in pairs if i[1] != '' and i[0] != i[1]})
    return new_names

def rename_cols_fcn(dfs, new_names, container=st):
    if dfs is None:
        return
    for num, df in enumerate(dfs):
        dfs[num] = df.rename(columns=new_names[num])
    container.success("Columns renamed successfully.")
    st.session_state.renamed_dfs = dfs
    return dfs

def merge_tables(dfs):
    if dfs is None:
        return
    cols_all  = []
    for df in dfs:
        cols_all.append(df.columns.tolist())
    
    common_cols = list(reduce(set.intersection, map(set, cols_all)))
    cols_all = set([j for i in cols_all for j in i])
    selections = st.multiselect('Columns', cols_all, common_cols)

    if selections!=[]:
        df_merged = dfs[0].merge(dfs[1], on=selections, how='inner').head()
        st.table(df_merged)
        return df_merged

def dowload_final(df, tables, container=st):
    if tables is None or df is None:
        return
    df_csv = dm.convert_for_download(df)
    name = '_'.join([tab.replace('.csv', '') for tab in tables])
    container.download_button(
        label="Download CSV",
        data=df_csv,
        file_name=f"{name}_merged_tables.csv",
        mime="text/csv",
        icon=":material/download:",
    )


dfs, tables = read_sel_files()
show_columns(dfs)
rename = st.expander("Rename columns", expanded=False)
rename_now = rename.button("Rename columns now")
new_names = rename_cols_menu(dfs, rename)
if rename_now:
    rename_cols_fcn(dfs, new_names)

dfs = st.session_state.get('renamed_dfs', dfs)
df_merged = merge_tables(dfs)
dowload_final(df_merged, tables)
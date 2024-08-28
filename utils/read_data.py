import os
import pandas as pd
import functools
import polars as pl

# @functools.lru_cache decorator requires that all the arguments passed to the cached function be hashable.
# A pandas.DataFrame is mutable and therefore unhashable. Therefore, we always need to reference the read from CSV, as this is considered non-mutable.

@functools.lru_cache
def read_and_combine_csv_files(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in csv_files]

    df = pd.concat(df_list, ignore_index=True)
    markets_pandas_df = pd.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')

    return pd.merge(df, markets_pandas_df, on='Market', how='inner')

def read_and_combine_csv_files_polars(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pl.read_csv(os.path.join(folder_path, file)) for file in csv_files]
    return_df = pl.concat(df_list)
    return return_df



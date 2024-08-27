import os
import polars as pl
import functools

# Fields to sum
sum_fields = ['Impressions', 'Clicks', 'Cost', 'Revenue']

# Fields to average
mean_fields = ['CTR', 'CPC', 'ROI']

# @functools.lru_cache decorator requires that all the arguments passed to the cached function be hashable.
# A pandas.DataFrame is mutable and therefore unhashable. Therefore, we always need to reference the read from CSV, as this is considered non-mutable.

@functools.lru_cache
def read_and_combine_csv_files(folder_path):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    df_list = [pl.read_csv(os.path.join(folder_path, file)) for file in csv_files]

    df = pl.concat(df_list)
    markets_polars_df = pl.read_csv('synthetic_data/data_csv/dataset_markets/markets.csv')

    return df.join(markets_polars_df, on='Market', how='inner')


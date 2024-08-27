import pandas as pd
import time
import functools
from utils.read_data import read_and_combine_csv_files

# Fields to sum
sum_fields = ['Impressions', 'Clicks', 'Cost', 'Revenue']

# Fields to average
mean_fields = ['CTR', 'CPC', 'ROI']

@functools.lru_cache
def filtering_pandas(folder_path,
                     dates_filter=None,
                     device_filter=None,
                     market_filter=None,
                     ROI_filter=None,
                     list_of_grp_by_fields=None,
                     ) -> pd.DataFrame:

    df = read_and_combine_csv_files(folder_path)

    start_time = time.time()

    if dates_filter:
        # Ensure the filter dates are datetime objects
        df['Date'] = pd.to_datetime(df['Date'])
        start_date = pd.to_datetime(dates_filter[0])
        end_date = pd.to_datetime(dates_filter[1])
        df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    if device_filter:
        df = df[df['Device'].isin(device_filter)]

    if market_filter:
        df = df[df['Market'].isin(market_filter)]

    if ROI_filter:
        df = df[(df['ROI'] >= ROI_filter[0]) & (df['ROI'] <= ROI_filter[1])]

    execution_time = time.time() - start_time
    print('Pandas cached filter: {}'.format(execution_time))

    if list_of_grp_by_fields:
        start_time = time.time()
        df = (df
              .groupby(list(list_of_grp_by_fields))
              .agg({**{field: 'sum' for field in sum_fields},
                    **{field: 'mean' for field in mean_fields}}
                   )
              )

        # Rename columns to clarify which operation was performed
        df.columns = [f'{col}_{"Sum" if col in sum_fields else "Avg"}' for col in df.columns]

        df = df.reset_index()
        execution_time = time.time() - start_time
        print('Pandas cached aggregations: {}'.format(execution_time))

    return df


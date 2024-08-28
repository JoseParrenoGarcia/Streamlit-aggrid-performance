import streamlit as st
from synthetic_data.synthetic_data_generator import datasets, markets
from utils.read_data import read_and_combine_csv_files, read_and_combine_csv_files_polars
from utils.aggrid_config import aggrid_configuration
from utils.filtering import filtering_pandas
import time
from datetime import datetime
from st_aggrid import AgGrid, GridOptionsBuilder

# ---------------------------------------------------------------------
# HOME PAGE - CONFIGURATION
# ---------------------------------------------------------------------
st.set_page_config(
    layout="wide",
)

# ---------------------------------------------------------------------
# HOME PAGE - SIDEBAR
# ---------------------------------------------------------------------
with st.sidebar:
    with st.container(border=True):
        st.write('**How many rows to load?**')
        formatted_datasets = {f"{x:,}": x for x in datasets}
        selected_num_rows = st.radio(label='How many rows to load?', options=list(formatted_datasets.keys()), label_visibility="collapsed")
        num_rows = formatted_datasets[selected_num_rows]

        with st.spinner(text=f'Reading data with {num_rows} rows'):
            folder_path = f'synthetic_data/data_csv/dataset_{num_rows}'
            df = read_and_combine_csv_files(folder_path)
            polars_df = read_and_combine_csv_files_polars(folder_path)

    with st.form('execution_form'):
        submitted = st.form_submit_button("Execute", type="primary")

        st.write('**Aggregate by:**')

        aggregation_fields = st.multiselect('Aggregated by:', options=['Date', 'Device', 'Market'], placeholder='----', label_visibility="collapsed")

        st.write('**Filter by:**')

        date_filter = st.date_input(label="Date filter:",
                                    value=(datetime(2023, 1, 1), datetime(2024, 12, 31)),
                                    min_value=datetime(2023, 1, 1),
                                    max_value=datetime(2024, 12, 31),
                                    format="YYYY-MM-DD")

        device_filter = st.multiselect('Device:', options=['Desktop', 'Mobile'], placeholder='----')

        market_filter = st.multiselect('Market:', options=markets, placeholder='----')

        ROI_filter = st.slider("ROI", 0.75, 1.55, (0.75, 1.55))

        immutable_device_filter = tuple(device_filter) if device_filter else None
        immutable_market_filter = tuple(market_filter) if market_filter else None
        immutable_ROI_filter = tuple(ROI_filter) if ROI_filter else None
        immutable_aggregation_fields = tuple(aggregation_fields) if ROI_filter else None

# ---------------------------------------------------------------------
# HOME PAGE - MAIN CONTENT AREA
# ---------------------------------------------------------------------
with st.container(border=True):
    st.subheader('Rendering AgGrid')
    start_time = time.time()
    aggrid_df, aggrid_polars_df = aggrid_configuration(df)
    execution_time = time.time() - start_time

with st.container(border=True):
    st.subheader('AgGrid execution time')
    st.write('Rendering AgGrid: {}'.format(execution_time))

with st.container(border=True):
    st.subheader('Rendering basic dataframe')
    start_time = time.time()
    filtered_df = filtering_pandas(folder_path=folder_path,
                                   dates_filter=date_filter,
                                   device_filter=immutable_device_filter,
                                   ROI_filter=immutable_ROI_filter,
                                   market_filter=immutable_market_filter,
                                   list_of_grp_by_fields=immutable_aggregation_fields)
    st.dataframe(filtered_df)
    execution_time = time.time() - start_time

with st.container(border=True):
    st.subheader('Basic dataframe execution time')
    st.write('Rendering basic dataframe: {}'.format(execution_time))

with st.container(border=True):
    st.subheader('Rendering AgGrid with polars')
    st.write('This is how the polars dataframe is loaded...')
    st.write(polars_df.head())

    st.write('And this is the error that AgGrid throws when dealing with pandas...')
    standard_AgGrid = AgGrid(polars_df, gridOptions=GridOptionsBuilder.from_dataframe(polars_df).build())



# what dataset to read, radio button. read pufunctool cached
# have a print saying: this is displayed if full-app is re-run
# timeit for rendering table - ready to capture
# timeit for filtering - ready to capture
# timeit for sorting - ready to capture
# timeit for aggregating - ready to capture



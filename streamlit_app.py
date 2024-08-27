import streamlit as st
from synthetic_data.synthetic_data_generator import datasets
from utils.read_data import read_and_combine_csv_files
from utils.aggrid_config import aggrid_configuration
import time

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
    num_rows = st.radio(label='How many rows to load?', options=datasets)

    with st.spinner(text=f'Reading data with {num_rows} rows'):
        df = read_and_combine_csv_files(f'synthetic_data/data_csv/dataset_{num_rows}')

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
    st.dataframe(aggrid_polars_df)


# what dataset to read, radio button. read pufunctool cached
# have a print saying: this is displayed if full-app is re-run
# timeit for rendering table
# timeit for filtering
# timeit for sorting
# timeit for aggregating



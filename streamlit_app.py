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
    with st.container(border=True):
        st.write('**How many rows to load?**')
        formatted_datasets = {f"{x:,}": x for x in datasets}
        selected_num_rows = st.radio(label='How many rows to load?', options=list(formatted_datasets.keys()), label_visibility="collapsed")
        num_rows = formatted_datasets[selected_num_rows]

        with st.spinner(text=f'Reading data with {num_rows} rows'):
            df = read_and_combine_csv_files(f'synthetic_data/data_csv/dataset_{num_rows}')

    with st.container(border=True):
        st.write("**Filtering options for basic streamlit dataframe**")


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
    st.dataframe(df)
    execution_time = time.time() - start_time

with st.container(border=True):
    st.subheader('Basic dataframe execution time')
    st.write('Rendering basic dataframe: {}'.format(execution_time))



# what dataset to read, radio button. read pufunctool cached
# have a print saying: this is displayed if full-app is re-run
# timeit for rendering table - ready to capture
# timeit for filtering
# timeit for sorting - ready to capture
# timeit for aggregating



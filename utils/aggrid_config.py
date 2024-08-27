from st_aggrid import AgGrid, GridOptionsBuilder
import polars as pl

# Wrapping up function
def aggrid_configuration(df):
    grid_builder = GridOptionsBuilder.from_dataframe(df)

    grid_builder.configure_side_bar()
    # grid_builder.configure_default_column(filter=True, groupable=True, value=True, enableRowGroup=True)

    numeric_types = ['numericColumn', 'numberColumnFilter', 'customNumericFormat']
    grid_builder.configure_column('Impressions', type=numeric_types, )
    grid_builder.configure_column('CTR', type=numeric_types,)
    grid_builder.configure_column('Clicks', type=numeric_types,)
    grid_builder.configure_column('CPC', type=numeric_types, )
    grid_builder.configure_column('Cost', type=numeric_types, )
    grid_builder.configure_column('ROI', type=numeric_types, )
    grid_builder.configure_column('Revenue', type=numeric_types, )
    grid_builder.configure_column('clickshare', header_name='Click Share', type=numeric_types, )

    # Build grid options
    gridOptions = grid_builder.build()

    grid_response = AgGrid(df,
                           gridOptions=gridOptions,
                           allow_unsafe_jscode=True,
                           height=min(2000, (len(df)) * 60),  # 38px per row or 500px
                           fit_columns_on_grid_load=False,
                           theme='balham'
                           )

    filtered_df = pl.DataFrame(grid_response['data'])

    # https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html
    return grid_response, filtered_df
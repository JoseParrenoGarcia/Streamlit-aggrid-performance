from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import polars as pl

# Define JsCode for country formatting
countryFormatter = JsCode("""
function(params) {
    const countryEmojis = {
        "UK": "🇬🇧", "US": "🇺🇸", "ES": "🇪🇸", "JP": "🇯🇵", "AU": "🇦🇺",
        "BR": "🇧🇷", "MX": "🇲🇽", "DE": "🇩🇪", "FR": "🇫🇷", "IT": "🇮🇹",
        "CA": "🇨🇦", "CN": "🇨🇳", "IN": "🇮🇳", "RU": "🇷🇺", "ZA": "🇿🇦",
        "AR": "🇦🇷", "NL": "🇳🇱", "SE": "🇸🇪", "NO": "🇳🇴", "DK": "🇩🇰",
        "FI": "🇫🇮", "BE": "🇧🇪", "CH": "🇨🇭", "AT": "🇦🇹", "PL": "🇵🇱",
        "PT": "🇵🇹", "GR": "🇬🇷", "TR": "🇹🇷", "EG": "🇪🇬", "SA": "🇸🇦",
        "AE": "🇦🇪", "SG": "🇸🇬", "MY": "🇲🇾", "TH": "🇹🇭", "ID": "🇮🇩",
        "PH": "🇵🇭", "VN": "🇻🇳", "NZ": "🇳🇿", "KR": "🇰🇷", "IL": "🇮🇱"
    };
    return `${countryEmojis[params.value] || ''} ${params.value || ''}`;
}
""")

# Define JsCode for device formatting
deviceFormatter = JsCode("""
function(params) {
    const deviceEmojis = {
        "Desktop": "🖥️", "Mobile": "📱"
    };
    return `${deviceEmojis[params.value] || ''} ${params.value || ''}`;
}
""")

def aggrid_configuration(df):
    grid_builder = GridOptionsBuilder.from_dataframe(df)

    # UI configuration
    grid_builder.configure_side_bar()

    # Use pagination and row virtualisation for better performance
    grid_builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    # grid_builder.configure_grid_options(enableRowVirtualization=True, enableRangeSelection=False)

    # All columns
    grid_builder.configure_default_column(filter=True, groupable=True, value=True, enableRowGroup=True)

    # Specific columns
    grid_builder.configure_column('Date', aggFunc=None,)

    numeric_types = ['numericColumn', 'numberColumnFilter', 'customNumericFormat']
    grid_builder.configure_column('Impressions',
                                  type=numeric_types,
                                  valueFormatter="new Intl.NumberFormat('en-US', {minimumFractionDigits: 0, maximumFractionDigits: 0}).format(value)",
                                  aggFunc="sum",)

    grid_builder.configure_column('CTR',
                                  type=numeric_types,
                                  valueFormatter="(value * 100).toFixed(2) + '%'",
                                  aggFunc="avg",)

    grid_builder.configure_column('Clicks',
                                  type=numeric_types,
                                  valueFormatter="new Intl.NumberFormat('en-US', {minimumFractionDigits: 0, maximumFractionDigits: 0}).format(value)",
                                  aggFunc="sum",)

    grid_builder.configure_column('CPC', type=numeric_types,
                                  valueFormatter="new Intl.NumberFormat('en-US', {style: 'currency', currency: 'EUR'}).format(value)",
                                  aggFunc="avg",)

    grid_builder.configure_column('Cost',
                                  type=numeric_types,
                                  valueFormatter="new Intl.NumberFormat('en-US', {style: 'currency', currency: 'EUR', minimumFractionDigits: 0, maximumFractionDigits: 0}).format(value)",
                                  aggFunc="sum",)

    grid_builder.configure_column('ROI', type=numeric_types,
                                  valueFormatter="(value * 100).toFixed(1) + '%'",
                                  aggFunc="avg",
                                  )

    grid_builder.configure_column('Revenue',
                                  type=numeric_types,
                                  valueFormatter="new Intl.NumberFormat('en-US', {style: 'currency', currency: 'EUR', minimumFractionDigits: 0, maximumFractionDigits: 0}).format(value)",
                                  aggFunc="sum",
                                  )

    grid_builder.configure_column('clickshare', header_name='Click Share', type=numeric_types,
                                  valueFormatter="(value * 100).toFixed(2) + '%'",
                                  aggFunc="avg",)

    text_types = ['textColumn', 'stringColumnFilter']
    grid_builder.configure_column('Market', type=text_types, valueFormatter=countryFormatter, aggFunc=None,)
    grid_builder.configure_column('Device', type=text_types, valueFormatter=deviceFormatter, aggFunc=None,)

    # Build grid options
    gridOptions = grid_builder.build()

    # Reorder columns by setting the 'columnDefs' after building the grid options
    column_order = ["Date", "Device", "Market", "Impressions", "Clicks", "Cost", "Revenue", "ROI", "CPC", "CTR", "clickshare"]
    gridOptions['columnDefs'] = sorted(gridOptions['columnDefs'], key=lambda col: column_order.index(col['field']) if col['field'] in column_order else len(column_order))

    grid_response = AgGrid(df,
                           gridOptions=gridOptions,
                           allow_unsafe_jscode=True,
                           height=min(500, (len(df)) * 60),  # 38px per row or 500px
                           fit_columns_on_grid_load=True,
                           theme='balham',
                           )

    # https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html
    return grid_response

def faster_aggrid_configuration(df):
    grid_builder = GridOptionsBuilder.from_dataframe(df)

    grid_builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)
    grid_builder.configure_grid_options(rowBuffer=0, enableRangeSelection=False)

    # Build grid options
    gridOptions = grid_builder.build()

    grid_response = AgGrid(df,
                           gridOptions=gridOptions,
                           allow_unsafe_jscode=True,
                           height=500,  # 38px per row or 500px
                           fit_columns_on_grid_load=False,
                           theme='balham',
                           )

    # https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html
    return grid_response
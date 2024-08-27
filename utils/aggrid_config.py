from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import polars as pl
import streamlit as st

# Define JsCode for country formatting
countryFormatter = JsCode("""
function(params) {
    if (params.value == null || params.value === undefined) {
        return '';
    }
    var countryEmojis = {
        "UK": "🇬🇧",
        "US": "🇺🇸",
        "ES": "🇪🇸",
        "JP": "🇯🇵",
        "AU": "🇦🇺",
        "BR": "🇧🇷",
        "MX": "🇲🇽",
        "DE": "🇩🇪",
        "FR": "🇫🇷",
        "IT": "🇮🇹",
        "CA": "🇨🇦",
        "CN": "🇨🇳",
        "IN": "🇮🇳",
        "RU": "🇷🇺",
        "ZA": "🇿🇦",
        "AR": "🇦🇷",
        "NL": "🇳🇱",
        "SE": "🇸🇪",
        "NO": "🇳🇴",
        "DK": "🇩🇰",
        "FI": "🇫🇮",
        "BE": "🇧🇪",
        "CH": "🇨🇭",
        "AT": "🇦🇹",
        "PL": "🇵🇱",
        "PT": "🇵🇹",
        "GR": "🇬🇷",
        "TR": "🇹🇷",
        "EG": "🇪🇬",
        "SA": "🇸🇦",
        "AE": "🇦🇪",
        "SG": "🇸🇬",
        "MY": "🇲🇾",
        "TH": "🇹🇭",
        "ID": "🇮🇩",
        "PH": "🇵🇭",
        "VN": "🇻🇳",
        "NZ": "🇳🇿",
        "KR": "🇰🇷",
        "IL": "🇮🇱"
    };
    var countryCode = params.value;
    var emoji = countryEmojis[countryCode] || '';
    return emoji + ' ' + countryCode;
}
""")

# Define JsCode for device formatting
deviceFormatter = JsCode("""
function(params) {
    if (params.value == null || params.value === undefined) {
        return '';
    }
    var deviceEmojis = {
        "Desktop": "🖥️",
        "Mobile": "📱",
        };
    var deviceType = params.value;
    var emoji = deviceEmojis[deviceType] || '';
    return emoji + ' ' + deviceType;
}
""")

# Define JsCode for percentage formatting
percentage_formatter = JsCode("""
function(params) {
    if (params.value == null) {
        return '';
    }
    var decimalPoints = params.column.colDef.cellRendererParams.decimalPoints || 2;
    return (params.value * 100).toFixed(decimalPoints) + '%';
}
""")

percentage_getter = JsCode("""
function(params) {
    return params.data[params.colDef.field];
}
""")

# Define JsCode for currency formatting
currency_formatter = JsCode("""
function(params) {
    if (params.value == null || params.value === undefined) {
        return '';
    }
    var decimalPoints = params.column.colDef.cellRendererParams.decimalPoints || 0;
    var currencySymbol = params.column.colDef.cellRendererParams.currencySymbol || '€';
    var value = params.value;

    // Format the number with thousand separators and decimal points
    var formattedNumber = value.toLocaleString('en-US', {
        minimumFractionDigits: decimalPoints,
        maximumFractionDigits: decimalPoints
    });

    return currencySymbol + formattedNumber;
}
""")

currency_getter = JsCode("""
function(params) {
    return params.data[params.colDef.field];
}
""")

# Define JsCode for currency formatting
thousands_formatter = JsCode("""
function(params) {
    if (params.value == null || params.value === undefined) {
        return '';
    }
    var decimalPoints = params.column.colDef.cellRendererParams.decimalPoints || 0;
    var value = params.value;

    // Format the number with thousand separators and decimal points
    var formattedNumber = value.toLocaleString('en-US', {
        minimumFractionDigits: decimalPoints,
        maximumFractionDigits: decimalPoints
    });

    return formattedNumber;
}
""")

thousands_getter = JsCode("""
function(params) {
    return params.data[params.colDef.field];
}
""")

def aggrid_configuration(df):
    grid_builder = GridOptionsBuilder.from_dataframe(df)

    # UI configuration
    grid_builder.configure_side_bar()
    grid_builder.configure_pagination(paginationAutoPageSize=False, paginationPageSize=20)

    # All columns
    grid_builder.configure_default_column(filter=True, groupable=True, value=True, enableRowGroup=True)

    # Specific columns
    grid_builder.configure_column('Date', aggFunc=None,)

    numeric_types = ['numericColumn', 'numberColumnFilter', 'customNumericFormat']
    grid_builder.configure_column('Impressions',
                                  type=numeric_types,
                                  valueGetter=thousands_getter,
                                  valueFormatter=thousands_formatter,
                                  cellRendererParams={'decimalPoints': 0},
                                  aggFunc="sum",)

    grid_builder.configure_column('CTR',
                                  type=numeric_types,
                                  valueGetter=percentage_getter,
                                  valueFormatter=percentage_formatter,
                                  cellRendererParams={'decimalPoints': 2},
                                  aggFunc="avg",)

    grid_builder.configure_column('Clicks',
                                  type=numeric_types,
                                  valueGetter=thousands_getter,
                                  valueFormatter=thousands_formatter,
                                  cellRendererParams={'decimalPoints': 0},
                                  aggFunc="sum",)

    grid_builder.configure_column('CPC', type=numeric_types,
                                  valueGetter=currency_getter,
                                  valueFormatter=currency_formatter,
                                  cellRendererParams={'decimalPoints': 3, 'currencySymbol': '€', },
                                  aggFunc="avg",)

    grid_builder.configure_column('Cost',
                                  type=numeric_types,
                                  valueGetter=currency_getter,
                                  valueFormatter=currency_formatter,
                                  cellRendererParams={'decimalPoints': 0, 'currencySymbol': '€',},
                                  aggFunc="sum",)

    grid_builder.configure_column('ROI', type=numeric_types,
                                  valueGetter=percentage_getter,
                                  valueFormatter=percentage_formatter,
                                  cellRendererParams={'decimalPoints': 1},
                                  aggFunc="avg",
                                  )

    grid_builder.configure_column('Revenue',
                                  type=numeric_types,
                                  valueGetter=currency_getter,
                                  valueFormatter=currency_formatter,
                                  cellRendererParams={'decimalPoints': 0, 'currencySymbol': '€',},
                                  aggFunc="sum",
                                  )

    grid_builder.configure_column('clickshare', header_name='Click Share', type=numeric_types,
                                  valueGetter=percentage_getter,
                                  valueFormatter=percentage_formatter,
                                  cellRendererParams={'decimalPoints': 2},
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

    filtered_df = pl.DataFrame(grid_response['data'])

    # https://streamlit-aggrid.readthedocs.io/en/docs/AgGrid.html
    return grid_response, filtered_df
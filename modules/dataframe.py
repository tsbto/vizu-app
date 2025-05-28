from dash import html, dash_table, Input, Output
import pandas as pd

def layout():
    return html.Div([
        html.H2("Data Frame"),
        html.Div(id="dataframe-table"),
    ])

def register_callbacks(app):
    @app.callback(
        Output("dataframe-table", "children"),
        Input("stored-data", "data"),
        prevent_initial_call=False,
    )
    def render_dataframe_table(stored_data):
        if stored_data is None:
            return html.P("Nenhum dado carregado ainda.", style={"color": "red"})
        df = pd.read_json(stored_data, orient='split')
        return dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
            style_header={"backgroundColor": "#1a1a1a", "color": "white", "fontWeight": "bold"},
        )

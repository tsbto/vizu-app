from dash import html, dash_table, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

def layout():
    return html.Div([
        html.H2("Data Frame", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.P("Aqui está a visualização da tabela carregada:"),
        html.Div(id="dataframe-table"),
        html.Br(),
        dbc.Button("Recarregar Tabela", id="btn-reload-table", color="primary", n_clicks=0),
    ])

def register_callbacks(app):
    @app.callback(
        Output("dataframe-table", "children"),
        [
            Input("stored-data", "data"),
            Input("btn-reload-table", "n_clicks"),
        ],
        prevent_initial_call=True,
    )
    def render_dataframe_table(stored_data, n_clicks):
        if stored_data is None:
            return html.P("Nenhum dado carregado ainda.", style={"color": "red"})
        
        df = pd.read_json(stored_data, orient='split')
        table = dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "color": "black", "backgroundColor": "white"},
            style_header={"backgroundColor": "#1a1a1a", "color": "white", "fontWeight": "bold"},
        )
        return table

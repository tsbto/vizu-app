from dash import html, dash_table, Input, Output, State, dcc
import dash_bootstrap_components as dbc
import pandas as pd

def layout():
    return html.Div([
        html.H2("DataFrame", style={"fontFamily": "Arial", "fontWeight": "bold"}),
        html.P("Aqui está a visualização da tabela carregada:", style={"fontFamily": "Courier New"}),

        html.Div(id="dataframe-table"),
        html.Br(),

        dbc.Button("Recarregar Tabela", id="btn-reload-table", color="primary", n_clicks=0),
        dcc.Store(id="stored-data"),
    ])

def register_callbacks(app):
    @app.callback(
        Output("stored-data", "data"),
        Input("btn-reload-table", "n_clicks"),
        prevent_initial_call=True
    )
    def load_data(n_clicks):
        # Dummy dataframe só para exemplo
        dummy_df = pd.DataFrame({
            "Coluna A": [1, 2, 3],
            "Coluna B": ["A", "B", "C"],
        })
        return dummy_df.to_json(date_format='iso', orient='split')

    @app.callback(
        Output("dataframe-table", "children"),
        Input("stored-data", "data"),
        prevent_initial_call=True
    )
    def render_table(stored_data):
        if stored_data is None:
            return html.P("Nenhum dado carregado ainda.", style={"color": "red", "fontFamily": "Courier New"})

        df = pd.read_json(stored_data, orient='split')
        return dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={
                "textAlign": "left",
                "color": "white",
                "backgroundColor": "#1e1e1e",
                "fontFamily": "Courier New"
            },
            style_header={
                "backgroundColor": "#1a1a1a",
                "color": "white",
                "fontWeight": "bold",
                "fontFamily": "Arial"
            },
        )

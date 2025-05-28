from dash import html, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import json

def layout():
    return html.Div([
        html.H2("Data Frame", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.P("Aqui está a visualização da tabela carregada:"),

        html.Div(id="dataframe-table"),
        html.Br(),

        dbc.Button("Recarregar Tabela", id="btn-reload-table", color="primary", n_clicks=0),

        # Componente oculto para armazenar dados carregados
        dcc.Store(id="stored-data")
    ])


def register_callbacks(app):
    @app.callback(
        Output("stored-data", "data"),
        [
            Input("btn-load-bq", "n_clicks"),
            Input("btn-load-csv", "n_clicks"),
        ],
        [
            State("bq-project", "value"),
            State("bq-dataset", "value"),
            State("bq-table", "value"),
            State("bq-json", "contents"),
            State("upload-csv", "contents"),
            State("upload-csv", "filename"),
        ],
        prevent_initial_call=True,
    )
    def load_data(bq_clicks, csv_clicks, project, dataset, table, bq_json, csv_contents, csv_filename):
        # Exemplo simplificado: aqui você pode implementar lógica para carregar dados
        # Por enquanto, só retorna um JSON dummy para testar
        dummy_df = pd.DataFrame({
            "Coluna A": [1, 2, 3],
            "Coluna B": ["A", "B", "C"],
        })
        return dummy_df.to_json(date_format='iso', orient='split')


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

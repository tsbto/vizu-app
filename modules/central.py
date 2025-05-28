from dash import html, dcc, Input, Output, State, ctx, no_update
import dash_bootstrap_components as dbc
import base64
import io
import pandas as pd

def layout():
    return html.Div([
        html.H2("Carregar dados"),
        dbc.Input(id="bq-project", placeholder="Projeto BigQuery", type="text", style={"marginTop": 5}),
        dbc.Input(id="bq-dataset", placeholder="Dataset BigQuery", type="text", style={"marginTop": 5}),
        dbc.Input(id="bq-table", placeholder="Tabela BigQuery", type="text", style={"marginTop": 5}),
        dcc.Upload(
            id="bq-json",
            children=html.Div(['Arraste/Selecione a chave JSON do serviço BigQuery aqui']),
            style={'border': '1px dashed #ccc', 'padding': '10px', 'marginTop': 10},
            multiple=False,
        ),
        dbc.Button("Carregar do BigQuery", id="btn-load-bq", color="primary", style={"marginTop": 10}),
        html.Hr(),
        dcc.Upload(
            id="upload-csv",
            children=html.Div(['Arraste/Selecione um arquivo CSV aqui']),
            style={'border': '1px dashed #ccc', 'padding': '10px'},
            multiple=False,
        ),
        dbc.Button("Carregar CSV", id="btn-load-csv", color="secondary", style={"marginTop": 10}),
        html.Br(),
        html.Div(id="output-msg", style={"marginTop": 15}),
        # Armazena dados carregados em JSON (orient='split')
        dcc.Store(id="stored-data"),
    ])

def carregar_tabela_bigquery(project, dataset, table, chave_json_bytes):
    # Aqui entra sua função real para carregar BigQuery com as credenciais
    # Exemplo fictício:
    import pandas_gbq
    import json
    from google.oauth2 import service_account

    credentials = service_account.Credentials.from_service_account_info(json.loads(chave_json_bytes.decode("utf-8")))
    query = f"SELECT * FROM `{project}.{dataset}.{table}` LIMIT 1000"
    df = pandas_gbq.read_gbq(query, project_id=project, credentials=credentials)
    return df

def register_callbacks(app):
    @app.callback(
        [Output("output-msg", "children"), Output("stored-data", "data")],
        [Input("btn-load-bq", "n_clicks"), Input("btn-load-csv", "n_clicks")],
        [State("bq-project", "value"),
         State("bq-dataset", "value"),
         State("bq-table", "value"),
         State("bq-json", "contents"),
         State("upload-csv", "contents"),
         State("upload-csv", "filename")],
        prevent_initial_call=True,
    )
    def handle_load_data(n_clicks_bq, n_clicks_csv, project, dataset, table, json_contents, csv_contents, csv_filename):
        trigger_id = ctx.triggered_id

        if trigger_id == "btn-load-bq":
            if not all([project, dataset, table, json_contents]):
                return dbc.Alert("Preencha todos os campos e envie o JSON!", color="danger"), no_update
            try:
                content_string = json_contents.split(",")[1]
                chave_json_bytes = base64.b64decode(content_string)

                df = carregar_tabela_bigquery(project, dataset, table, chave_json_bytes)

                json_data = df.to_json(date_format='iso', orient='split')
                return dbc.Alert("Tabela carregada do BigQuery com sucesso!", color="success"), json_data
            except Exception as e:
                return dbc.Alert(f"Erro ao carregar BigQuery: {e}", color="danger"), no_update

        elif trigger_id == "btn-load-csv":
            if csv_contents is None:
                return dbc.Alert("Nenhum arquivo CSV enviado!", color="warning"), no_update
            try:
                content_string = csv_contents.split(",")[1]
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

                json_data = df.to_json(date_format='iso', orient='split')
                return dbc.Alert("CSV carregado com sucesso!", color="success"), json_data
            except Exception as e:
                return dbc.Alert(f"Erro ao processar CSV: {e}", color="danger"), no_update

        return no_update, no_update

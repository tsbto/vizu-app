from dash import html, dcc, Input, Output, State, callback_context as ctx
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
from google.cloud import bigquery
import tempfile

def layout():
    return html.Div([
        html.H2("🔌 Central de Conexões"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Google BigQuery"),
                        dbc.Label("Project ID"),
                        dbc.Input(id="bq-project", placeholder="Project ID"),
                        dbc.Label("Dataset ID"),
                        dbc.Input(id="bq-dataset", placeholder="Dataset ID"),
                        dbc.Label("Table ID"),
                        dbc.Input(id="bq-table", placeholder="Table ID"),
                        dbc.Label("Chave JSON"),
                        dcc.Upload(
                            id="bq-json",
                            children=html.Div(["Arraste ou clique para enviar JSON"]),
                            style={"border": "1px dashed gray", "padding": "10px", "border-radius": "10px", "text-align": "center", "margin-bottom": "10px"}
                        ),
                        dbc.Button("🚀 Carregar BigQuery", id="btn-load-bq", color="primary", className="mt-2"),
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Upload de CSV"),
                        dcc.Upload(
                            id="upload-csv",
                            children=html.Div(["Arraste ou clique para enviar CSV"]),
                            style={"border": "1px dashed gray", "padding": "10px", "border-radius": "10px", "text-align": "center"}
                        ),
                        dbc.Button("📁 Carregar CSV", id="btn-load-csv", color="success", className="mt-2"),
                    ])
                ])
            ], width=6)
        ]),
        html.Hr(),
        html.Div(id="output-msg"),
        dcc.Store(id="stored-data")
    ])

def carregar_tabela_bigquery(project_id, dataset_id, table_id, chave_json_bytes):
    with tempfile.NamedTemporaryFile(delete=False) as temp_cred_file:
        temp_cred_file.write(chave_json_bytes)
        temp_cred_file.flush()
        client = bigquery.Client.from_service_account_json(temp_cred_file.name, project=project_id)
        tabela_full_id = f"{project_id}.{dataset_id}.{table_id}"
        query = f"SELECT * FROM `{tabela_full_id}` LIMIT 1000"
        query_job = client.query(query)
        df = query_job.result().to_dataframe()
    return df

def register_callbacks(app):
    @app.callback(
        [Output("output-msg", "children"), Output("stored-data", "data")],
        [Input("btn-load-bq", "n_clicks"), Input("btn-load-csv", "n_clicks")],
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
    def load_data(bq_clicks, csv_clicks, project, dataset, table, json_contents, csv_contents, csv_filename):
        trigger = ctx.triggered_id

        if trigger == "btn-load-bq":
            if not all([project, dataset, table, json_contents]):
                return dbc.Alert("Preencha todos os campos e envie o JSON!", color="danger"), None
            try:
                content_string = json_contents.split(",")[1]
                chave_json_bytes = base64.b64decode(content_string)
                df = carregar_tabela_bigquery(project, dataset, table, chave_json_bytes)
                return dbc.Alert("Tabela carregada com sucesso!", color="success"), df.to_json(date_format='iso', orient='split')
            except Exception as e:
                return dbc.Alert(f"Erro ao carregar BigQuery: {e}", color="danger"), None

        elif trigger == "btn-load-csv":
            if csv_contents is None:
                return dbc.Alert("Nenhum arquivo CSV enviado!", color="warning"), None
            try:
                content_string = csv_contents.split(",")[1]
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
                return dbc.Alert("CSV carregado com sucesso!", color="success"), df.to_json(date_format='iso', orient='split')
            except Exception as e:
                return dbc.Alert(f"Erro ao processar CSV: {e}", color="danger"), None

        return dbc.Alert("Nenhuma ação realizada.", color="secondary"), None

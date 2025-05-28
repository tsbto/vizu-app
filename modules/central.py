# modules/central_conexoes_dash.py
import dash
from dash import html, dcc, Output, Input, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd
from google.cloud import bigquery
import tempfile
from modules.db import get_engine
from data import data_loader

# Função para carregar dados do BigQuery
def carregar_tabela_bigquery(project_id, dataset_id, table_id, chave_json_file):
    with tempfile.NamedTemporaryFile(delete=False) as temp_cred_file:
        temp_cred_file.write(chave_json_file)
        temp_cred_file.flush()

        client = bigquery.Client.from_service_account_json(temp_cred_file.name, project=project_id)
        tabela_full_id = f"{project_id}.{dataset_id}.{table_id}"
        query = f"SELECT * FROM `{tabela_full_id}` LIMIT 1000"

        query_job = client.query(query)
        df = query_job.result().to_dataframe()

    return df

# Função para salvar DataFrame no Postgres
def salvar_dataframe(df: pd.DataFrame, nome_tabela: str):
    engine = get_engine()
    df.to_sql(nome_tabela, engine, index=False, if_exists='replace')

# Layout do módulo
def layout():
    return html.Div([
        html.H2("🔌 Central de Conexões", className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Google BigQuery", className="card-title"),
                        html.P("Conecte diretamente ao seu projeto no BigQuery e carregue dados."),
                        dbc.Accordion([
                            dbc.AccordionItem([
                                dbc.Form([
                                    dbc.Label("Project ID"),
                                    dbc.Input(id="bq-project", placeholder="Project ID"),

                                    dbc.Label("Dataset ID", className="mt-2"),
                                    dbc.Input(id="bq-dataset", placeholder="Dataset ID"),

                                    dbc.Label("Table ID", className="mt-2"),
                                    dbc.Input(id="bq-table", placeholder="Table ID"),

                                    dbc.Label("Chave JSON", className="mt-2"),
                                    dcc.Upload(
                                        id="bq-json",
                                        children=html.Div(["Arraste ou clique para enviar JSON"]),
                                        style={
                                            "border": "1px dashed gray",
                                            "padding": "10px",
                                            "border-radius": "10px",
                                            "text-align": "center",
                                            "margin-bottom": "10px"
                                        }
                                    ),
                                    dbc.Button("🚀 Carregar BigQuery", color="primary", id="btn-load-bq", className="mt-2", style={"border-radius": "999px"}),
                                ])
                            ], title="🔑 Conectar BigQuery")
                        ])
                    ])
                ])
            ], width=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Upload de CSV", className="card-title"),
                        html.P("Faça upload de um arquivo CSV e comece sua análise."),
                        dcc.Upload(
                            id="upload-csv",
                            children=html.Div(["Arraste ou clique para enviar CSV"]),
                            style={
                                "border": "1px dashed gray",
                                "padding": "10px",
                                "border-radius": "10px",
                                "text-align": "center"
                            }
                        ),
                        dbc.Button("📁 Carregar CSV", color="success", id="btn-load-csv", className="mt-2", style={"border-radius": "999px"}),
                    ])
                ])
            ], width=6)
        ]),
        html.Hr(),
        html.Div(id="output-msg", className="mt-3")
    ])

# Callbacks para o módulo
def register_callbacks(app: dash.Dash):
    @app.callback(
        [Output("output-msg", "children"),
         Output("stored-data", "data")],
        [
            Input("btn-load-bq", "n_clicks"),
            Input("btn-load-csv", "n_clicks")
        ],
        [
            State("bq-project", "value"),
            State("bq-dataset", "value"),
            State("bq-table", "value"),
            State("bq-json", "contents"),
            State("upload-csv", "contents"),
            State("upload-csv", "filename")
        ],
        prevent_initial_call=True
    )
    def load_data(bq_clicks, csv_clicks,
               project_id, dataset_id, table_id, json_contents,
               csv_contents, csv_filename):
    trigger = ctx.triggered_id
    if trigger == "btn-load-bq":
        # ...mesma lógica
        df = carregar_tabela_bigquery(...)
        salvar_dataframe(df, f"{project_id}_{dataset_id}_{table_id}")
        return dbc.Alert("Tabela carregada e salva com sucesso!", color="success"), df.to_json(date_format='iso', orient='split')
    elif trigger == "btn-load-csv":
        if csv_contents is None:
            return dbc.Alert("Nenhum arquivo CSV enviado!", color="warning"), no_update
        try:
            import io, base64
            content_string = csv_contents.split(",")[1]
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
            if "data" in df.columns:
                df["data"] = pd.to_datetime(df["data"])
            salvar_dataframe(df, csv_filename.replace(".csv", ""))
            return dbc.Alert("CSV carregado e salvo com sucesso!", color="success"), df.to_json(date_format='iso', orient='split')
        except Exception as e:
            return dbc.Alert(f"Erro ao processar CSV: {e}", color="danger"), no_update
    return dbc.Alert("Nenhuma ação realizada.", color="secondary"), no_update

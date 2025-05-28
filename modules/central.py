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
        Output("output-msg", "children"),
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
    def handle_uploads(n_clicks_bq, n_clicks_csv, project, dataset, table, json_contents, csv_contents, csv_filename):
        ctx = dash.callback_context

        if not ctx.triggered:
            return "Nenhum botão clicado."
        else:
            triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

            if triggered_id == "btn-load-bq":
                # Lógica de carregar BigQuery
                return "BigQuery carregado!"
            elif triggered_id == "btn-load-csv":
                # Lógica de carregar CSV
                return "CSV carregado!"
            else:
                return "Ação desconhecida."



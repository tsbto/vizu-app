from dash import html, dcc, Input, Output, State, callback_context as ctx
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
import json
from google.cloud import bigquery
from google.oauth2 import service_account


def layout():
    return html.Div([
        html.H3("📁 Upload e Integração de Dados", style={"marginBottom": "20px"}),

        # Cards principais (Upload, BigQuery, Snowflake)
        html.Div([
            html.Div([
                html.H5("Upload CSV"),
                html.P("Envie seus dados em CSV para integração."),
                dcc.Upload(
                    id="upload-data",
                    children=html.Button("Selecionar arquivo CSV", className="pill-btn"),
                    multiple=False,
                    style={"marginTop": "10px"}
                ),
            ], className="minimal-card"),

            html.Div([
                html.H5("BigQuery"),
                html.P("Conecte-se ao BigQuery para buscar dados."),
                html.Button("Conectar BigQuery", id="connect-bq-btn", n_clicks=0, className="pill-btn"),
            ], className="minimal-card"),

            html.Div([
                html.H5("Snowflake"),
                html.P("Conecte-se ao Snowflake para buscar dados."),
                html.Button("Conectar Snowflake", id="connect-sf-btn", n_clicks=0, className="pill-btn"),
            ], className="minimal-card"),
        ], style={"display": "flex", "gap": "20px", "marginBottom": "20px"}),

        # Formulário BigQuery está no layout desde o início, mas escondido
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H5("🔗 Conexão BigQuery", className="card-title"),
                    dbc.Input(id="bq-project-id", placeholder="Project ID", type="text", style={"marginBottom": "10px"}),
                    dbc.Input(id="bq-dataset", placeholder="Dataset", type="text", style={"marginBottom": "10px"}),
                    dbc.Input(id="bq-table", placeholder="Tabela", type="text", style={"marginBottom": "10px"}),
                    dbc.Textarea(id="bq-json-key", placeholder="Chave JSON", style={"marginBottom": "10px"}),
                    html.Button("Conectar", id="bq-connect-final-btn", n_clicks=0, className="pill-btn"),
                    html.Div(id="bq-connection-feedback", style={"marginTop": "10px"})
                ])
            ], style={"marginTop": "20px", "backgroundColor": "#222", "color": "white"}),
        ], id="bq-connection-form", style={"display": "none"}),  # Escondido inicialmente

        # Card para preview e resumo estatístico
        html.Div([
            html.H4("📊 Tabela de Dados", style={"marginBottom": "10px"}),
            dag.AgGrid(
                id="ag-grid-preview",
                columnSize="sizeToFit",
                defaultColDef={"editable": True, "resizable": True},
                style={"height": "300px", "width": "100%", "color": "black"},
            ),
            html.H4("📈 Resumo Estatístico", style={"marginTop": "20px"}),
            html.Pre(id="resumo-estatistico", style={"whiteSpace": "pre-wrap", "color": "white"}),
        ], className="big-card"),
    ], style={"padding": "20px", "color": "white"})


def register_callbacks(app, pg_engine):
    # Mostrar/Esconder formulário BigQuery ao clicar no botão
    @app.callback(
        Output("bq-connection-form", "style"),
        Input("connect-bq-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_bigquery_form(n_clicks):
        if n_clicks and n_clicks > 0:
            return {"display": "block"}  # Mostrar formulário
        return {"display": "none"}  # Esconder formulário


    # Callback unificado para Upload CSV, BigQuery e Snowflake
    @app.callback(
        Output("ag-grid-preview", "rowData"),
        Output("ag-grid-preview", "columnDefs"),
        Output("resumo-estatistico", "children"),
        Output("bq-connection-feedback", "children"),
        Output("stored-data", "data"),
        Input("upload-data", "contents"),
        Input("bq-connect-final-btn", "n_clicks"),
        Input("connect-sf-btn", "n_clicks"),
        State("upload-data", "filename"),
        State("bq-project-id", "value"),
        State("bq-dataset", "value"),
        State("bq-table", "value"),
        State("bq-json-key", "value"),
        prevent_initial_call=True,
        allow_missing=True
    )
    def unified_data_handler(upload_contents, bq_n_clicks, sf_n_clicks, filename,
                             bq_project, bq_dataset, bq_table, bq_json_key):
        triggered_id = ctx.triggered_id

        # Inicializa outputs padrões
        row_data = []
        column_defs = []
        resumo = "Nenhum dado carregado ainda."
        feedback = ""
        json_data = None
        
        if triggered_id == "upload-data" and upload_contents:
            try:
                content_type, content_string = upload_contents.split(',')
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                row_data = df.to_dict("records")
                column_defs = [{"headerName": col, "field": col} for col in df.columns]
                resumo = df.describe().to_string()
                feedback = "Arquivo CSV carregado com sucesso!"
                json_data = df.to_json(date_format="iso", orient="split")
            except Exception as e:
                resumo = f"Erro ao processar CSV: {str(e)}"
                feedback = ""

        elif triggered_id == "bq-connect-final-btn" and bq_n_clicks and bq_n_clicks > 0:
            try:
                if not bq_json_key:
                    raise ValueError("Chave JSON do BigQuery não pode estar vazia.")
                credentials_info = json.loads(bq_json_key)
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                client = bigquery.Client(credentials=credentials, project=bq_project)
                query = f"SELECT * FROM `{bq_project}.{bq_dataset}.{bq_table}` LIMIT 1000"
                df = client.query(query).to_dataframe()
                row_data = df.to_dict("records")
                column_defs = [{"headerName": col, "field": col} for col in df.columns]
                resumo = df.describe(include="all").to_string()
                feedback = dbc.Alert("Conectado ao BigQuery com sucesso!", color="success")
                json_data = df.to_json(date_format="iso", orient="split")
            except Exception as e:
                resumo = f"Erro ao conectar ao BigQuery: {str(e)}"
                feedback = dbc.Alert(f"Erro: {str(e)}", color="danger")

        elif triggered_id == "connect-sf-btn" and sf_n_clicks and sf_n_clicks > 0:
            resumo = "Conexão ao Snowflake: Em construção!"
            feedback = ""

        return row_data, column_defs, resumo, feedback, json_data

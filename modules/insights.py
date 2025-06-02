import pandas as pd
from dash import html, dcc, Input, Output, State
import dash
import plotly.express as px
from modules import resumo_ia
from google.cloud import bigquery
from google.oauth2 import service_account
import random

loading_messages = [
    "🔍 Minerando insights preciosos...",
    "🚀 Preparando gráficos incríveis...",
    "🤖 A IA está trabalhando duro...",
    "⏳ Carregando dados mágicos...",
    "💡 Buscando padrões ocultos..."
]

def layout():
    return html.Div([
        html.H3("📊 Insights Automáticos com IA"),
        html.P("Os insights são gerados automaticamente ao visitar esta página.", style={"color": "#bbb"}),
        html.Div(id="loading-container", children=[
            dcc.Loading(
                id="loading-insights",
                type="circle",
                color="#FFB6C1",
                children=[
                    html.Div(id="llm-summary-container", style={"marginTop": "20px", "color": "white"}),
                    html.Hr(),
                    html.Div(id="graphs-container")
                ]
            )
        ])
    ], style={"padding": "20px", "color": "white"})

def register_callbacks(app):
    @app.callback(
        [Output("graphs-container", "children"),
         Output("llm-summary-container", "children")],
        Input("url", "pathname"),
        State("stored-data", "data"),  # Usa o dcc.Store
        prevent_initial_call=True
    )
    def generate_insights(pathname, stored_data):
        loading_msg = random.choice(loading_messages)
        if pathname == "/insights" and stored_data:
            try:
                project_id = stored_data["project_id"]
                dataset_id = stored_data["dataset_id"]
                table_id = stored_data["table_id"]
                credentials_info = stored_data["json_key"]

                import json
                credentials_dict = json.loads(credentials_info)
                credentials = service_account.Credentials.from_service_account_info(credentials_dict)
                client = bigquery.Client(credentials=credentials, project=project_id)

                query = f"SELECT * FROM `{project_id}.{dataset_id}.{table_id}`"
                df = client.query(query).to_dataframe()
            except Exception as e:
                error_msg = f"Erro ao carregar dados: {str(e)}"
                return html.Div(error_msg, style={"color": "red"}), html.Div(error_msg, style={"color": "red"})

            if df.empty:
                no_data_msg = "Nenhum dado disponível. Por favor, carregue dados para gerar insights."
                return html.Div(no_data_msg, style={"color": "orange"}), html.Div(no_data_msg, style={"color": "orange"})

            graphs = []
            cat_cols = df.select_dtypes(include=["object", "category"]).columns
            for col in cat_cols:
                if df[col].nunique() < 20:
                    fig = px.histogram(df, x=col, title=f"Distribuição de {col}")
                    graphs.append(dcc.Graph(figure=fig))

            num_cols = df.select_dtypes(include=["number"]).columns
            for col in num_cols:
                fig = px.histogram(df, x=col, nbins=30, title=f"Histograma de {col}")
                graphs.append(dcc.Graph(figure=fig))

            resumo_estatistico = df.describe(include="all").to_string()
            llm_summary = resumo_ia.gerar_resumo_ia(resumo_estatistico, model_provider="together")

            return graphs, html.Div([
                html.H5("🤖 Resumo Gerado por IA"),
                html.P(llm_summary)
            ])
        else:
            return [], ""

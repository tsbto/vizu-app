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
        ]),
        dcc.Store(id="llm-summary-store", storage_type="session")  # novo store para guardar o resumo IA
    ], style={"padding": "20px", "color": "white"})

def register_callbacks(app):
    @app.callback(
        [
            Output("graphs-container", "children"),
            Output("llm-summary-container", "children"),
            Output("llm-summary-store", "data")  # novo output para salvar o resumo IA
        ],
        Input("url", "pathname"),
        Input("stored-data", "data"),
    )
    def generate_insights(pathname, stored_data):
        if pathname != "/insights":
            # Se não estiver na página insights, limpa output
            return [], "", ""

        if not stored_data:
            no_data_msg = "Nenhum dado carregado para gerar insights. Por favor, faça upload ou conecte ao BigQuery."
            return html.Div(no_data_msg, style={"color": "orange"}), html.Div(no_data_msg, style={"color": "orange"}), ""

        try:
            import pandas as pd
            import json

            # Converte JSON salvo no dcc.Store em dataframe
            df = pd.read_json(stored_data, orient="split")

        except Exception as e:
            error_msg = f"Erro ao processar dados armazenados: {str(e)}"
            return html.Div(error_msg, style={"color": "red"}), html.Div(error_msg, style={"color": "red"}), ""

        if df.empty:
            no_data_msg = "O conjunto de dados está vazio."
            return html.Div(no_data_msg, style={"color": "orange"}), html.Div(no_data_msg, style={"color": "orange"}), ""

        # Cria gráficos
        graphs = []
        import plotly.express as px
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        for col in cat_cols:
            if df[col].nunique() < 20:
                fig = px.histogram(df, x=col, title=f"Distribuição de {col}")
                graphs.append(dcc.Graph(figure=fig))

        num_cols = df.select_dtypes(include=["number"]).columns
        for col in num_cols:
            fig = px.histogram(df, x=col, nbins=30, title=f"Histograma de {col}")
            graphs.append(dcc.Graph(figure=fig))

        # resumo estatístico bruto
        resumo_estatistico = df.describe(include="all").to_string()

        # usa sua função de resumo IA (presumo que retorna string)
        llm_summary = resumo_ia.gerar_resumo_ia(resumo_estatistico, model_provider="together")

        return (
            graphs,
            html.Div([
                html.H5("🤖 Resumo Gerado por IA"),
                html.P(llm_summary)
            ]),
            llm_summary  # salva no novo dcc.Store (session)
        )

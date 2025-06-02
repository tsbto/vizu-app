import pandas as pd
from dash import html, dcc, Input, Output, State
import dash
import plotly.express as px
from modules import resumo_ia

def layout():
    return html.Div([
        html.H3("📊 Insights Automáticos com IA"),
        html.P("Os insights são gerados automaticamente ao visitar esta página.", style={"color": "#bbb"}),
        html.Div(id="llm-summary-container", style={"marginTop": "20px", "color": "white"}),
        html.Hr(),
        html.Div(id="graphs-container")
    ], style={"padding": "20px", "color": "white"})


def register_callbacks(app, pg_engine):
    @app.callback(
        [Output("graphs-container", "children"),
         Output("llm-summary-container", "children")],
        Input("url", "pathname"),
    )
    def generate_insights(pathname):
        if pathname == "/insights":
            # 1) Ler os dados do Postgres
            try:
                df = pd.read_sql("SELECT * FROM dados_upload", con=pg_engine)
            except Exception as e:
                error_msg = f"Erro ao carregar dados: {str(e)}"
                return html.Div(error_msg, style={"color": "red"}), html.Div(error_msg, style={"color": "red"})

            # 2) Verificar se o DataFrame está vazio
            if df.empty:
                no_data_msg = "Nenhum dado disponível. Por favor, carregue um CSV para gerar insights."
                return html.Div(no_data_msg, style={"color": "orange"}), html.Div(no_data_msg, style={"color": "orange"})

            # 3) Gerar gráficos automáticos
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

            # 4) Resumo estatístico simples (pra IA usar como base)
            resumo_estatistico = df.describe(include="all").to_string()

            # 5) Gera resumo com LLM
            llm_provider = "together"  # ou "together"
            llm_summary = resumo_ia.gerar_resumo_ia(resumo_estatistico, model_provider=llm_provider)

            return graphs, html.Div([
                html.H5("🤖 Resumo Gerado por IA"),
                html.P(llm_summary)
            ])
        else:
            return [], ""  # Caso não esteja na página /insights, não renderiza nada

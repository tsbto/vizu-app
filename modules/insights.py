import pandas as pd
from dash import html, dcc, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from modules import resumo_ia

# Layout da página de insights
layout = html.Div([
    html.H3("💡 Página de Insights Automáticos", style={"marginBottom": "20px"}),

    html.Div([
        html.Label("Escolha o modelo de IA:", style={"marginRight": "10px"}),
        dcc.Dropdown(
            id="llm-provider-dropdown",
            options=[
                {"label": "Together AI", "value": "together"},
                {"label": "OpenAI", "value": "openai"}
            ],
            value="together",
            clearable=False,
            style={"width": "250px"}
        ),
    ], style={"marginBottom": "20px"}),

    dbc.Button("Gerar Insights", id="btn-generate-insights", color="primary", n_clicks=0),
    html.Div(id="llm-summary-container", style={"marginTop": "20px", "color": "white"}),

    html.Hr(),
    html.H5("Gráficos Automáticos"),
    dcc.Loading(id="loading-graphs", type="circle", children=html.Div(id="graphs-container")),
], style={"padding": "20px", "color": "white"})


def register_callbacks(app, pg_engine):
    @app.callback(
        [Output("graphs-container", "children"),
         Output("llm-summary-container", "children")],
        Input("btn-generate-insights", "n_clicks"),
        State("llm-provider-dropdown", "value"),
        prevent_initial_call=True
    )
    def generate_insights(n_clicks, llm_provider):
        # 1) Ler os dados do Postgres
        try:
            df = pd.read_sql("SELECT * FROM dados_upload", con=pg_engine)
        except Exception as e:
            return html.Div(f"Erro ao carregar dados: {str(e)}", style={"color": "red"}), ""

        # 2) Gerar gráficos automáticos
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

        # 3) Resumo estatístico simples (pra IA usar como base)
        resumo_estatistico = df.describe(include="all").to_string()

        # 4) Gera resumo com LLM (resumo_ia já gerencia qual LLM usar)
        llm_summary = resumo_ia.gerar_resumo_ia(resumo_estatistico, model_provider=llm_provider)

        return graphs, html.Div([
            html.H5("🤖 Resumo Gerado por IA"),
            html.P(llm_summary)
        ])

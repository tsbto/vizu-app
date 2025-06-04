import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, Input, Output, State, no_update
import plotly.express as px
from modules import resumo_ia
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
        dcc.Store(id="llm-summary-store", storage_type="session"),
        html.H3("📊 Insights Automáticos com IA", style={"fontFamily": "Arial, sans-serif", "fontSize": "34px", "fontWeight": "bold", "marginBottom": "20px"}),
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
        [
            Output("graphs-container", "children"),
            Output("llm-summary-container", "children"),
            Output("llm-summary-store", "data")
        ],
        [Input("url", "pathname"), Input("stored-data", "data")],
        State("llm-summary-store", "data"),
    )
    def generate_insights(pathname, stored_data, llm_summary_store):
        if pathname != "/insights":
            return [], "", no_update

        if not stored_data:
            return [], "", None  # Limpa o store se não há dado

        # Se já existe insight para esse dado, só exibe
        if (
            llm_summary_store
            and llm_summary_store.get("llm_summary")
            and llm_summary_store.get("df") == stored_data
        ):
            df = pd.read_json(stored_data, orient="split")
            graphs = []
            cat_cols = df.select_dtypes(include=["object", "category"]).columns
            for col in cat_cols:
                if df[col].nunique() < 20:
                    fig = px.histogram(df, x=col, title=f"Distribuição de {col}")
                    fig.update_layout(
                        plot_bgcolor="#222",
                        paper_bgcolor="#222",
                        font_color="white",
                        title_font_color="white"
                    )
                    graphs.append(
                        dbc.Card(
                            dbc.CardBody([
                                dcc.Graph(figure=fig, config={"displayModeBar": False})
                            ]),
                            style={
                                "backgroundColor": "#222",
                                "borderRadius": "16px",
                                "marginBottom": "24px",
                                "boxShadow": "0 2px 8px rgba(0,0,0,0.15)"
                            },
                            className="big-card"
                        )
                    )
            num_cols = df.select_dtypes(include=["number"]).columns
            for col in num_cols:
                fig = px.histogram(df, x=col, nbins=30, title=f"Histograma de {col}")
                fig.update_layout(
                    plot_bgcolor="#222",
                    paper_bgcolor="#222",
                    font_color="white",
                    title_font_color="white"
                )
                graphs.append(
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(figure=fig, config={"displayModeBar": False})
                        ]),
                        style={
                            "backgroundColor": "#222",
                            "borderRadius": "16px",
                            "marginBottom": "24px",
                            "boxShadow": "0 2px 8px rgba(0,0,0,0.15)"
                        },
                        className="big-card"
                    )
                )
            llm_summary = llm_summary_store.get("llm_summary", "")
            return graphs, html.Div([
                html.H5("🤖 Resumo Gerado por IA"),
                html.P(llm_summary)
            ]), no_update

        # Gera novo insight e salva no store
        df = pd.read_json(stored_data, orient="split")
        graphs = []
        cat_cols = df.select_dtypes(include=["object", "category"]).columns
        for col in cat_cols:
            if df[col].nunique() < 20:
                fig = px.histogram(df, x=col, title=f"Distribuição de {col}")
                fig.update_layout(
                    plot_bgcolor="#222",
                    paper_bgcolor="#222",
                    font_color="white",
                    title_font_color="white"
                )
                graphs.append(
                    dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(figure=fig, config={"displayModeBar": False})
                        ]),
                        style={
                            "backgroundColor": "#222",
                            "borderRadius": "16px",
                            "marginBottom": "24px",
                            "boxShadow": "0 2px 8px rgba(0,0,0,0.15)"
                        },
                        className="big-card"
                    )
                )
        num_cols = df.select_dtypes(include=["number"]).columns
        for col in num_cols:
            fig = px.histogram(df, x=col, nbins=30, title=f"Histograma de {col}")
            fig.update_layout(
                plot_bgcolor="#222",
                paper_bgcolor="#222",
                font_color="white",
                title_font_color="white"
            )
            graphs.append(
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(figure=fig, config={"displayModeBar": False})
                    ]),
                    style={
                        "backgroundColor": "#222",
                        "borderRadius": "16px",
                        "marginBottom": "24px",
                        "boxShadow": "0 2px 8px rgba(0,0,0,0.15)"
                    },
                    className="big-card"
                )
            )
        resumo_estatistico = df.describe(include="all").to_string()
        llm_summary = resumo_ia.gerar_resumo_ia(resumo_estatistico, model_provider="together")
        store_data = {
            "df": stored_data,
            "llm_summary": llm_summary
        }
        return graphs, html.Div([
            html.H5("🤖 Resumo Gerado por IA"),
            html.P(llm_summary)
        ]), store_data
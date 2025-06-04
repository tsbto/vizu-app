from dash import html, dcc, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from modules.resumo_ia import gerar_resumo_ia  # LLM

# Contexto estatístico de exemplo
resumo_contexto = """
Coluna 1: média=100, mediana=98, desvio padrão=5
Coluna 2: média=200, mediana=198, desvio padrão=10
Coluna 3: média=50, mediana=52, desvio padrão=2
"""

def layout():
    return html.Div([
        dcc.Store(id="stored-data", storage_type="session"),
        html.H3("🤖 QueryGPT", className="titulo-arial", style={"fontFamily": "Arial, sans-serif","fontSize": "34px", "fontStyle": "normal", "fontWeight": "bold", "marginBottom": "20px"}),

        html.P("Digite sua pergunta para a IA. O contexto estatístico será usado automaticamente!", style={"color": "#bbb"}),

        dbc.Input(id="query-gpt-input", placeholder="Digite aqui sua pergunta...", type="text", class_name="minimal-input"),

        html.Button("Enviar pergunta", id="query-gpt-btn", n_clicks=0, className="pill-btn"),

        html.Div(id="query-gpt-output", style={"marginTop": "20px", "color": "white", "whiteSpace": "pre-wrap"})
    ], style={"padding": "20px", "color": "white"})


def register_callbacks(app, pg_engine):

    @app.callback(
        Output("query-gpt-output", "children"),
        Input("query-gpt-btn", "n_clicks"),
        State("query-gpt-input", "value"),
        State("stored-data", "data"),
        prevent_initial_call=True
    )
    def gerar_resposta(n_clicks, pergunta, stored):
        if not pergunta:
            return ""

        # Junta a pergunta com o contexto estatístico
        prompt = f"Contexto do negócio:\n{resumo_contexto}\n\nPergunta do usuário:\n{pergunta}"

        # Gera a resposta final usando a IA
        resposta = gerar_resumo_ia(prompt, model_provider="together")  # ou "openai"

        # Se quiser salvar a pergunta e resposta, crie um novo dict (não tente salvar em stored)
        # Exemplo: salvar em outro dcc.Store se quiser persistir

        return resposta

    # Se quiser preencher o input com a última pergunta, use um dcc.Store separado para isso

    @app.callback(
        Output("query-gpt-input", "value"),
        Input("stored-data", "data"),
    )
    def preencher_input(stored):
        return ""

    # ⚠️ Removi o outro callback duplicado que usava "query-gpt-output"

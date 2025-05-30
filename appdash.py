import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from modules import home, okr, insights, querygpt, upload
from sqlalchemy import create_engine
from modules import resumo_ia as gerar_resumo_ia  # IMPORTANTE!

# Engine do Postgres
pg_engine = create_engine("postgresql://tarsobarreto@localhost:5432/vizu")

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])

# Estilos
SIDEBAR_STYLE = {
    "position": "fixed", "top": 0, "left": 0, "bottom": 0,
    "width": "220px", "padding": "20px",
    "backgroundColor": "#111", "color": "#eee"
}
CONTENT_STYLE = {"marginLeft": "240px", "marginTop": "20px", "padding": "20px"}

# Sidebar
sidebar = html.Div([
    html.H2("Vizu Dash App", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "fontSize": "18px", "marginBottom": "20px"}),
    html.Hr(className="sidebar-separator"),
    dbc.Nav([
        dbc.NavLink("Home", href="/", active="exact"),
        dbc.NavLink("OKRs", href="/okrs", active="exact"),
        dbc.NavLink("Insights", href="/insights", active="exact"),
        dbc.NavLink("QueryGPT", href="/querygpt", active="exact"),
        dbc.NavLink("Upload CSV", href="/upload", active="exact"),
    ], vertical=True, pills=True, style={"fontFamily": "Courier New, monospace", "fontSize": "14px"}),
], style=SIDEBAR_STYLE)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

# Simulação de onde vem o resumo estatístico
# No mundo real, você deve carregar isso do banco, de um arquivo CSV já processado, etc.
resumo_estatistico = """
Coluna 1: média=100, mediana=98, desvio padrão=5
Coluna 2: média=200, mediana=198, desvio padrão=10
Coluna 3: média=50, mediana=52, desvio padrão=2
"""

# Gera o resumo de IA (chamado de 'resumo_contexto' para usar na QueryGPT)
resumo_contexto = gerar_resumo_ia(resumo_estatistico)

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.layout()
    elif pathname == "/okrs":
        return html.H3("Página OKRs - em construção...", style={"color": "#eee"})
    elif pathname == "/insights":
        return insights.layout
    elif pathname == "/querygpt":
        # Agora passamos o resumo_contexto real para a página
        return querygpt.layout(resumo_contexto=resumo_contexto)
    elif pathname == "/upload":
        return upload.layout
    else:
        return dbc.Jumbotron([
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"A página {pathname} não existe."),
        ])

@app.callback(
    Output("query-gpt-output", "children"),
    Input("query-gpt-btn", "n_clicks"),
    State("query-gpt-input", "value"),
    prevent_initial_call=True  # evita rodar no carregamento
)
def gerar_resposta(n_clicks, pergunta):
    if pergunta:
        # Monta o prompt com o contexto já gerado
        from resumo_ia import gerar_resumo_ia  # opcional: se quiser reusar a função
        prompt = (
            f"Contexto do negócio:\n{resumo_contexto}\n\n"
            f"Pergunta do usuário:\n{pergunta}"
        )

        # Aqui você chama a mesma função ou um endpoint de LLM para gerar a resposta
        resposta = gerar_resumo_ia(prompt)
        return html.Pre(resposta, style={"whiteSpace": "pre-wrap"})
    return ""

# Callbacks extras
home.register_callbacks(app)
upload.register_callbacks(app, pg_engine=pg_engine)
insights.register_callbacks(app, pg_engine=pg_engine)

if __name__ == "__main__":
    app.run(debug=True)

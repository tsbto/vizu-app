import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from modules import home, okr, insights, querygpt, upload
from modules.resumo_ia import gerar_resumo_ia  # LLM

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
        dbc.NavLink("APIs", href="/upload", active="exact"),
    ], vertical=True, pills=True, style={"fontFamily": "Courier New, monospace", "fontSize": "14px"}),
], style=SIDEBAR_STYLE)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Store(id="stored-data", storage_type='session'),  # Store para persistir dados
    dcc.Location(id="url", refresh=False),
    sidebar,
    content,  # Aqui já está o page-content com o estilo correto
])


# Resumo estatístico de contexto
resumo_estatistico = """
Coluna 1: média=100, mediana=98, desvio padrão=5
Coluna 2: média=200, mediana=198, desvio padrão=10
Coluna 3: média=50, mediana=52, desvio padrão=2
"""
# Isso fica só guardado, **não gera nada sozinho**
resumo_contexto = resumo_estatistico  # se quiser pode já gerar um resumo aqui

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.layout()
    elif pathname == "/okrs":
        return okr.okr_module()
    elif pathname == "/insights":
        return insights.layout()
    elif pathname == "/querygpt":
        return querygpt.layout()
    elif pathname == "/upload":
        return upload.layout()
    else:
        return dbc.Jumbotron([
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"A página {pathname} não existe."),
        ])

# Callback pra gerar resposta do QueryGPT


# Callbacks extras
home.register_callbacks(app)
insights.register_callbacks(app, pg_engine=pg_engine)
querygpt.register_callbacks(app, pg_engine=pg_engine)
upload.register_callbacks(app, pg_engine=pg_engine)

if __name__ == "__main__":
    app.run(debug=True)

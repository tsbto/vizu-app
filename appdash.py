import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from modules import home, okr, insights, querygpt, upload, bigquery_utils
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

# Adicionamos a classe fade-in aqui, pro primeiro load já ter transição
content = html.Div(id="page-content", className="fade-in", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="stored-data", storage_type='session'),  # Store para persistir dados
    sidebar,
    content,
])

# Callback para renderizar páginas e aplicar fade-in sempre que muda
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        children = home.layout()
    elif pathname == "/okrs":
        children = okr.okr_module()
    elif pathname == "/insights":
        children = insights.layout()
    elif pathname == "/querygpt":
        children = querygpt.layout()
    elif pathname == "/upload":
        children = upload.layout()
    else:
        children = dbc.Jumbotron([
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"A página {pathname} não existe."),
        ])
    
    # Sempre coloca a classe fade-in no container de página
    return html.Div(children, className="fade-in")

# Callbacks extras
home.register_callbacks(app)
insights.register_callbacks(app)
querygpt.register_callbacks(app, pg_engine=pg_engine)
upload.register_callbacks(app, pg_engine=pg_engine)

if __name__ == "__main__":
    app.run(debug=True)

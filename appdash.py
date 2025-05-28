import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from modules import home, okr, insights, querygpt, upload  # já importou
from sqlalchemy import create_engine

pg_engine = create_engine("postgresql://tarsobarreto@localhost:5432/vizu")
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "220px",
    "padding": "20px",
    "backgroundColor": "#111",
    "color": "#eee",
}

CONTENT_STYLE = {
    "marginLeft": "240px",
    "marginTop": "20px",
    "padding": "20px",
}

sidebar = html.Div(
    [
        html.H2("Vizu Dash App", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "fontSize": "18px", "marginBottom": "20px"}),
        html.Hr(className="sidebar-separator"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact", style={"fontFamily": "Courier New, monospace", "fontSize": "14px"}),
                dbc.NavLink("OKRs", href="/okrs", active="exact", style={"fontFamily": "Courier New, monospace", "fontSize": "14px"}),
                dbc.NavLink("Insights", href="/insights", active="exact", style={"fontFamily": "Courier New, monospace", "fontSize": "14px"}),
                dbc.NavLink("QueryGPT", href="/querygpt", active="exact", style={"fontFamily": "Courier New, monospace", "fontSize": "14px"}),
                dbc.NavLink("Upload CSV", href="/upload", active="exact", style={"fontFamily": "Courier New, monospace", "fontSize": "14px"}),  # NOVA PÁGINA
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return home.layout()
    elif pathname == "/okrs":
        return html.H3("Página OKRs - em construção...", style={"color": "#eee"})
    elif pathname == "/insights":
        return html.H3("Página Insights - em construção...", style={"color": "#eee"})
    elif pathname == "/querygpt":
        return html.H3("Página QueryGPT - em construção...", style={"color": "#eee"})
    elif pathname == "/upload":  # ROTA NOVA
        return upload.layout
    else:
        return dbc.Jumbotron(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"A página {pathname} não existe."),
            ]
        )

# Registrar callbacks
home.register_callbacks(app)
upload.register_callbacks(app, pg_engine=pg_engine)  # passe a engine do Postgres aqui se quiser usar

if __name__ == "__main__":
    app.run(debug=True)

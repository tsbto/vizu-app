from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Importa páginas
from modules import home, okrs, insights, querygpt, dataframe

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
server = app.server

# Sidebar escura
sidebar = html.Div(
    [
        html.H2("Vizu Dash", className="display-4", style={"fontFamily": "Arial", "fontWeight": "bold"}),
        html.Hr(),
        html.P("Navegue entre as páginas:", className="lead", style={"fontFamily": "Courier New"}),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("OKRs", href="/okrs", active="exact"),
                dbc.NavLink("Insights", href="/insights", active="exact"),
                dbc.NavLink("QueryGPT", href="/querygpt", active="exact"),
                dbc.NavLink("DataFrame", href="/dataframe", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style={
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "backgroundColor": "#222222",
        "color": "white",
    },
)

# Layout principal com sidebar e conteúdo
content = html.Div(id="page-content", style={"marginLeft": "18rem", "marginRight": "2rem", "padding": "2rem 1rem"})

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content
])


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return home.layout()
    elif pathname == "/okrs":
        return okrs.layout()
    elif pathname == "/insights":
        return insights.layout()
    elif pathname == "/querygpt":
        return querygpt.layout()
    elif pathname == "/dataframe":
        return dataframe.layout()
    return html.H1("404: Página não encontrada", className="text-danger", style={"fontFamily": "Courier New"})


# Registra os callbacks de cada página
home.register_callbacks(app)
okrs.register_callbacks(app)
insights.register_callbacks(app)
querygpt.register_callbacks(app)
dataframe.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)

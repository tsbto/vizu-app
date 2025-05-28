from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

# Importa o layout e callbacks da página central (dataframe)
from modules import central

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # para deploy

# Layout principal com navbar e container para páginas
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),

    dbc.NavbarSimple(
        brand="Vizu Dash App",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Data Frame", href="/dataframe")),
        ],
    ),

    dbc.Container(id="page-content", className="pt-4")
])


# Callback para renderizar as páginas baseado na url
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page(pathname):
    if pathname == "/dataframe":
        return central.layout()
    # página Home simples
    return html.Div([
        html.H1("Bem-vindo ao Vizu Dash!"),
        html.P("Use o menu para navegar entre as páginas.")
    ])


# Registra os callbacks da página central
central.register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True)

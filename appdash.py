from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Componente para armazenar os dados carregados (JSON do dataframe)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='stored-data'),

    dbc.Nav([
        dbc.NavLink("Home", href="/", active="exact"),
        dbc.NavLink("Data Frame", href="/dataframe", active="exact"),
    ], pills=True, className="mb-4"),

    html.Div(id='page-content'),
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/dataframe':
        from modules.dataframe import layout, register_callbacks
        register_callbacks(app)
        return layout()
    else:
        return html.H3("Página inicial - Bem vindo!")

if __name__ == '__main__':
    app.run_server(debug=True)

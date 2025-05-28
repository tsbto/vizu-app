from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from modules import central

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Store(id="stored-data"),
    central.layout()
])

central.register_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)

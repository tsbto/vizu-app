from dash import Dash, html
import dash_bootstrap_components as dbc
from modules import central, dataframe

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    central.layout(),
    dataframe.layout(),
])

central.register_callbacks(app)
dataframe.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)

#card

import dash
import dash_bootstrap_components as dbc
from dash import html

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1("Minimalist Dark Design", className="text-center mb-4"),
        html.H2("Subtítulo Secundário", className="text-center mb-4"),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Cartão de Exemplo", className="card-title"),
                                html.P("Este é um conteúdo do cartão, apenas para fins de teste.", className="card-text"),
                                dbc.Button("Botão Pílula", color="secondary", className="pill-btn"),
                            ]
                        ),
                        className="custom-card"
                    ),
                    width=2,
                ),
            ],
            justify="left"
        ),
    ],
    fluid=True,
    className="dark-container"
)

if __name__ == "__main__":
    app.run(debug=True)

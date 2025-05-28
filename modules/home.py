from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

def layout():
    return html.Div(
        [
            html.H2("Home", className="page-title"),
            html.P("Escolha a fonte de dados:", className="card-text"),
            dbc.Row(
                [
                    # Card 1 - BigQuery
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Img(
                                    src="https://cdn.iconscout.com/icon/free/png-256/google-bigquery-3629288-3029137.png",
                                    style={"height": "50px", "margin": "10px auto", "display": "block"}
                                ),
                                html.H5("BigQuery", className="card-title text-center"),
                                dbc.Button(
                                    "Conectar",
                                    id="btn-bigquery",
                                    className="btn-pill",
                                    color="light",
                                    style={"margin": "10px auto", "display": "block"}
                                )
                            ],
                            className="p-3 text-center",
                            style={"backgroundColor": "#1e1e1e", "color": "#fff", "borderRadius": "8px"},
                        ),
                        width=4,
                    ),

                    # Card 2 - Snowflake
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Img(
                                    src="https://cdn-icons-png.flaticon.com/512/5969/5969174.png",
                                    style={"height": "50px", "margin": "10px auto", "display": "block"}
                                ),
                                html.H5("Snowflake", className="card-title text-center"),
                                dbc.Button(
                                    "Conectar",
                                    id="btn-snowflake",
                                    className="btn-pill",
                                    color="light",
                                    style={"margin": "10px auto", "display": "block"}
                                )
                            ],
                            className="p-3 text-center",
                            style={"backgroundColor": "#1e1e1e", "color": "#fff", "borderRadius": "8px"},
                        ),
                        width=4,
                    ),

                    # Card 3 - CSV
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Img(
                                    src="https://cdn-icons-png.flaticon.com/512/337/337946.png",
                                    style={"height": "50px", "margin": "10px auto", "display": "block"}
                                ),
                                html.H5("CSV", className="card-title text-center"),
                                dbc.Button(
                                    "Conectar",
                                    id="btn-csv",
                                    className="btn-pill",
                                    color="light",
                                    style={"margin": "10px auto", "display": "block"}
                                )
                            ],
                            className="p-3 text-center",
                            style={"backgroundColor": "#1e1e1e", "color": "#fff", "borderRadius": "8px"},
                        ),
                        width=4,
                    ),
                ],
                className="mt-4",
            ),
        ],
        style={"padding": "20px"},
    )

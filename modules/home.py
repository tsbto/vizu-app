from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

def layout():
    return html.Div(
        [
            html.H1("Página Home", style={
                "fontFamily": "Arial", 
                "fontWeight": "bold", 
                "color": "white", 
                "fontSize": "1.5rem",  # título menor
                "marginBottom": "20px"
            }),

            html.Div(
                [
                    # Card BigQuery
                    dbc.Card(
                        [
                            html.Div(
                                html.Img(src="/assets/bigquery.png", style={
                                    "width": "40px", 
                                    "marginBottom": "10px"
                                }),
                                style={"textAlign": "center"}
                            ),
                            html.H4("BigQuery", style={
                                "fontFamily": "Courier New", 
                                "color": "white", 
                                "textAlign": "center", 
                                "fontSize": "0.9rem"
                            }),
                            dbc.Button("Conectar", id="btn-bq", color="light", className="pill-btn mt-2"),
                            dbc.Collapse(
                                dbc.CardBody([
                                    dcc.Input(id="bq-credentials", type="text", placeholder="Insira credenciais...", style={
                                        "width": "100%", 
                                        "fontSize": "0.8rem"
                                    }),
                                    dbc.Button("Salvar", id="btn-save-bq", color="success", className="pill-btn mt-2"),
                                ]),
                                id="collapse-bq",
                                is_open=False,
                            )
                        ],
                        color="dark",
                        style={"width": "180px", "margin": "10px", "padding": "10px"}
                    ),

                    # Card Snowflake
                    dbc.Card(
                        [
                            html.Div(
                                html.Img(src="/assets/snowflake.png", style={
                                    "width": "40px", 
                                    "marginBottom": "10px"
                                }),
                                style={"textAlign": "center"}
                            ),
                            html.H4("Snowflake", style={
                                "fontFamily": "Courier New", 
                                "color": "white", 
                                "textAlign": "center", 
                                "fontSize": "0.9rem"
                            }),
                            dbc.Button("Conectar", id="btn-snow", color="light", className="pill-btn mt-2"),
                            dbc.Collapse(
                                dbc.CardBody([
                                    dcc.Input(id="snow-credentials", type="text", placeholder="Insira credenciais...", style={
                                        "width": "100%", 
                                        "fontSize": "0.8rem"
                                    }),
                                    dbc.Button("Salvar", id="btn-save-snow", color="success", className="pill-btn mt-2"),
                                ]),
                                id="collapse-snow",
                                is_open=False,
                            )
                        ],
                        color="dark",
                        style={"width": "180px", "margin": "10px", "padding": "10px"}
                    ),

                    # Card CSV
                    dbc.Card(
                        [
                            html.Div(
                                html.Img(src="/assets/csv.png", style={
                                    "width": "40px", 
                                    "marginBottom": "10px"
                                }),
                                style={"textAlign": "center"}
                            ),
                            html.H4("CSV", style={
                                "fontFamily": "Courier New", 
                                "color": "white", 
                                "textAlign": "center", 
                                "fontSize": "0.9rem"
                            }),
                            dbc.Button("Conectar", id="btn-csv", color="light", className="pill-btn mt-2"),
                            dbc.Collapse(
                                dbc.CardBody([
                                    dcc.Input(id="csv-path", type="text", placeholder="Caminho do CSV...", style={
                                        "width": "100%", 
                                        "fontSize": "0.8rem"
                                    }),
                                    dbc.Button("Salvar", id="btn-save-csv", color="success", className="pill-btn mt-2"),
                                ]),
                                id="collapse-csv",
                                is_open=False,
                            )
                        ],
                        color="dark",
                        style={"width": "180px", "margin": "10px", "padding": "10px"}
                    ),
                ],
                style={"display": "flex", "justifyContent": "center", "gap": "15px"}
            ),
        ],
        style={"backgroundColor": "#1a1a1a", "padding": "20px"}
    )

def register_callbacks(app):
    @app.callback(
        Output("collapse-bq", "is_open"),
        Input("btn-bq", "n_clicks"),
        State("collapse-bq", "is_open"),
        prevent_initial_call=True
    )
    def toggle_bq(n, is_open):
        return not is_open

    @app.callback(
        Output("collapse-snow", "is_open"),
        Input("btn-snow", "n_clicks"),
        State("collapse-snow", "is_open"),
        prevent_initial_call=True
    )
    def toggle_snow(n, is_open):
        return not is_open

    @app.callback(
        Output("collapse-csv", "is_open"),
        Input("btn-csv", "n_clicks"),
        State("collapse-csv", "is_open"),
        prevent_initial_call=True
    )
    def toggle_csv(n, is_open):
        return not is_open

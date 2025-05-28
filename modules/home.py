from dash import html, dcc, Input, Output, callback 
import dash_bootstrap_components as dbc
import dash

def layout():
    card_style = {
        "width": "150px",
        "height": "150px",
        "borderRadius": "20px",
        "backgroundColor": "#333",
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "justifyContent": "center",
        "cursor": "pointer",
        "margin": "10px",
    }

    icons = {
        "bigquery": "/assets/bigquery.png",
        "snowflake": "/assets/snowflake.png",
        "csv": "/assets/csv.png",
    }

    cards = []
    for key, label in [("bigquery", "BigQuery"), ("snowflake", "Snowflake"), ("csv", "CSV")]:
        card = html.Div([
            # Título no topo à esquerda, em capslock
            html.Div(label.upper(), style={
                "textAlign": "left",
                "fontFamily": "Arial, sans-serif",
                "fontWeight": "bold",
                "fontSize": "9px",
                "color": "#ffffff",
                "marginBottom": "8px",
                "marginLeft": "100px",
                "width": "100%",  # força o alinhamento à esquerda
            }),
            # Imagem centralizada
            html.Img(src=icons[key], style={
                "width": "64px",
                "height": "64px",
                "display": "block",
                "margin": "0 auto",
            }),
            # Botão com classe btn-pill, estilo via CSS
            dbc.Button("Conectar", id=f"btn-{key}", n_clicks=0, className="btn-pill", style={"marginTop": "30px"}),
            # Container do dropdown
            html.Div(id=f"dropdown-{key}-container")
        ], className="card-custom", style=card_style, id=f"card-{key}")
        cards.append(card)

    return html.Div([
        html.H2("Home", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "fontSize": "20px", "color": "#eee", "marginBottom": "30px"}),
        html.Div(cards, style={"display": "flex", "justifyContent": "center"}),
    ], style={"padding": "30px"})


def register_callbacks(app):
    # Callback que mostra/esconde o dropdown no card clicado
    @app.callback(
        [Output(f"dropdown-{key}-container", "children") for key in ["bigquery", "snowflake", "csv"]],
        [Input(f"btn-{key}", "n_clicks") for key in ["bigquery", "snowflake", "csv"]],
    )
    def toggle_dropdown(*btn_clicks):
        ctx = dash.callback_context
        if not ctx.triggered:
            return [""] * 3

        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        outputs = []
        for key in ["bigquery", "snowflake", "csv"]:
            idx = ["bigquery", "snowflake", "csv"].index(key)
            if f"btn-{key}" == button_id and btn_clicks[idx] % 2 == 1:
                dropdown = html.Div([
                    dcc.Input(placeholder="Usuário", type="text", style={"marginBottom": "8px", "width": "100%"}),
                    dcc.Input(placeholder="Senha", type="password", style={"marginBottom": "8px", "width": "100%"}),
                    dcc.Input(placeholder="Projeto/Database", type="text", style={"marginBottom": "8px", "width": "100%"}),
                    dbc.Button("Salvar", color="primary", size="sm", style={"width": "100%"}),
                ], style={"marginTop": "10px"})
                outputs.append(dropdown)
            else:
                outputs.append("")
        return outputs

    # Callback genérico para alternar a classe dos botões entre "btn-pill" e "btn-pill active"
    for key in ["bigquery", "snowflake", "csv"]:
        @app.callback(
            Output(f"btn-{key}", "className"),
            Input(f"btn-{key}", "n_clicks"),
            prevent_initial_call=True
        )
        def toggle_button_class(n_clicks, key=key):
            if n_clicks and n_clicks % 2 != 0:
                return "btn-pill active"
            return "btn-pill"

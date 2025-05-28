from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import dash

def layout():
    card_style = {
        "width": "150px",
        "height": "150px",
        "borderRadius": "20px",
        "backgroundColor": "#333",  # cinza escuro
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "justifyContent": "center",
        "cursor": "pointer",
        "margin": "10px",
    }
    button_style = {
        "borderRadius": "20px",
        "backgroundColor": "#fff",
        "color": "#000",
        "fontSize": "12px",
        "padding": "6px 12px",
        "border": "none",
        "marginTop": "10px",
        "width": "110px",
    }

    icons = {
        "bigquery": "/Users/tarsobarreto/Documents/vizu-dash/assets/bigquery.png",
        "snowflake": "/Users/tarsobarreto/Documents/vizu-dash/assets/snowflake.png",
        "csv": "/Users/tarsobarreto/Documents/vizu-dash/assets/csv.png",
    }

    cards = []
    for key, label in [("bigquery", "BigQuery"), ("snowflake", "Snowflake"), ("csv", "CSV")]:
        card = html.Div([
            html.Img(src=icons[key], style={"width": "64px", "height": "64px"}),
            html.Div(label, style={"marginTop": "10px", "fontFamily": "Arial, sans-serif", "fontWeight": "bold", "fontSize": "14px", "color": "#333"}),
            dbc.Button("Conectar", id=f"btn-{key}", n_clicks=0, style=button_style),
            html.Div(id=f"dropdown-{key}-container")
        ], style=card_style, id=f"card-{key}")
        cards.append(card)

    return html.Div([
        html.H2("Home", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "fontSize": "20px", "color": "#eee", "marginBottom": "30px"}),
        html.Div(cards, style={"display": "flex", "justifyContent": "center"}),
    ], style={"padding": "30px"})

def register_callbacks(app):
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
            if f"btn-{key}" == button_id and btn_clicks[["bigquery", "snowflake", "csv"].index(key)] % 2 == 1:
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

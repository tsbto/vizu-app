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
        "bigquery": "/assets/bigquery.png",
        "snowflake": "/assets/snowflake.png",
        "csv": "/assets/csv.png",
    }

    cards = []
    for key, label in [("bigquery", "BigQuery"), ("snowflake", "Snowflake"), ("csv", "CSV")]:
    card = html.Div([
        # Título no topo à esquerda
        html.Div(label.upper(), style={
            "textAlign": "left",
            "fontFamily": "Arial, sans-serif",
            "fontWeight": "bold",
            "fontSize": "9px",
            "color": "#ffffff",
            "marginBottom": "8px",
        }),
        # Imagem centralizada
        html.Img(src=icons[key], style={
            "width": "64px",
            "height": "64px",
            "display": "block",
            "margin": "0 auto",
        }),
        # Botão "Conectar"
        dbc.Button("Conectar", id=f"btn-{key}", n_clicks=0, className="btn-pill"),
        # Dropdown container
        html.Div(id=f"dropdown-{key}-container")
    ], className="card-custom", id=f"card-{key}")
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
    
    @app.callback(
        Output("btn-bigquery", "className"),
        Input("btn-bigquery", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_bigquery_class(n_clicks):
        if n_clicks and n_clicks % 2 != 0:
            return "btn-pill active"
        return "btn-pill"

    @app.callback(
        Output("btn-snowflake", "className"),
        Input("btn-snowflake", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_snowflake_class(n_clicks):
        if n_clicks and n_clicks % 2 != 0:
            return "btn-pill active"
        return "btn-pill"

    @app.callback(
        Output("btn-csv", "className"),
        Input("btn-csv", "n_clicks"),
        prevent_initial_call=True
    )
    def toggle_csv_class(n_clicks):
        if n_clicks and n_clicks % 2 != 0:
            return "btn-pill active"
        return "btn-pill"
from dash import html, dcc

def dropdown_card(options):
    return html.Div(
        className="card",
        children=[
            html.H2("Selecione", style={"fontFamily": "Arial"}),
            dcc.Dropdown(
                options=[{"label": opt, "value": opt} for opt in options],
                placeholder="Escolha uma opção",
                style={"backgroundColor": "transparent", "color": "white"}
            )
        ]
    )

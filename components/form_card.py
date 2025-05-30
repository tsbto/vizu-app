from dash import html, dcc

def form_card():
    return html.Div(
        className="card",
        children=[
            html.H2("Formulário", style={"fontFamily": "Arial"}),
            html.Label("Nome:", style={"fontFamily": "Courier New"}),
            dcc.Input(type="text", placeholder="Digite seu nome"),
            html.Label("Email:", style={"fontFamily": "Courier New"}),
            dcc.Input(type="email", placeholder="Digite seu email"),
            html.Button("Enviar", className="pill-btn")
        ]
    )

from dash import html

def layout():
    return html.Div([
        html.H1("QueryGPT", style={"fontFamily": "Arial", "fontWeight": "bold"}),
        html.P("Aqui você pode interagir com o modelo QueryGPT.", style={"fontFamily": "Courier New"})
    ])

def register_callbacks(app):
    pass  # Se não tiver callback ainda

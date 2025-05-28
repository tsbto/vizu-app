from dash import html

def layout():
    return html.Div([
        html.H1("Página Insights", style={"fontFamily": "Arial", "fontWeight": "bold"}),
        html.P("Aqui você pode visualizar insights e análises.", style={"fontFamily": "Courier New"})
    ])

def register_callbacks(app):
    pass  # Se não tiver callback ainda

from dash import html

def layout():
    return html.Div([
        html.H1("OKRs", style={"fontFamily": "Arial", "fontWeight": "bold"}),
        html.P("Aqui você pode gerenciar seus OKRs.", style={"fontFamily": "Courier New"}),
    ])

def register_callbacks(app):
    pass

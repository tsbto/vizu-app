from dash import html

def layout():
    return html.Div([
        html.H1("Bem-vindo ao Vizu Dash!", style={"fontFamily": "Arial", "fontWeight": "bold"}),
        html.P("Use o menu lateral para navegar entre as páginas.", style={"fontFamily": "Courier New"}),
    ])

def register_callbacks(app):
    pass

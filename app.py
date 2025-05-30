import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    [
        html.H1("Minimalist Dark Design", className="text-center mb-4", style={
            "fontFamily": "Arial",
            "fontWeight": "bold",
            "fontSize": "40px",
        }),
        html.H2("Subtítulo Secundário", className="text-center mb-4", style={
            "fontFamily": "Arial",
            "fontWeight": "bold",
            "fontSize": "30px",
        }),

        # Cartão de exemplo
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Cartão de Exemplo", className="card-title"),
                                html.P("Este é um conteúdo do cartão, apenas para fins de teste.", className="card-text"),
                                dbc.Button("Botão Pílula", color="secondary", className="pill-btn"),
                            ]
                        ),
                        className="custom-card"
                    ),
                    width=4,
                ),
            ],
            justify="start"
        ),

        # Formulário dentro de um card igual ao primeiro
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Formulário Minimalista", className="card-title"),

                                html.Label("Nome:", style={"fontFamily": "Courier New"}),
                                dcc.Input(
                                    type="text",
                                    placeholder="Digite seu nome",
                                    style={
                                        "backgroundColor": "#222221",
                                        "border": "none",
                                        "borderBottom": "1px solid white",
                                        "color": "white",
                                        "padding": "0.5rem 1rem",
                                        "width": "100%",
                                        "marginBottom": "1rem",
                                        "fontFamily": "Courier New"
                                    },
                                ),

                                html.Label("Email:", style={"fontFamily": "Courier New"}),
                                dcc.Input(
                                    type="email",
                                    placeholder="Digite seu email",
                                    style={
                                        "backgroundColor": "#222221",
                                        "border": "none",
                                        "borderBottom": "1px solid white",
                                        "color": "white",
                                        "padding": "0.5rem 1rem",
                                        "width": "100%",
                                        "marginBottom": "1rem",
                                        "fontFamily": "Courier New"
                                    },
                                ),

                                html.Label("Selecione uma opção:", style={"fontFamily": "Courier New"}),
                                dcc.Dropdown(
                                    options=[
                                        {"label": "Opção 1", "value": "1"},
                                        {"label": "Opção 2", "value": "2"},
                                        {"label": "Opção 3", "value": "3"},
                                    
                                    ],
                                    placeholder="Escolha...",
                                    style={
                                        "backgroundColor": "#222221",
                                        "border": "none",
                                        "borderBottom": "0px",
                                        "color": "222221",
                                        "borderRadius": "0",
                                        "marginBottom": "0rem",
                                        "fontFamily": "Courier New"
                                    },
                                    className="dropdown-custom"
                                ),

                                html.Label("Selecione suas opções:", style={"fontFamily": "Courier New"}),
                                dcc.Checklist(
                                    options=[
                                        {"label": "Checkbox 1", "value": "cb1"},
                                        {"label": "Checkbox 2", "value": "cb2"},
                                        {"label": "Checkbox 3", "value": "cb3"},
                                    ],
                                    style={
                                        "marginBottom": "1rem",
                                        "fontFamily": "Courier New",
                                        "color": "white",
                                        "backgroundColor": "#222221",
                                        "padding": "0.5rem",
                                        "borderRadius": "5px",
                                    },
                                    inputStyle={
                                        "marginRight": "0.5rem",
                                        "accentColor": "#222221",
                                        "backgroundColor": "#222221",
                                        "border": "1px solid white"
                                    },
                                    labelStyle={"marginRight": "1rem"}
                                ),

                                dbc.Button("ENVIAR", color="secondary", className="pill-btn"),
                            ]
                        ),
                        className="custom-card"
                    ),
                    width=4,
                ),
            ],
            justify="start"
        ),
    ],
    fluid=True,
    className="dark-container",
    style={
        "backgroundColor": "#121212",
        "minHeight": "100vh",
        "padding": "2rem",
        "color": "white",
        "fontFamily": "Courier New",
    }
)

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Minimalist Dash App</title>
        {%favicon%}
        {%css%}
        <style>
            body, .dark-container {
                background-color: #121212;
                color: white;
                font-family: 'Courier New', monospace;
            }
            h1, h2 {
                font-family: Arial, sans-serif;
                font-weight: bold;
            }
            .pill-btn {
                margin-top: 0.5rem;
                font-family: Arial, sans-serif;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 0.55rem;
                border: 0.5px solid white;
                border-radius: 999px;
                background-color: transparent;
                color: white;
                transition: all 0.3s ease;
                padding: 0.5rem 1rem;
            }
            .pill-btn:hover,
            .pill-btn:focus,
            .pill-btn:active {
                background-color: white;
                color: #121212;
                border-color: white;
                text-decoration: none;
            }
            .custom-card {
                margin-left: 1rem;
                background-color: #222221;
                border: 0px solid white;
                border-radius: 40px;
                padding: 1rem;
                margin-bottom: 1rem;
            }
            .card-title {
                font-family: Arial, sans-serif;
                font-weight: bold;
                color: white;
                font-size: 18px;
                margin-bottom: 1rem;
            }
            .card-text {
                font-family: 'Courier New', monospace;
                color: white;
                font-size: 0.7rem;
            }
            /* Checklist customizado */
            input[type="checkbox"] {
                -webkit-appearance: none;
                appearance: none;
                background-color: #121212;
                margin: 0;
                font: inherit;
                color: white;
                width: 1rem;
                height: 1rem;
                border: 1px solid white;
                border-radius: 2px;
                display: grid;
                place-content: center;
                cursor: pointer;
            }
            input[type="checkbox"]:checked::before {
                content: "";
                width: 0.5rem;
                height: 0.5rem;
                background-color: white;
            }
            select, .dropdown-custom > div > div {
                background-color: #121212 !important;
                border: none !important;
                border-bottom: 2px solid white !important;
                color: white !important;
                border-radius: 0 !important;
            }
            input:focus, select:focus, .dropdown-custom > div > div:focus-within {
                outline: none;
                border-color: white;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)

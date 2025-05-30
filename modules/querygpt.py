from dash import html, dcc
import dash_bootstrap_components as dbc

def layout(resumo_contexto: str = ""):
    return html.Div([
        html.H3("QueryGPT", style={"color": "#eee"}),
        html.P("Este é o resumo de contexto gerado automaticamente:", style={"color": "#aaa"}),
        html.Pre(resumo_contexto, style={
            "backgroundColor": "#222",
            "color": "#ddd",
            "padding": "10px",
            "borderRadius": "5px",
            "whiteSpace": "pre-wrap"
        }),
        html.Hr(),
        html.P("Digite sua pergunta abaixo:", style={"color": "#aaa"}),
        dbc.Input(id="query-gpt-input", type="text", placeholder="Digite sua pergunta...", debounce=True),
        dbc.Button("Enviar para GPT", id="query-gpt-btn", color="primary", style={"marginTop": "10px"}),
        html.Br(),
        html.Div(id="query-gpt-output", style={"marginTop": "20px", "color": "#eee"})
    ])

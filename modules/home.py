from dash import html, dcc, Input, Output, callback 
import dash_bootstrap_components as dbc

def layout():
    return html.Div([
        html.H2("Bem-vindo ao Vizu Dash App!", style={"fontFamily": "Arial, sans-serif", "fontSize": "24px", "fontWeight": "bold", "marginBottom": "20px"}),
        html.P(
            "Este dashboard permite que você faça upload de dados, gere insights automáticos com IA, "
            "explore OKRs e utilize QueryGPT para perguntas inteligentes sobre seus dados.",
            style={"fontSize": "18px", "color": "#bbb"}
        ),
        html.Ul([
            html.Li("Use o menu à esquerda para navegar entre as funcionalidades."),
            html.Li("Faça upload de um CSV ou conecte-se ao BigQuery/Snowflake em 'APIs'."),
            html.Li("Veja insights automáticos em 'Insights'."),
            html.Li("Gerencie OKRs em 'OKRs'."),
            html.Li("Converse com a IA em 'QueryGPT'."),
        ], style={"fontSize": "16px", "marginTop": "20px"}),
        html.P("Dúvidas ou sugestões? Fale com o time de dados!", style={"marginTop": "30px", "color": "#888"})
    ], style={"padding": "40px", "color": "white"})
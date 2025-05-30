from dash import html

def insights_card(insight_text):
    return html.Div(
        className="card",
        children=[
            html.H2("Insight do Dia", style={"fontFamily": "Arial"}),
            html.P(insight_text, style={"fontFamily": "Courier New", "fontSize": "0.8rem"})
        ]
    )

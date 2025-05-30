from dash import html

def kpi_card(title, value):
    return html.Div(
        className="card",
        children=[
            html.H2(title, style={"fontFamily": "Arial","fontSize": "0.5rem", "text-transform": "uppercase"}),
            html.H1(value, style={"fontFamily":"Arial", "fontSize": "2rem", "margin": "0"})
        ]
    )

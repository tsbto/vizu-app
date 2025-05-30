from dash import html, dcc

def tasks_card(tasks):
    return html.Div(
        className="card",
        children=[
            html.H2("Checklist", style={"fontFamily": "Arial"}),
            dcc.Checklist(
                options=[{"label": task, "value": task} for task in tasks],
                value=[],
                inputStyle={
                    "appearance": "none",
                    "backgroundColor": "#121212",
                    "border": "1px solid white",
                    "width": "1rem",
                    "height": "1rem",
                    "marginRight": "0.5rem",
                    "cursor": "pointer"
                },
                labelStyle={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}
            )
        ]
    )

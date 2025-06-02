from dash import html
import dash_bootstrap_components as dbc

def okr_module():
    return html.Div([
        # Header e botão Add OKR alinhados
        dbc.Row([
            dbc.Col(html.H1("OKRs Management"), width="auto"),
            dbc.Col(html.P("Set and track your Objectives and Key Results"), width="auto"),
            dbc.Col(html.Div([
                html.Button("+ Add OKR", className="pill-btn")
            ], style={"textAlign": "right"}), width=True)
        ], align="center", justify="between", style={"marginBottom": "2rem"}),

        # Linha de cards de OKRs (3 cards lado a lado)
        dbc.Row([
            dbc.Col(
                dbc.Card([
                    html.Div([
                        html.H2("Increase Customer Satisfaction", className="card-title"),
                        html.Div([
                            html.Button("✏️", className="pill-btn"),
                            html.Button("🗑️", className="pill-btn"),
                        ], style={"marginLeft": "auto", "display": "flex", "gap": "0.3rem"})
                    ], style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}),
                    html.P("Key Results:"),
                    html.Ul([
                        html.Li("Achieve NPS score of 8.5+"),
                        html.Li("Reduce customer churn by 15%"),
                        html.Li("Increase support response time to under 2 hours")
                    ]),
                    html.P("Progress"),
                    html.Div([
                        html.Div(style={
                            "width": "75%",
                            "backgroundColor": "#3498db",
                            "height": "8px",
                            "borderRadius": "999px"
                        }),
                    ], style={
                        "backgroundColor": "#333",
                        "borderRadius": "999px",
                        "height": "8px",
                        "marginBottom": "0.5rem",
                        "overflow": "hidden"
                    }),
                    html.P("75%")
                ], className="custom-card"), width=4),

            dbc.Col(
                dbc.Card([
                    html.Div([
                        html.H2("Drive Revenue Growth", className="card-title"),
                        html.Div([
                            html.Button("✏️", className="pill-btn"),
                            html.Button("🗑️", className="pill-btn"),
                        ], style={"marginLeft": "auto", "display": "flex", "gap": "0.3rem"})
                    ], style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}),
                    html.P("Key Results:"),
                    html.Ul([
                        html.Li("Increase monthly recurring revenue by 25%"),
                        html.Li("Acquire 500 new customers"),
                        html.Li("Improve conversion rate to 3.5%")
                    ]),
                    html.P("Progress"),
                    html.Div([
                        html.Div(style={
                            "width": "60%",
                            "backgroundColor": "#3498db",
                            "height": "8px",
                            "borderRadius": "999px"
                        }),
                    ], style={
                        "backgroundColor": "#333",
                        "borderRadius": "999px",
                        "height": "8px",
                        "marginBottom": "0.5rem",
                        "overflow": "hidden"
                    }),
                    html.P("60%")
                ], className="custom-card"), width=4),

            dbc.Col(
                dbc.Card([
                    html.Div([
                        html.H2("Enhance Product Performance", className="card-title"),
                        html.Div([
                            html.Button("✏️", className="pill-btn"),
                            html.Button("🗑️", className="pill-btn"),
                        ], style={"marginLeft": "auto", "display": "flex", "gap": "0.3rem"})
                    ], style={"display": "flex", "alignItems": "center", "marginBottom": "0.5rem"}),
                    html.P("Key Results:"),
                    html.Ul([
                        html.Li("Reduce page load time to under 2 seconds"),
                        html.Li("Achieve 99.9% uptime"),
                        html.Li("Launch 3 new feature releases")
                    ]),
                    html.P("Progress"),
                    html.Div([
                        html.Div(style={
                            "width": "45%",
                            "backgroundColor": "#3498db",
                            "height": "8px",
                            "borderRadius": "999px"
                        }),
                    ], style={
                        "backgroundColor": "#333",
                        "borderRadius": "999px",
                        "height": "8px",
                        "marginBottom": "0.5rem",
                        "overflow": "hidden"
                    }),
                    html.P("45%")
                ], className="custom-card"), width=4),
        ], style={"marginBottom": "2rem"}),

        # Linha de cards de status (3 cards)
        dbc.Row([
            dbc.Col(dbc.Card([
                html.P("🟢 On Track"),
                html.H2("2 OKRs")
            ], className="custom-card"), width=4),

            dbc.Col(dbc.Card([
                html.P("🟡 At Risk"),
                html.H2("1 OKR")
            ], className="custom-card"), width=4),

            dbc.Col(dbc.Card([
                html.P("🔵 Average Progress"),
                html.H2("60%")
            ], className="custom-card"), width=4),
        ])
    ], style={"padding": "2rem", "color": "white"})

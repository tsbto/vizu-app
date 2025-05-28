from dash import Dash, html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
from modules import central
from data import data_loader

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Sidebar com menu vertical e estilo
sidebar = html.Div(
    [
        html.H2("Vizu", className="display-4", style={"color": "white", "fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.Hr(style={"borderColor": "gray"}),
        dbc.Nav(
            [
                dbc.NavLink("Central de Conexões", href="/central", active="exact", style={"borderRadius": "9999px"}),
                dbc.NavLink("OKRs", href="/okrs", active="exact", style={"borderRadius": "9999px"}),
                dbc.NavLink("Data Frame", href="/dataframe", active="exact", style={"borderRadius": "9999px"}),
                dbc.NavLink("Insights", href="/insights", active="exact", style={"borderRadius": "9999px"}),
                dbc.NavLink("Query GPT", href="/querygpt", active="exact", style={"borderRadius": "9999px"}),
            ],
            vertical=True,
            pills=True,
            style={"color": "white"},
        ),
    ],
    style={
        "backgroundColor": "#121212",
        "padding": "2rem",
        "position": "fixed",
        "height": "100vh",
        "width": "16rem",
        "overflowY": "auto",
    },
)

# Conteúdo principal
content = html.Div(id="page-content", style={"marginLeft": "18rem", "padding": "2rem", "color": "white", "fontFamily": "'Courier New', monospace"})

def home_content():
    return html.Div([
        html.H1("A Vizu é uma proposta inovadora", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif", "marginBottom": "1rem"}),
        html.P(
            "A Vizu é uma proposta inovadora que combina o melhor de uma consultoria com a agilidade e criatividade de uma software house. Atuamos para transformar dados e oportunidades em estratégias sólidas e produtos digitais que geram impacto real. Usamos inteligência artificial, RAG (Retrieval-Augmented Generation) e tecnologias de ponta para expandir o potencial de cada cliente — mas com o cuidado e a visão de um parceiro que entende que cada desafio é único.",
            style={"marginBottom": "2rem"},
        ),
        html.P(
            "Acreditamos que estamos vivendo algo novo: a era da internet de verdade. Por isso, somos uma nova empresa para um novo momento. Uma empresa que surge para ajudar marcas e negócios a navegarem essa nova fase com inteligência e ousadia — conectando dados, pessoas e ideias para criar o futuro que todos queremos viver.",
            style={"marginBottom": "2rem"},
        ),
    ])

def okrs_content():
    return html.Div([
        html.H2("OKRs", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.P("Aqui vai o conteúdo do módulo OKRs."),
    ])

def dataframe_content():
    return html.Div([
        html.H2("Data Frame", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.P("Aqui vai o conteúdo do módulo Data Frame."),
    ])

def insights_content():
    return html.Div([
        html.H2("Insights", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.P("Aqui vai o conteúdo do módulo Insights."),
    ])

def querygpt_content():
    return html.Div([
        html.H2("Query GPT", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.P("Aqui vai o conteúdo do módulo Query GPT."),
    ])

# Layout principal
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,
])

# Callback para renderizar o conteúdo da página
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/" or pathname == "/home":
        return home_content()
    elif pathname == "/central":
        return central.layout  # Supondo que central.layout esteja definido
    elif pathname == "/okrs":
        return okrs_content()
    elif pathname == "/dataframe":
        return dataframe_content()
    elif pathname == "/insights":
        return insights_content()
    elif pathname == "/querygpt":
        return querygpt_content()
    else:
        return html.Div([
            html.H1("404: Página não encontrada", style={"color": "red"}),
            html.P(f"O caminho {pathname} não existe."),
        ])

if __name__ == "__main__":
    app.run(debug=True)

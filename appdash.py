from dash import Dash, html, dcc, Input, Output, State, no_update, ctx
import dash_bootstrap_components as dbc
from dash import dash_table
import base64
import io
import pandas as pd

from modules import central
from data import data_loader

# Função de placeholder para carregar dados do BigQuery
def carregar_tabela_bigquery(project, dataset, table, json_keyfile):
    # Retorne um DataFrame aqui. Exemplo:
    return pd.DataFrame({
        "coluna1": [1, 2, 3],
        "coluna2": ["A", "B", "C"]
    })

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])

# Sidebar
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

# Layout principal
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="stored-data"),
    sidebar,
    content,
])

# Páginas de conteúdo
def home_content():
    return html.Div([
        html.H1("A Vizu é uma proposta inovadora", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif", "marginBottom": "1rem"}),
        html.P(
            "A Vizu é uma proposta inovadora que combina o melhor de uma consultoria com a agilidade e criatividade de uma software house...",
            style={"marginBottom": "2rem"},
        ),
    ])

def okrs_content():
    return html.Div([
        html.H2("OKRs", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.P("Aqui vai o conteúdo do módulo OKRs."),
    ])

from dash import dash_table

def dataframe_content():
    return html.Div([
        html.H2("Data Frame", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.P("Aqui está a visualização da tabela carregada:"),
        html.Div(id="dataframe-table"),  # Componente que vai receber a tabela
        html.Br(),
        dbc.Button("Recarregar Tabela", id="btn-reload-table", color="primary", n_clicks=0),
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

# Callback para atualizar o conteúdo principal conforme a URL
@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/" or pathname == "/home":
        return home_content()
    elif pathname == "/central":
        return central.layout()
    elif pathname == "/okrs":
        return okrs_content()
    elif pathname == "/dataframe":
        return dataframe_layout()
    elif pathname == "/insights":
        return insights_content()
    elif pathname == "/querygpt":
        return querygpt_content()
    else:
        return html.Div([
            html.H1("404: Página não encontrada", style={"color": "red"}),
            html.P(f"O caminho {pathname} não existe."),
        ])

# Callback para lidar com carregamento de CSV ou BigQuery
@app.callback(
    Output("stored-data", "data"),
    [
        Input("btn-load-bq", "n_clicks"),
        Input("btn-load-csv", "n_clicks")
    ],
    [
        State("bq-project", "value"),
        State("bq-dataset", "value"),
        State("bq-table", "value"),
        State("bq-json", "contents"),
        State("upload-csv", "contents"),
        State("upload-csv", "filename"),
    ],
    prevent_initial_call=True,
)
def handle_uploads(n_clicks_bq, n_clicks_csv, project, dataset, table, json_contents, csv_contents, csv_filename):
    if not ctx.triggered:
        return no_update
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if triggered_id == "btn-load-csv":
        if csv_contents is None:
            return no_update
        content_type, content_string = csv_contents.split(',')
        decoded = base64.b64decode(content_string)
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        return df.to_json(date_format='iso', orient='split')

    elif triggered_id == "btn-load-bq":
        if None in (project, dataset, table, json_contents):
            return no_update
        df = carregar_tabela_bigquery(project, dataset, table, json_contents.encode())
        return df.to_json(date_format='iso', orient='split')

    return no_update

# Callback para atualizar a tabela DataFrame na página /dataframe
@app.callback(
    Output("data-table", "data"),
    Output("data-table", "columns"),
    Input("stored-data", "data"),
)
def update_table(data_json):
    if data_json is None:
        return [], []

    df = pd.read_json(data_json, orient='split')
    data = df.to_dict("records")
    columns = [{"name": i, "id": i} for i in df.columns]
    return data, columns

# Registra os callbacks do módulo Central
central.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)

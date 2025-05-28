from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from modules import central

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

app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,
])

@app.callback(
    Output("output-msg", "children"),
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
        State("upload-csv", "filename")
    ],
    prevent_initial_call=True
)
def load_data(bq_clicks, csv_clicks,
               project_id, dataset_id, table_id, json_contents,
               csv_contents, csv_filename):
    trigger = ctx.triggered_id
    if trigger == "btn-load-bq":
        if not all([project_id, dataset_id, table_id, json_contents]):
            return dbc.Alert("Preencha todos os campos e envie o JSON!", color="danger")
        try:
            import base64
            content_string = json_contents.split(",")[1]
            chave_json_bytes = base64.b64decode(content_string)

            df = carregar_tabela_bigquery(project_id, dataset_id, table_id, chave_json_bytes)
            salvar_dataframe(df, f"{project_id}_{dataset_id}_{table_id}")
            return dbc.Alert("Tabela carregada e salva com sucesso!", color="success")
        except Exception as e:
            return dbc.Alert(f"Erro: {e}", color="danger")

    elif trigger == "btn-load-csv":
        if csv_contents is None:
            return dbc.Alert("Nenhum arquivo CSV enviado!", color="warning")
        try:
            import io, base64
            content_string = csv_contents.split(",")[1]
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

            if "data" in df.columns:
                df["data"] = pd.to_datetime(df["data"])

            salvar_dataframe(df, csv_filename.replace(".csv", ""))
            return dbc.Alert("CSV carregado e salvo com sucesso!", color="success")
        except Exception as e:
            return dbc.Alert(f"Erro ao processar CSV: {e}", color="danger")

    return dbc.Alert("Nenhuma ação realizada.", color="secondary")


# Registrar callbacks do módulo central
central.register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)

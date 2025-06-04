from dash import html, dcc, dash_table, Input, Output, State, callback_context as ctx
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
import json
from google.cloud import bigquery
from google.oauth2 import service_account
from dash.exceptions import PreventUpdate
from modules.schema_utils import get_table_schema, classify_columns
from modules.bigquery_utils import get_bigquery_client
from modules.resumo_data import resumo_estatistico_engordado

def layout():
    return html.Div([
        dcc.Store(id="upload-store", storage_type="session"),
        dcc.Store(id="bq-form-visible", data=False, storage_type="session"),
        dcc.Store(id="sf-form-visible", data=False, storage_type="session"),
        dcc.Store(id="stored-data", storage_type="session"),
        dcc.Store(id="stored-grid", storage_type="session"),
        dcc.Store(id="stored-resumo", storage_type="session"),

        html.H3(
            "Upload e Integração de Dados",
            style={
                "fontFamily": "Arial, sans-serif",
                "fontSize": "34px",
                "fontWeight": "bold",
                "marginBottom": "20px"
            }
        ),

        # Cards de upload/conexão
        html.Div([
            # Card CSV
            html.Div([
                html.Div([
                    html.H5("CSV", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "marginBottom": "20px"}),
                    html.P("Envie seu arquivo CSV para extrair o melhor dos seus dados e obter insights automáticos.", style={"fontSize": "13px", "marginBottom": "20px"}),
                    dcc.Upload(
                        id="upload-data",
                        children=html.Button("Selecionar arquivo CSV", className="pill-btn"),
                        multiple=False,
                        style={"marginTop": "10px"}
                    ),
                ], style={"flex": "1"}),
                html.Img(
                    src="/assets/csv.png",
                    style={"width": "40px", "marginLeft": "16px", "alignSelf": "flex-start"}
                ),
            ], style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "flex-start"
            }, className="minimal-card"),

            # Card BigQuery
            html.Div([
                html.Div([
                    html.H5("BigQuery", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "marginBottom": "20px"}),
                    html.P("Insira suas credenciais do Big Query para gerar insights sem esforço.", style={"fontSize": "13px", "marginBottom": "20px"}),
                    html.Button("Conectar BigQuery", id="connect-bq-btn", n_clicks=0, className="pill-btn"),
                ], style={"flex": "1"}),
                html.Img(
                    src="/assets/bigquery.png",
                    style={"width": "40px", "marginLeft": "16px", "alignSelf": "flex-start"}
                ),
            ], style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "flex-start"
            }, className="minimal-card"),

            # Card Snowflake
            html.Div([
                html.Div([
                    html.H5("Snowflake", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold", "marginBottom": "20px"}),
                    html.P("Insira suas credenciais do Snowflake para desbloquear o poder dos dados.", style={"fontSize": "13px", "marginBottom": "20px"}),
                    html.Button("Conectar Snowflake", id="connect-sf-btn", n_clicks=0, className="pill-btn"),
                ], style={"flex": "1"}),
                html.Img(
                    src="/assets/snowflake.png",
                    style={"width": "40px", "marginLeft": "16px", "alignSelf": "flex-start"}
                ),
            ], style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "flex-start"
            }, className="minimal-card"),
        ], style={"display": "flex", "gap": "20px", "marginBottom": "20px"}),

        # Formulário BigQuery (inicialmente escondido)
        html.Div(
            id="bq-connection-form",
            children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Credenciais BigQuery", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold"}),
                        dcc.Input(id="bq-project-id", placeholder="Project ID", type="text", style={"marginBottom": "10px", "width": "100%"}),
                        dcc.Input(id="bq-dataset", placeholder="Dataset", type="text", style={"marginBottom": "10px", "width": "100%"}),
                        dcc.Input(id="bq-table", placeholder="Tabela", type="text", style={"marginBottom": "10px", "width": "100%"}),
                        dcc.Textarea(id="bq-json-key", placeholder="Chave JSON", style={"marginBottom": "10px", "width": "100%"}),
                        html.Button("Conectar", id="bq-connect-final-btn", n_clicks=0, className="pill-btn"),
                        html.Div(id="bq-connection-feedback", style={"marginTop": "10px"})
                    ])
                ], style={"marginTop": "20px", "backgroundColor": "#222", "color": "white"}),
            ],
            style={"display": "none"}
        ),

        # Formulário Snowflake (inicialmente escondido)
        html.Div(
            id="sf-connection-form",
            children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Credenciais Snowflake", style={"fontFamily": "Arial, sans-serif", "fontWeight": "bold"}),
                        dcc.Input(id="sf-user", placeholder="Usuário", type="text", style={"marginBottom": "10px", "width": "100%"}),
                        dcc.Input(id="sf-password", placeholder="Senha", type="password", style={"marginBottom": "10px", "width": "100%"}),
                        dcc.Input(id="sf-account", placeholder="Account", type="text", style={"marginBottom": "10px", "width": "100%"}),
                        dcc.Input(id="sf-database", placeholder="Database", type="text", style={"marginBottom": "10px", "width": "100%"}),
                        dcc.Input(id="sf-schema", placeholder="Schema", type="text", style={"marginBottom": "10px", "width": "100%"}),
                        dcc.Input(id="sf-warehouse", placeholder="Warehouse", type="text", style={"marginBottom": "10px", "width": "100%"}),
                        html.Button("Conectar", id="sf-connect-final-btn", n_clicks=0, className="pill-btn"),
                        html.Div(id="sf-connection-feedback", style={"marginTop": "10px"})
                    ])
                ], style={"marginTop": "20px", "backgroundColor": "#222", "color": "white"}),
            ],
            style={"display": "none"}
        ),

        # Card da Tabela de Dados (AgGrid)
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊 Tabela de Dados", style={"marginBottom": "10px", "fontFamily": "Arial, sans-serif", "fontWeight": "bold"}),
                    dcc.Loading(
                        id="aggrid-container",
                        type="default",
                        children=[
                            html.Div(id="aggrid-container")
                        ]
                    ),
                ])
            ], className="big-card", style={"marginBottom": "24px"}),
        ]),

        # Card do Resumo Estatístico
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📈 Resumo Estatístico", style={"marginBottom": "10px", "fontFamily": "Arial, sans-serif", "fontWeight": "bold"}),
                    html.Pre(id="resumo-estatistico", style={"whiteSpace": "pre-wrap", "color": "white"}),
                ])
            ], className="big-card"),
        ]),
    ])

# Função para classificar colunas de um DataFrame
def classify_columns_from_df(df):
    classified = {
        "numerical": [],
        "temporal": [],
        "categorical": [],
        "boolean": [],
        "others": []
    }
    for col in df.columns:
        dtype = df[col].dtype
        if pd.api.types.is_numeric_dtype(dtype):
            classified["numerical"].append(col)
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            classified["temporal"].append(col)
        elif pd.api.types.is_bool_dtype(dtype):
            classified["boolean"].append(col)
        elif pd.api.types.is_object_dtype(dtype):
            classified["categorical"].append(col)
        else:
            classified["others"].append(col)
    return classified

# Função para renderizar o resumo estatístico
def render_resumo_estatistico(resumo_dict):
    if not resumo_dict:
        return html.Div("Nenhum resumo disponível.")
    rows = []
    for col, stats in resumo_dict.items():
        base = {
            "Coluna": col,
            "Tipo": stats.get("tipo", ""),
            "Count": stats.get("count", "")
        }
        if stats["tipo"] == "numérica":
            base.update({
                "Média": round(stats.get("mean", 0), 2),
                "Mediana": round(stats.get("median", 0), 2),
                "Mínimo": round(stats.get("min", 0), 2),
                "Máximo": round(stats.get("max", 0), 2),
                "Desvio Padrão": round(stats.get("std", 0), 2),
                "Assimetria": round(stats.get("skewness", 0), 2) if stats.get("skewness") is not None else "",
                "Curtose": round(stats.get("kurtosis", 0), 2) if stats.get("kurtosis") is not None else "",
            })
        elif stats["tipo"] == "categórica":
            base.update({
                "Top Categoria": stats.get("top", ""),
                "Frequência Top": stats.get("freq_top", ""),
                "Nº Categorias": stats.get("num_categories", "")
            })
        elif stats["tipo"] == "texto":
            base.update({
                "Únicos": stats.get("unique", ""),
                "Tamanho Médio": round(stats.get("avg_length", 0), 2),
                "Tamanho Máx": stats.get("max_length", "")
            })
        rows.append(base)
    colunas = [{"name": k, "id": k} for k in rows[0].keys()]
    return html.Div(
        children=[
            dash_table.DataTable(
                columns=colunas,
                data=rows,
                style_table={"overflowX": "auto"},
                style_header={
                    "backgroundColor": "#333",
                    "color": "white",
                    "fontWeight": "bold",
                    "border": "1px solid white"
                },
                style_cell={
                    "textAlign": "left",
                    "backgroundColor": "#333333",
                    "color": "white",
                    "border": "1px solid #444",
                    "whiteSpace": "normal",
                    "fontFamily": "Courier New, monospace",
                    "fontWeight": "light",
                    "fontSize": "14px"
                },
                style_data_conditional=[],
                page_size=10
            )
        ],
        style={
            "backgroundColor": "#333333",
            "padding": "24px",
            "borderRadius": "16px",
            "marginTop": "16px"
        }
    )

# Callbacks para mostrar/ocultar formulários
def register_callbacks(app, pg_engine=None):
    @app.callback(
        Output("bq-connection-form", "style"),
        Input("connect-bq-btn", "n_clicks"),
        State("bq-connection-form", "style"),
        prevent_initial_call=True
    )
    def toggle_bq_form(n_clicks, current_style):
        if n_clicks:
            if current_style and current_style.get("display") == "block":
                return {"display": "none"}
            return {"display": "block"}
        return current_style or {"display": "none"}

    @app.callback(
        Output("sf-connection-form", "style"),
        Input("connect-sf-btn", "n_clicks"),
        State("sf-connection-form", "style"),
        prevent_initial_call=True
    )
    def toggle_sf_form(n_clicks, current_style):
        if n_clicks:
            if current_style and current_style.get("display") == "block":
                return {"display": "none"}
            return {"display": "block"}
        return current_style or {"display": "none"}

    # Callback principal para dados
    @app.callback(
        Output("aggrid-container", "children"),
        Output("resumo-estatistico", "children"),
        Output("bq-connection-feedback", "children"),
        Output("stored-data", "data"),
        Output("stored-grid", "data"),
        Output("stored-resumo", "data"),
        Output("upload-store", "data"),
        Input("stored-data", "data"),
        Input("upload-data", "contents"),
        Input("bq-connect-final-btn", "n_clicks"),
        Input("connect-sf-btn", "n_clicks"),
        Input("url", "pathname"),
        State("upload-data", "filename"),
        State("bq-project-id", "value"),
        State("bq-dataset", "value"),
        State("bq-table", "value"),
        State("bq-json-key", "value"),
        State("stored-grid", "data"),
        State("stored-resumo", "data"),
        prevent_initial_call=True,
        allow_missing=True
    )
    def unified_data_handler(
        stored_data, upload_contents, bq_n_clicks, sf_n_clicks, pathname,
        filename, bq_project, bq_dataset, bq_table, bq_json_key,
        stored_grid, stored_resumo
    ):
        triggered_id = ctx.triggered_id

        if pathname != "/upload":
            raise PreventUpdate

        # Defaults
        table_component = html.Div("Nenhum dado carregado ainda.")
        resumo = "Nenhum dado carregado ainda."
        feedback = ""
        json_data = None
        grid_data = None
        resumo_data = None

        # Restauração de sessão ao navegar para /upload
        if triggered_id == "url" and pathname == "/upload":
            if stored_grid and stored_resumo and stored_grid.get("rowData") and stored_grid.get("columnDefs"):
                table_component = html.Div(
                    children=[
                        dash_table.DataTable(
                            columns=[{"name": col["headerName"], "id": col["field"]} for col in stored_grid["columnDefs"]],
                            data=stored_grid["rowData"],
                            style_table={"overflowX": "auto"},
                            style_header={
                                "backgroundColor": "#333",
                                "color": "white",
                                "fontWeight": "bold",
                                "border": "1px solid white"
                            },
                            style_cell={
                                "textAlign": "left",
                                "backgroundColor": "#333333",
                                "color": "white",
                                "border": "1px solid #444",
                                "whiteSpace": "normal",
                                "fontFamily": "Courier New, monospace",
                                "fontWeight": "light",
                                "fontSize": "14px"
                            },
                            style_data_conditional=[],
                            page_size=10
                        )
                    ],
                    style={
                        "backgroundColor": "#333333",
                        "padding": "24px",
                        "borderRadius": "16px",
                        "marginTop": "16px"
                    }
                )
                return table_component, stored_resumo, "", None, stored_grid, stored_resumo, None
            return table_component, "", "", None, stored_grid, stored_resumo, None

        # Upload CSV
        if triggered_id == "upload-data" and upload_contents:
            try:
                content_type, content_string = upload_contents.split(',')
                decoded = base64.b64decode(content_string)
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                row_data = df.to_dict("records")
                column_defs = [{"headerName": col, "field": col} for col in df.columns]
                tipos = classify_columns_from_df(df)
                resumo_dict = resumo_estatistico_engordado(df, tipos)
                resumo = render_resumo_estatistico(resumo_dict)
                feedback = "Arquivo CSV carregado com sucesso!"
                json_data = df.to_json(date_format="iso", orient="split")
                grid_data = {"rowData": row_data, "columnDefs": column_defs}
                resumo_data = resumo
                table_component = html.Div(
                    children=[
                        dash_table.DataTable(
                            columns=[{"name": col["headerName"], "id": col["field"]} for col in column_defs],
                            data=row_data,
                            style_table={"overflowX": "auto"},
                            style_header={
                                "backgroundColor": "#333",
                                "color": "white",
                                "fontWeight": "bold",
                                "border": "1px solid white"
                            },
                            style_cell={
                                "textAlign": "left",
                                "backgroundColor": "#333333",
                                "color": "white",
                                "border": "1px solid #444",
                                "whiteSpace": "normal",
                                "fontFamily": "Courier New, monospace",
                                "fontWeight": "light",
                                "fontSize": "14px"
                            },
                            style_data_conditional=[],
                            page_size=10
                        )
                    ],
                    style={
                        "backgroundColor": "#333333",
                        "padding": "24px",
                        "borderRadius": "16px",
                        "marginTop": "16px"
                    }
                )
            except Exception as e:
                resumo = f"Erro ao processar CSV: {str(e)}"
                feedback = ""
                table_component = html.Div("Nenhum dado carregado ainda.")
            return table_component, resumo, feedback, json_data, grid_data, resumo_data, None

        # BigQuery
        if triggered_id == "bq-connect-final-btn" and bq_n_clicks and bq_n_clicks > 0:
            try:
                if not bq_json_key:
                    raise ValueError("Chave JSON do BigQuery não pode estar vazia.")
                credentials_info = json.loads(bq_json_key)
                credentials = service_account.Credentials.from_service_account_info(credentials_info)
                client = bigquery.Client(credentials=credentials, project=bq_project)
                query = f"SELECT * FROM `{bq_project}.{bq_dataset}.{bq_table}` LIMIT 1000"
                df = client.query(query).to_dataframe()
                row_data = df.to_dict("records")
                column_defs = [{"headerName": col, "field": col} for col in df.columns]
                tipos = classify_columns_from_df(df)
                resumo_dict = resumo_estatistico_engordado(df, tipos)
                resumo = render_resumo_estatistico(resumo_dict)
                schema_info = get_table_schema(client, bq_project, bq_dataset, bq_table)
                tipos = classify_columns(schema_info)
                feedback = dbc.Alert("Conectado ao BigQuery com sucesso!", color="success")
                json_data = df.to_json(date_format="iso", orient="split")
                grid_data = {"rowData": row_data, "columnDefs": column_defs}
                resumo_data = resumo
                table_component = html.Div(
                    children=[
                        dash_table.DataTable(
                            columns=[{"name": col["headerName"], "id": col["field"]} for col in column_defs],
                            data=row_data,
                            style_table={"overflowX": "auto"},
                            style_header={
                                "backgroundColor": "#333",
                                "color": "white",
                                "fontWeight": "bold",
                                "border": "1px solid white"
                            },
                            style_cell={
                                "textAlign": "left",
                                "backgroundColor": "#333333",
                                "color": "white",
                                "border": "1px solid #444",
                                "whiteSpace": "normal",
                                "fontFamily": "Courier New, monospace",
                                "fontWeight": "light",
                                "fontSize": "14px"
                            },
                            style_data_conditional=[],
                            page_size=10
                        )
                    ],
                    style={
                        "backgroundColor": "#333333",
                        "padding": "24px",
                        "borderRadius": "16px",
                        "marginTop": "16px"
                    }
                )
            except Exception as e:
                resumo = f"Erro ao conectar ao BigQuery: {str(e)}"
                feedback = dbc.Alert(f"Erro: {str(e)}", color="danger")
                table_component = html.Div("Nenhum dado carregado ainda.")
            return table_component, resumo, feedback, json_data, grid_data, resumo_data, None

        # Snowflake (placeholder)
        if triggered_id == "connect-sf-btn" and sf_n_clicks and sf_n_clicks > 0:
            resumo = "Conexão ao Snowflake: Em construção!"
            feedback = ""
            table_component = html.Div(
                children=[
                    dash_table.DataTable(
                        columns=[{"name": col["headerName"], "id": col["field"]} for col in column_defs],
                        data=row_data,
                        style_table={"overflowX": "auto"},
                        style_header={
                            "backgroundColor": "#333",
                            "color": "white",
                            "fontWeight": "bold",
                            "border": "1px solid white"
                        },
                        style_cell={
                            "textAlign": "left",
                            "backgroundColor": "#333333",
                            "color": "white",
                            "border": "1px solid #444",
                            "whiteSpace": "normal",
                            "fontFamily": "Courier New, monospace",
                            "fontWeight": "light",
                            "fontSize": "14px"
                        },
                        style_data_conditional=[],
                        page_size=10
                    )
                ],
                style={
                    "backgroundColor": "#333333",
                    "padding": "24px",
                    "borderRadius": "16px",
                    "marginTop": "16px"
                }
            )
            return table_component, resumo, feedback, None, stored_grid, stored_resumo, None

        # Fallback
        return html.Div("Nenhum dado carregado ainda."), "", "", None, None, None, None
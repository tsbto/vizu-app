from dash import html, dcc, Input, Output, State, dash_table
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io

def layout():
    return html.Div([
        html.H3("📁 Upload e Integração de Dados", style={"marginBottom": "20px"}),

        # Cards de conexão (Upload, BigQuery, Snowflake)
        html.Div([
            html.Div([
                html.H5("Upload CSV"),
                html.P("Envie seus dados em CSV para integração.",),
                dcc.Upload(
                    id="upload-data",
                    children=html.Button("Selecionar arquivo CSV", className="pill-btn"),
                    multiple=False,
                    style={"marginTop": "10px"}
                ),
            ], className="minimal-card"),

            html.Div([
                html.H5("BigQuery"),
                html.P("Conecte-se ao BigQuery para buscar dados."),
                html.Button("Conectar BigQuery", id="connect-bq-btn", n_clicks=0, className="pill-btn"),
            ], className="minimal-card"),

            html.Div([
                html.H5("Snowflake"),
                html.P("Conecte-se ao Snowflake para buscar dados."),
                html.Button("Conectar Snowflake", id="connect-sf-btn", n_clicks=0, className="pill-btn"),
            ], className="minimal-card"),
        ], style={"display": "flex", "gap": "20px", "marginBottom": "20px"}),

        # Card grandão para preview e resumo estatístico
        html.Div([
            html.H4("📊 Tabela de Dados", style={"marginBottom": "10px"}),
            dag.AgGrid(
                id="ag-grid-preview",
                columnSize="sizeToFit",
                defaultColDef={"editable": True, "resizable": True},
                style={"height": "300px", "width": "100%", "color": "black"},
            ),
            html.H4("📈 Resumo Estatístico", style={"marginTop": "20px"}),
            html.Pre(id="resumo-estatistico", style={"whiteSpace": "pre-wrap", "color": "white"})
        ], className="big-card"),
    ], style={"padding": "20px", "color": "white"})

def register_callbacks(app, pg_engine):

    @app.callback(
        Output("ag-grid-preview", "rowData"),
        Output("ag-grid-preview", "columnDefs"),
        Output("resumo-estatistico", "children"),
        Input("upload-data", "contents"),
        State("upload-data", "filename"),
        prevent_initial_call=True
    )
    def update_output(contents, filename):
        if contents:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            # AG Grid data
            row_data = df.to_dict("records")
            column_defs = [{"headerName": col, "field": col} for col in df.columns]

            # Resumo estatístico
            resumo = df.describe().to_string()

            return row_data, column_defs, resumo
        return [], [], "Nenhum arquivo carregado ainda."

    # Botões de conexão: só um placeholder por enquanto
    @app.callback(
        Output("resumo-estatistico", "children", allow_duplicate=True),
        Input("connect-bq-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def connect_bigquery(n_clicks):
        return "Conexão ao BigQuery: Em construção!"

    @app.callback(
        Output("resumo-estatistico", "children", allow_duplicate=True),
        Input("connect-sf-btn", "n_clicks"),
        prevent_initial_call=True
    )
    def connect_snowflake(n_clicks):
        return "Conexão ao Snowflake: Em construção!"

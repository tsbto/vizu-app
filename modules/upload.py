import base64
import io
import pandas as pd
from dash import html, dcc, Input, Output, State, callback, dash_table
import dash_bootstrap_components as dbc

# Layout da página
layout = html.Div([
    html.H3("Importar CSV e conectar BigQuery", style={"marginBottom": "20px"}),
    
    dbc.Row([
        dbc.Col([
            dcc.Upload(
                id='upload-csv',
                children=html.Div([
                    'Arraste e solte ou ',
                    html.A('selecione um arquivo CSV')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'marginBottom': '10px',
                    'color': '#fff',
                    'backgroundColor': '#333',
                },
                multiple=False
            ),
            html.Div(id='output-csv-upload', style={"color": "white", "marginTop": "10px"}),
            html.Div(id='csv-table-container', style={"marginTop": "20px"}),
            html.Div(id='summary-table-container', style={"marginTop": "20px"}),
        ], width=6),

        dbc.Col([
            html.H5("Configurações BigQuery", style={"marginBottom": "10px"}),
            dbc.Input(id="bq-project", placeholder="Projeto BigQuery", type="text", style={"marginBottom": "10px"}),
            dbc.Input(id="bq-dataset", placeholder="Dataset", type="text", style={"marginBottom": "10px"}),
            dbc.Input(id="bq-table", placeholder="Nome da tabela", type="text", style={"marginBottom": "10px"}),
            dbc.Textarea(id="bq-json", placeholder="Credenciais JSON (cole aqui)", style={"height": "150px", "color": "#000"}),
            dbc.Button("Enviar para BigQuery", id="btn-send-bq", color="primary", n_clicks=0),
            html.Div(id="output-bq-status", style={"color": "white", "marginTop": "10px"}),
        ], width=6)
    ])
], style={"padding": "20px", "color": "white"})


def register_callbacks(app, pg_engine):
    @app.callback(
        [Output('output-csv-upload', 'children'),
         Output('csv-table-container', 'children'),
         Output('summary-table-container', 'children')],
        Input('upload-csv', 'contents'),
        State('upload-csv', 'filename'),
        prevent_initial_call=True
    )
    def parse_csv(contents, filename):
        if contents is None:
            return "", "", ""
        if pg_engine is not None:
            df.to_sql("nome_da_tabela", pg_engine, if_exists="replace", index=False)

        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            
            # Salvar no Postgres
            df.to_sql('dados_upload', con=pg_engine, if_exists='replace', index=False)
            
            # Resumo estatístico
            summary = df.describe().reset_index()

            info = html.Div([
                html.P(f'Arquivo "{filename}" carregado e salvo no Postgres com sucesso!'),
                html.P(f'Total de linhas: {len(df)}'),
                html.P(f'Colunas: {", ".join(df.columns)}'),
            ])
            
            # Tabela com dados do CSV
            table = dash_table.DataTable(
                data=df.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in df.columns],
                page_size=10,
                style_table={'overflowX': 'auto', 'backgroundColor': '#333', 'color': '#fff'},
                style_cell={
                    'backgroundColor': '#333',
                    'color': 'white',
                    'textAlign': 'left',
                    'minWidth': '100px', 'width': '150px', 'maxWidth': '200px',
                    'whiteSpace': 'normal'
                },
                style_header={
                    'backgroundColor': '#444',
                    'fontWeight': 'bold'
                }
            )

            # Tabela com resumo estatístico
            summary_table = dash_table.DataTable(
                data=summary.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in summary.columns],
                style_table={'overflowX': 'auto', 'backgroundColor': '#333', 'color': '#fff'},
                style_cell={
                    'backgroundColor': '#333',
                    'color': 'white',
                    'textAlign': 'left',
                    'minWidth': '100px', 'width': '150px', 'maxWidth': '200px',
                    'whiteSpace': 'normal'
                },
                style_header={
                    'backgroundColor': '#555',
                    'fontWeight': 'bold'
                }
            )

            return info, table, summary_table

        except Exception as e:
            return html.Div([
                'Erro ao processar o arquivo CSV.',
                html.Pre(str(e))
            ], style={"color": "red"}), "", ""

    @app.callback(
        Output('output-bq-status', 'children'),
        Input('btn-send-bq', 'n_clicks'),
        State('upload-csv', 'contents'),
        State('bq-project', 'value'),
        State('bq-dataset', 'value'),
        State('bq-table', 'value'),
        State('bq-json', 'value'),
        prevent_initial_call=True
    )
    def send_to_bigquery(n_clicks, contents, project, dataset, table, json_creds):
        if n_clicks == 0:
            return ""
        if not all([contents, project, dataset, table, json_creds]):
            return "Por favor, preencha todos os campos e faça upload do CSV."

        try:
            import json
            from google.cloud import bigquery
            from google.oauth2 import service_account

            # Decodificar CSV
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            # Credenciais BigQuery
            creds_dict = json.loads(json_creds)
            credentials = service_account.Credentials.from_service_account_info(creds_dict)

            client = bigquery.Client(credentials=credentials, project=project)

            table_id = f"{project}.{dataset}.{table}"
            job = client.load_table_from_dataframe(df, table_id)
            job.result()  # espera carregar

            return f"Dados enviados para BigQuery na tabela {table_id} com sucesso!"

        except Exception as e:
            return f"Erro ao enviar para BigQuery: {str(e)}"

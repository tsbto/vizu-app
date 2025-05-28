from dash import html, dash_table, Input, Output, State, callback_context as ctx
import dash_bootstrap_components as dbc
import pandas as pd
import base64
import io
import json

def layout():
    return html.Div([
        html.H2("Data Frame", style={"fontWeight": "bold", "fontFamily": "Arial, sans-serif"}),
        html.P("Aqui está a visualização da tabela carregada:"),
        
        # Inputs básicos para carregar dados (exemplo)
        dbc.Input(id="bq-project", placeholder="BigQuery Project", type="text", style={"marginBottom": "10px"}),
        dbc.Input(id="bq-dataset", placeholder="BigQuery Dataset", type="text", style={"marginBottom": "10px"}),
        dbc.Input(id="bq-table", placeholder="BigQuery Table", type="text", style={"marginBottom": "10px"}),
        dcc.Upload(
            id="upload-csv",
            children=html.Div([
                "Arraste e solte ou ",
                html.A("selecione um arquivo CSV")
            ]),
            style={
                "width": "100%", "height": "60px", "lineHeight": "60px",
                "borderWidth": "1px", "borderStyle": "dashed", "borderRadius": "5px",
                "textAlign": "center", "marginBottom": "10px"
            },
            multiple=False
        ),
        
        dbc.Button("Carregar do BigQuery", id="btn-load-bq", color="primary", n_clicks=0, style={"marginRight": "10px"}),
        dbc.Button("Carregar CSV", id="btn-load-csv", color="secondary", n_clicks=0),
        
        html.Br(), html.Br(),
        
        html.Div(id="output-msg", style={"color": "red", "fontWeight": "bold"}),
        
        html.Div(id="dataframe-table"),
        html.Br(),
        dbc.Button("Recarregar Tabela", id="btn-reload-table", color="success", n_clicks=0),
    ])


def register_callbacks(app):
    @app.callback(
        [Output("output-msg", "children"), Output("stored-data", "data")],
        [Input("btn-load-bq", "n_clicks"), Input("btn-load-csv", "n_clicks")],
        [
            State("bq-project", "value"),
            State("bq-dataset", "value"),
            State("bq-table", "value"),
            State("upload-csv", "contents"),
            State("upload-csv", "filename"),
        ],
        prevent_initial_call=True
    )
    def carregar_dados(btn_load_bq, btn_load_csv, bq_project, bq_dataset, bq_table, csv_contents, csv_filename):
        trigger = ctx.triggered_id
        if trigger == "btn-load-bq":
            # Aqui você insere a lógica para carregar dados do BigQuery (exemplo simples)
            # Por enquanto, só mockamos um df:
            if not (bq_project and bq_dataset and bq_table):
                return "Informe project, dataset e tabela do BQ.", None
            
            # Simulação de df (substituir por chamada real do BigQuery)
            df = pd.DataFrame({
                "Coluna1": [1, 2, 3],
                "Coluna2": ["A", "B", "C"]
            })
            
            return f"Dados carregados do BigQuery {bq_project}.{bq_dataset}.{bq_table}", df.to_json(date_format='iso', orient='split')
        
        elif trigger == "btn-load-csv":
            if csv_contents is None:
                return "Nenhum arquivo CSV carregado.", None
            
            content_type, content_string = csv_contents.split(',')
            decoded = base64.b64decode(content_string)
            try:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            except Exception as e:
                return f"Erro ao ler CSV: {str(e)}", None
            
            return f"Arquivo CSV '{csv_filename}' carregado com sucesso.", df.to_json(date_format='iso', orient='split')
        
        return "Nenhuma ação detectada.", None

    @app.callback(
        Output("dataframe-table", "children"),
        [Input("stored-data", "data"), Input("btn-reload-table", "n_clicks")],
        prevent_initial_call=True
    )
    def renderizar_tabela(stored_data, n_clicks):
        if stored_data is None:
            return html.P("Nenhum dado carregado ainda.", style={"color": "red"})
        try:
            df = pd.read_json(stored_data, orient='split')
        except Exception as e:
            return html.P(f"Erro ao carregar dados: {str(e)}", style={"color": "red"})
        
        table = dash_table.DataTable(
            data=df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in df.columns],
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left", "color": "black", "backgroundColor": "white"},
            style_header={"backgroundColor": "#1a1a1a", "color": "white", "fontWeight": "bold"},
        )
        return table

from dash import Input, Output, State
import pandas as pd

def register_callbacks(app):

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
            State("upload-csv", "filename")
        ],
        prevent_initial_call=True
    )
    def load_data(bq_clicks, csv_clicks, project, dataset, table, bq_json, csv_contents, csv_filename):
        # lógica para carregar dataframe de BQ ou CSV
        # no exemplo abaixo, só um dataframe dummy
        df = pd.DataFrame({"col1": [1,2,3], "col2": ["a","b","c"]})
        return df.to_json(orient='split')

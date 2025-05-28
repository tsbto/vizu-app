from google.cloud import bigquery
import pandas as pd
import tempfile

def carregar_tabela_bigquery(project_id, dataset_id, table_id, chave_json_bytes):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(chave_json_bytes)
        caminho_cred = tmp.name

    client = bigquery.Client.from_service_account_json(caminho_cred, project=project_id)
    tabela_full = f"{project_id}.{dataset_id}.{table_id}"
    query = f"SELECT * FROM `{tabela_full}`"

    df = client.query(query).to_dataframe()
    return df

def salvar_dataframe(df: pd.DataFrame, nome_arquivo: str):
    caminho = f"./data/{nome_arquivo}.csv"
    df.to_csv(caminho, index=False)

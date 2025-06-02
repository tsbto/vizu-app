from google.cloud import bigquery
from google.oauth2 import service_account

def get_bigquery_client(path_to_key_json):
    """
    Cria e retorna um cliente BigQuery autenticado.
    """
    credentials = service_account.Credentials.from_service_account_file(path_to_key_json)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    return client

def get_resumo_estatistico(project_id, dataset_id, table_id, cols, path_to_key_json):
    """
    Gera um resumo estatístico simples (média, desvio padrão, min, max, mediana) para colunas numéricas da tabela.
    
    Args:
        project_id (str): ID do projeto GCP.
        dataset_id (str): Nome do dataset.
        table_id (str): Nome da tabela.
        cols (list of str): Lista com nomes das colunas numéricas para resumir.
        path_to_key_json (str): Caminho para a chave JSON do service account.

    Returns:
        dict: dicionário com os valores calculados para cada estatística e coluna.
    """
    client = get_bigquery_client(path_to_key_json)

    col_agg = []
    for col in cols:
        col_agg.append(f"AVG({col}) AS avg_{col}")
        col_agg.append(f"STDDEV({col}) AS stddev_{col}")
        col_agg.append(f"MIN({col}) AS min_{col}")
        col_agg.append(f"MAX({col}) AS max_{col}")
        # Mediana aproximada usando APPROX_QUANTILES
        col_agg.append(f"APPROX_QUANTILES({col}, 2)[OFFSET(1)] AS median_{col}")

    query = f"""
        SELECT {', '.join(col_agg)}
        FROM `{project_id}.{dataset_id}.{table_id}`
    """

    try:
        query_job = client.query(query)
        results = query_job.result()
        row = list(results)[0]

        resumo = {k: v for k, v in row.items()}
        return resumo

    except Exception as e:
        print(f"Erro ao gerar resumo estatístico: {e}")
        return None

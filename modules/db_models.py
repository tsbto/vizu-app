# modules/db_models.py

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, MetaData, Table
from modules.db import get_engine

metadata = MetaData()

tabela_resumos = Table(
    "resumos_estatisticos",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome_tabela", String),
    Column("resumo_json", JSON),
    Column("criado_em", DateTime)
)

def criar_tabelas():
    engine = get_engine()
    metadata.create_all(engine)

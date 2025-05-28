# modules/db.py

from sqlalchemy import create_engine

def get_engine():
    # Ajuste a URL de conexão conforme seu ambiente
    url = "postgresql://vizu:vizu@localhost:5432/vizu"
    engine = create_engine(url, echo=True)
    return engine

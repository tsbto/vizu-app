import pandas as pd
import numpy as np
from collections import Counter
from scipy.stats import skew, kurtosis

def resumo_estatistico_engordado(df, tipos_colunas):
    resumo = {}

    # Numéricas
    for col in tipos_colunas.get("numerical", []):
        s = df[col].dropna()
        quartis = s.quantile([0.25, 0.5, 0.75]).to_dict()
        resumo[col] = {
            "tipo": "numérica",
            "count": s.count(),
            "mean": s.mean(),
            "std": s.std(),
            "min": s.min(),
            "max": s.max(),
            "median": s.median(),
            "Q1": quartis.get(0.25),
            "Q2": quartis.get(0.5),
            "Q3": quartis.get(0.75),
            "skewness": skew(s) if len(s) > 2 else None,
            "kurtosis": kurtosis(s) if len(s) > 3 else None,
        }

    # Categóricas
    for col in tipos_colunas.get("categorical", []):
        s = df[col].dropna()
        contagem = s.value_counts()
        resumo[col] = {
            "tipo": "categórica",
            "count": s.count(),
            "num_categories": contagem.size,
            "top": contagem.idxmax() if not contagem.empty else None,
            "freq_top": contagem.max() if not contagem.empty else None,
            "frequencies": contagem.head(5).to_dict(),
        }

    # Textuais
    for col in tipos_colunas.get("text", []):
        s = df[col].dropna()
        comprimento = s.apply(lambda x: len(str(x)))
        resumo[col] = {
            "tipo": "texto",
            "count": s.count(),
            "unique": s.nunique(),
            "avg_length": comprimento.mean(),
            "max_length": comprimento.max(),
        }

    return resumo

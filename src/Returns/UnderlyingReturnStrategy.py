import pandas as pd

"""
    Yahoo fournit deux colonnes de prix pour une même action ou un même ETF :
    - Close : le prix de clôture, sans les dividendes
    - Adj Close : le prix ajusté, qui inclut les dividendes réinvestis

    Les classes filles indiquent la colonne à utiliser avec l'attribut `column`.
"""

class UnderlyingReturnStrategy:
    column: str = None

    def select(self, df: pd.DataFrame) -> pd.Series:
        """Renvoie la série des prix de la colonne choisie (self.column), sans valeurs manquantes """
        if self.column not in df.columns:
            raise KeyError(f"Colonne '{self.column}' absente. Colonnes : {list(df.columns)}")
        return df[self.column].dropna().astype(float)

class WithoutDividends(UnderlyingReturnStrategy):
    """Prix du sous-jacent sans les dividendes versés (colonne Close de Yahoo)."""
    column = "Close"


class WithDividends(UnderlyingReturnStrategy):
    """Prix du sous-jacent avec les dividendes réinvestis (colonne Adj Close de Yahoo)."""
    column = "Adj Close"
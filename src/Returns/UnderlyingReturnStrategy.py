"""Rendements du sous-jacent (avec ou sans dividendes) et rendement du cash."""
import pandas as pd
from src.Config.Config import IndexParams


class UnderlyingReturnStrategy:
    """Classe mère : choisit la série de prix du sous-jacent dans le DataFrame Yahoo."""
    column: str = None

    def select(self, df: pd.DataFrame) -> pd.Series:
        if self.column not in df.columns:
            raise KeyError(f"Colonne '{self.column}' absente. Colonnes : {list(df.columns)}")
        return df[self.column].dropna().astype(float)

class PriceOnlyReturns(UnderlyingReturnStrategy):
    """Sous-jacent en Price Return : dividendes exclus."""
    column = "Close"


class TotalReturnReturns(UnderlyingReturnStrategy):
    """Sous-jacent en Total Return : dividendes réinvestis (Adj Close)."""
    column = "Adj Close"
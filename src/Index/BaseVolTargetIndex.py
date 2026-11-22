from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from src.Config.Config import IndexParams

TRADING_DAYS = 252


class BaseVolTargetIndex(ABC):
    """Commun à tous les indices : exposition E(t), rendement du sous-jacent rU(t), niveau base 100.

    Les classes filles ne définissent que le facteur multiplicatif journalier.
    """
    BASE_LEVEL = 100.0

    def __init__(self, params: IndexParams, exposure: pd.Series, underlying_returns: pd.Series):
        if not exposure.index.equals(underlying_returns.index):
            raise ValueError("exposure et underlying_returns doivent avoir le même index de dates")
        self.params, self.E, self.rU = params, exposure, underlying_returns

    @abstractmethod
    def daily_factor(self) -> pd.Series:
        """Facteur multiplicatif du jour : Index(t) = Index(t-1) x facteur(t)."""

    def compute(self) -> pd.Series:
        """Niveau de l'indice. Base 100 la veille du premier jour où le facteur est calculable."""
        factor = self.daily_factor()
        first = factor.first_valid_index()
        if first is None:
            raise ValueError("Historique insuffisant : aucun facteur journalier calculable")
        valid = factor.loc[first:]
        if valid.isna().any():
            raise ValueError("Valeurs manquantes après le démarrage de l'indice")
        levels = self.BASE_LEVEL * valid.cumprod()
        pos = factor.index.get_loc(first)
        if pos > 0:                                    # point de départ (base 100)
            levels = pd.concat([pd.Series(self.BASE_LEVEL, index=[factor.index[pos - 1]]), levels])
        return levels.rename(self.params.name)

    def summary(self) -> dict:
        """Quelques statistiques pour contrôler que l'indice se comporte comme prévu."""
        lv = self.compute()
        ret = lv.pct_change().dropna()
        years = len(ret) / TRADING_DAYS
        return {
            "annual_return": (lv.iloc[-1] / lv.iloc[0]) ** (1 / years) - 1,
            "realized_vol": ret.std() * np.sqrt(TRADING_DAYS),
            "target_vol": self.params.vol_target,
            "max_drawdown": (lv / lv.cummax() - 1).min(),
            "avg_exposure": self.E.dropna().mean(),
        }



from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from src.Config.IndexParams import IndexParams

TRADING_DAYS = 252


class BaseVolTargetIndex(ABC):
    """Commun à tous les indices : reçoit la série de l'exposition au sous-jacent E(t)
    et la série du rendement du sous-jacent rU(t).

    Calcule la valeur de l'indice à partir du facteur journalier, que les classes filles définissent.
    """

    BASE_LEVEL = 100.0   #valeur de départ de l'indice 

    def __init__(self, params: IndexParams, exposure: pd.Series, underlying_returns: pd.Series):
        if not exposure.index.equals(underlying_returns.index):
            raise ValueError("exposure et underlying_returns doivent avoir le même index de dates")
        self.params, self.E, self.rU = params, exposure, underlying_returns

    @abstractmethod
    def daily_factor(self) -> pd.Series:
        """Renvoie une série du facteur journalier : Index(t) = Index(t-1) x facteur(t)."""

    def compute(self) -> pd.Series:
        """Renvoie la série de la valeur de l'indice pour chaque jour"""
        """ Indice démarre à BASE_LEVEL, la veille du premier jour où le facteur journalier est calculable."""

        factor = self.daily_factor()
        first = factor.first_valid_index()   # date de la première valeur qui n'est pas NaN
        if first is None:
            raise ValueError("Historique insuffisant : aucun facteur journalier calculable")
        valid = factor.loc[first:]
        if valid.isna().any():
            raise ValueError("Valeurs manquantes après le démarrage de l'indice")
        levels = self.BASE_LEVEL * valid.cumprod()
        pos = factor.index.get_loc(first)
        if pos > 0:                                    
            levels = pd.concat([pd.Series(self.BASE_LEVEL, index=[factor.index[pos - 1]]), levels])
        return levels.rename(self.params.name)



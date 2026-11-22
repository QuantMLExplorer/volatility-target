import numpy as np 
import pandas as pd 
import warnings
from src.Config.IndexParams import IndexParams

class ReturnsCalculator:

    def __init__(self, prices: pd.Series, params: IndexParams, cash_rate: pd.Series = None):
        if not prices.index.is_monotonic_increasing:
            warnings.warn("Les prix n'étaient pas triés par date : tri appliqué")
            prices = prices.sort_index()
        if prices.index.has_duplicates:
            raise ValueError("L'index des prix contient des dates en double")
        if params.uses_cash : 
            if cash_rate is None:
                raise ValueError(f"{params.name}: un taux de cash '{params.cash_rate}' est requis")
            if not cash_rate.index.is_monotonic_increasing:
                warnings.warn("Les taux du cash n'étaient pas triés par date : tri appliqué")
                cash_rate = cash_rate.sort_index()
            if cash_rate.index.has_duplicates:
                raise ValueError("L'index du taux de cash contient des dates en double")
        self.prices, self.params, self.cash_rate = prices, params, cash_rate

    def log_returns(self) -> pd.Series:
        """Renvoie la série du rendement logarithmique du sous-jacent : ln(S(t) / S(t-1))"""
        return np.log(self.prices / self.prices.shift(1)).rename("log_r")

    def underlying_returns(self) -> pd.Series:
        """Renvoie la série du rendement du sous-jacent : rU(t) = S(t) / S(t-1) - 1."""
        return self.prices.pct_change().rename("rU")

    def cash_returns(self) -> pd.Series:
        """Renvoie la série du rendement du cash : rC(t) = r(t-1) x d(t,t-1) / DayCount """
        """"
        r(t-1) : taux annuel de la date de calcul précédente
        d(t,t-1) : nombre de jours calendaires entre t-1 et t
        DayCount : nombre de jours dans l'année pour ce taux (360 ou 365)
        """
        if not self.params.uses_cash:
            raise ValueError(f"{self.params.name}: cet indice n'utilise pas de cash")
        idx = self.prices.index

        rate = self.cash_rate.reindex(idx, method="ffill")     # dernier taux connu à chaque date de calcul
        d = idx.to_series().diff().dt.days                     # jours calendaires entre t-1 et t
        return (rate.shift(1) * d / self.params.day_count).rename("rC")

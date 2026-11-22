import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
from src.Config.Config import IndexParams

TRADING_DAYS = 252


class VolatilityEstimator:
    """Estime sigma_S, sigma_L et sigma_MAX à partir des rendements log."""

    def __init__(self, params: IndexParams):
        self.params = params

    @staticmethod
    def weights(lam: float, K: int) -> np.ndarray:
        """Poids normalisés, du plus ANCIEN au plus RÉCENT : w[-1] est le jour le plus récent."""
        if lam == 1:                                   # cas limite : moyenne simple
            return np.full(K, 1 / K)
        w = (1 - lam) * lam ** np.arange(K - 1, -1, -1)      # [K-1, K-2, ..., 1, 0]
        return w / w.sum()                                   

    def _ewma_vol(self, log_returns: pd.Series, lam: float) -> pd.Series:
        K = self.params.K
        r2 = (log_returns ** 2).to_numpy(dtype=float)  # pas de soustraction de la moyenne
        out = np.full(len(r2), np.nan)
        if len(r2) >= K:
            windows = sliding_window_view(r2, K)       # chaque ligne : fenêtre de K jours consécutifs, décalés d'un jour à chaque ligne
            variance = windows @ self.weights(lam, K)
            out[K - 1:] = np.sqrt(TRADING_DAYS * variance)
        return pd.Series(out, index=log_returns.index)

    def sigma_short(self, log_returns: pd.Series) -> pd.Series:
        return self._ewma_vol(log_returns, self.params.lam_S).rename("sigma_S")

    def sigma_long(self, log_returns: pd.Series) -> pd.Series:
        return self._ewma_vol(log_returns, self.params.lam_L).rename("sigma_L")

    def sigma_max(self, log_returns: pd.Series) -> pd.Series:
        """Plus grande des deux estimations sur les T derniers jours"""
        both = pd.concat([self.sigma_short(log_returns), self.sigma_long(log_returns)], axis=1)
        return both.max(axis=1, skipna=False).rolling(self.params.T).max().rename("sigma_max")

import numpy as np
import pandas as pd
from numpy.lib.stride_tricks import sliding_window_view
from src.Config.IndexParams import IndexParams
from src.VolatilityEstimator.BaseVolatilityEstimator import BaseVolatilityEstimator

TRADING_DAYS = 252


class EwmaMaxVolatilityEstimator(BaseVolatilityEstimator):
    """Calcule les séries de volatilité à partir de la série des rendements logarithmiques.

    σ(t) = sqrt(252 × Σ_{k=t-K+1..t} α(t-k+1) × r(k)² / Σ_{k=1..K} α(k)),  r(k) = ln(S(k)/S(k-1))
    α(k) = (1-λ) × λ^(k-1),  avec λ = λS pour σS et λ = λL pour σL (λS < λL ≤ 1)
    σMAX(t) = max_{i=0..T-1} max(σS(t-i), σL(t-i))
    """

    @staticmethod
    def weights(lam: float, K: int) -> np.ndarray:
        """Renvoie les K poids exponentiels normalisés, du plus ancien au plus récent (w[-1] = jour le plus récent)."""
        if lam == 1:      # lam = 1, les poids sont égaux : moyenne simple"""                              
            return np.full(K, 1 / K)
        w = (1 - lam) * lam ** np.arange(K - 1, -1, -1)      # [K-1, K-2, ..., 1, 0]
        return w / w.sum()                                   

    def _ewma_vol(self, log_returns: pd.Series, lam: float, name: str) -> pd.Series:
        """Renvoie la série de la volatilité annualisée, calculée avec une moyenne mobile exponentielle de facteur lam."""
        K = self.params.K
        r2 = (log_returns ** 2).to_numpy(dtype=float)  # pas de soustraction de la moyenne
        out = np.full(len(r2), np.nan)
        if len(r2) >= K:
            windows = sliding_window_view(r2, K)       # chaque ligne : fenêtre de K jours consécutifs, décalés d'un jour à chaque ligne
            variance = windows @ self.weights(lam, K)
            out[K - 1:] = np.sqrt(TRADING_DAYS * variance)
        return pd.Series(out, index=log_returns.index, name=name)


    def compute(self, log_returns: pd.Series) -> pd.Series:
        """Renvoie la série σMAX : max glissant sur T jours de max(σS, σL), NaN tant que σS ou σL n'est pas défini """
        p = self.params
        both = pd.concat(
            [self._ewma_vol(log_returns, p.lam_S, "sigma_S"),
            self._ewma_vol(log_returns, p.lam_L, "sigma_L")],
            axis=1,
        )
        return both.max(axis=1, skipna=False).rolling(p.T).max().rename("sigma_max")

import numpy as np
import pandas as pd

from src.Exposure.VolatilityEstimator import VolatilityEstimator

"""Ce test s'assure que σMAX(t) est le max sur les T derniers jours de max(σS, σL)."""

def test_sigma_max_is_rolling_max_of_both_volatilities(params):
    K, T = params.K, params.T
    idx = pd.bdate_range("2022-01-03", periods=K + T )
    returns = pd.Series(np.random.default_rng(0).normal(0, 0.01, len(idx)), index=idx)

    est = VolatilityEstimator(params)
    sigma_S = est._ewma_vol(returns, params.lam_S, "sigma_S").to_numpy()
    sigma_L = est._ewma_vol(returns, params.lam_L, "sigma_L").to_numpy()
    sigma_max = est.sigma_max(returns)

    first = K - 1 + T - 1                      # première date où les T dernières valeurs sont définies
    assert sigma_max.iloc[:first].isna().all()

    for t in range(first, len(returns)):       # formule écrite telle quelle : max sur i = 0..T-1
        attendu = max(max(sigma_S[t - i], sigma_L[t - i]) for i in range(T))
        assert np.isclose(sigma_max.iloc[t], attendu)
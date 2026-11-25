import numpy as np
import pandas as pd

from src.VolatilityEstimator.EwmaMaxVolatilityEstimator import EwmaMaxVolatilityEstimator

"""Ce test s'assure que σMAX est NaN dès que σS ou σL est NaN (skipna=False)."""

def test_sigma_max_is_nan_when_one_volatility_is_nan(params):
    T = params.T
    idx = pd.bdate_range("2022-01-03", periods=100)
    returns = pd.Series(0.0, index=idx)
    k0 = 50                                        # position où σS est NaN, σL est définie

    def fake_ewma_vol(log_returns, lam, name):
        if lam == params.lam_S:
            valeurs = np.full(len(log_returns), 0.2)
            valeurs[k0] = np.nan
        else:
            valeurs = np.full(len(log_returns), 0.1)
        return pd.Series(valeurs, index=log_returns.index, name=name)

    est = EwmaMaxVolatilityEstimator(params)
    est._ewma_vol = fake_ewma_vol                  # remplace le calcul par des séries connues

    sigma_max = est.compute(returns)

    assert sigma_max.iloc[k0:k0 + T].isna().all()  # toute fenêtre de T jours contenant k0 est NaN
    assert sigma_max.iloc[k0 - 1] == 0.2           # avant : max(0.2, 0.1)
    assert sigma_max.iloc[k0 + T] == 0.2           # après : la fenêtre ne contient plus k0
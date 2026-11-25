import numpy as np
import pandas as pd

from src.VolatilityEstimator.EwmaMaxVolatilityEstimator import EwmaMaxVolatilityEstimator


"""Ce test s'assure que σMAX réagit immédiatement à un pic de volatilité,
reste élevé pendant T jours, puis redescend quand le pic sort de la fenêtre.
"""

def test_sigma_max_reacts_immediately_then_decays_after_t_days(params):
    T = params.T
    idx = pd.bdate_range("2022-01-03", periods=100)
    returns = pd.Series(0.0, index=idx)
    k0 = 50                                        # jour du choc : σS bondit pendant un seul jour

    def fake_ewma_vol(log_returns, lam, name):
        if lam == params.lam_S:
            valeurs = np.full(len(log_returns), 0.1)
            valeurs[k0] = 0.5                      # choc de volatilité court terme
        else:
            valeurs = np.full(len(log_returns), 0.12)
        return pd.Series(valeurs, index=log_returns.index, name=name)

    est = EwmaMaxVolatilityEstimator(params)
    est._ewma_vol = fake_ewma_vol

    sigma_max = est.compute(returns)

    assert sigma_max.iloc[k0 - 1] == 0.12          # avant le choc : max(σS, σL) = σL
    assert (sigma_max.iloc[k0:k0 + T] == 0.5).all()  # réaction immédiate, maintenue T jours
    assert sigma_max.iloc[k0 + T] == 0.12          # le choc sort de la fenêtre de T jours
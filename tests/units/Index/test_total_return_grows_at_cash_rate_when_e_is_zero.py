import numpy as np
import pandas as pd

from src.Index.CashAwareIndex.TotalReturnIndex import TotalReturnIndex

"""Ce test s'assure que, avec E = 0, total_return croît uniquement au taux du cash,
quel que soit le rendement du sous-jacent.
"""

def test_total_return_grows_at_cash_rate_when_e_is_zero(params):
    n = 100
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2022-01-03", periods=n)
    exposure = pd.Series(0.0, index=idx)                               # E = 0 : tout est placé en cash
    underlying_returns = pd.Series(rng.normal(0, 0.05, n), index=idx)  # sous-jacent très volatil, sans effet
    cash_returns = pd.Series(rng.uniform(0.0001, 0.0004, n), index=idx)  # rC strictement positif

    total = TotalReturnIndex(params, exposure, underlying_returns, cash_returns).compute()

    attendu = TotalReturnIndex.BASE_LEVEL * (1 + cash_returns).cumprod()   

    assert len(total) == n
    np.testing.assert_allclose(total, attendu)
    assert total.is_monotonic_increasing                                   # le cash rapporte toujours quelque chose
import numpy as np
import pandas as pd

from src.Index.CashAwareIndex.ExcessReturnIndex import ExcessReturnIndex

"""Ce test s'assure que, avec E = 1, excess_return évolue chaque jour du rendement
du sous-jacent moins celui du cash : facteur = 1 + (rU - rC).
"""

def test_excess_return_is_underlying_minus_cash_when_e_is_one(params):
    n = 100
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2022-01-03", periods=n)
    exposure = pd.Series(1.0, index=idx)                                 # E = 1 : tout est investi dans le sous-jacent
    underlying_returns = pd.Series(rng.normal(0, 0.01, n), index=idx)
    cash_returns = pd.Series(rng.uniform(0.0001, 0.0004, n), index=idx)  # rC strictement positif

    excess = ExcessReturnIndex(params, exposure, underlying_returns, cash_returns).compute()

    attendu = ExcessReturnIndex.BASE_LEVEL * (1 + underlying_returns - cash_returns).cumprod()   

    assert len(excess) == n
    np.testing.assert_allclose(excess, attendu)
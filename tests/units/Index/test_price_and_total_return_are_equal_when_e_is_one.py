import numpy as np
import pandas as pd

from src.Index.PriceReturnIndex import PriceReturnIndex
from src.Index.CashAwareIndex.TotalReturnIndex import TotalReturnIndex

"""Ce test s'assure que, avec E = 1, price_return et total_return donnent exactement
la même série, quel que soit le rendement du cash (rien n'est placé en cash).
"""

def test_price_and_total_return_are_equal_when_e_is_one(params):
    n = 100
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2022-01-03", periods=n)
    exposure = pd.Series(1.0, index=idx)                          # E = 1 : tout est investi dans le sous-jacent
    underlying_returns = pd.Series(rng.normal(0, 0.01, n), index=idx)
    cash_returns = pd.Series(rng.uniform(0.0001, 0.0004, n), index=idx)   # rC strictement positif sans effet car 1 - E = 0

    price = PriceReturnIndex(params, exposure, underlying_returns).compute()
    total = TotalReturnIndex(params, exposure, underlying_returns, cash_returns).compute()

    attendu = PriceReturnIndex.BASE_LEVEL * (1 + underlying_returns).cumprod()   

    np.testing.assert_allclose(price, attendu)
    np.testing.assert_allclose(total, attendu)
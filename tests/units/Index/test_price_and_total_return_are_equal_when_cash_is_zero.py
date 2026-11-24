import numpy as np
import pandas as pd

from src.Index.PriceReturnIndex import PriceReturnIndex
from src.Index.CashAwareIndex.TotalReturnIndex import TotalReturnIndex

"""Ce test s'assure que, avec un rendement du cash nul, price_return et total_return
donnent exactement la même série, quelle que soit l'exposition E(t).
"""
def test_price_and_total_return_are_equal_when_cash_is_zero(params):
    n = 100
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2022-01-03", periods=n)
    exposure = pd.Series(rng.uniform(0.1, 1.5, n), index=idx)     # E variable, strictement positif
    underlying_returns = pd.Series(rng.normal(0, 0.01, n), index=idx)
    cash_returns = pd.Series(0.0, index=idx)                      # rC = 0 : la part (1 - E) ne rapporte rien

    price = PriceReturnIndex(params, exposure, underlying_returns).compute()
    total = TotalReturnIndex(params, exposure, underlying_returns, cash_returns).compute()

    attendu = PriceReturnIndex.BASE_LEVEL * (1 + exposure * underlying_returns).cumprod()  

    assert (exposure > 0).all()
    np.testing.assert_allclose(price, attendu)
    np.testing.assert_allclose(total, attendu)
import numpy as np
import pandas as pd

from src.Index.PriceReturnIndex import PriceReturnIndex

"""Ce test s'assure que, avec E = 0, price_return reste constant à BASE_LEVEL,
quel que soit le rendement du sous-jacent.
"""

def test_price_return_is_constant_when_e_is_zero(params):
    n = 100
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2022-01-03", periods=n)
    exposure = pd.Series(0.0, index=idx)                          # E = 0 : rien n'est investi dans le sous-jacent
    underlying_returns = pd.Series(rng.normal(0, 0.01, n), index=idx)

    price = PriceReturnIndex(params, exposure, underlying_returns).compute()

    assert len(price) == n
    np.testing.assert_allclose(price, PriceReturnIndex.BASE_LEVEL)
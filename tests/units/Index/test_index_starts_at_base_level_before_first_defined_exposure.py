import numpy as np
import pandas as pd

from src.Index.PriceReturnIndex import PriceReturnIndex

"""Ce test s'assure que l'indice démarre à BASE_LEVEL la veille de la première date
où E est défini, et qu'aucun NaN n'est propagé ensuite.
"""

def test_index_starts_at_base_level_before_first_defined_exposure(params):
    n, m = 100, 30                                                 # E est NaN sur les m premières dates
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2022-01-03", periods=n)
    exposure = pd.Series(np.nan, index=idx)
    exposure.iloc[m:] = rng.uniform(0.1, 1.5, n - m)               # E défini à partir de la position m
    underlying_returns = pd.Series(rng.normal(0, 0.01, n), index=idx)

    price = PriceReturnIndex(params, exposure, underlying_returns).compute()

    assert price.index[0] == idx[m - 1]                            # la série démarre la veille de la première date de E
    assert price.iloc[0] == PriceReturnIndex.BASE_LEVEL            # à la valeur de base
    assert len(price) == n - m + 1                                 # base + une valeur par facteur défini
    assert price.notna().all()                                     # aucun NaN propagé

    attendu = PriceReturnIndex.BASE_LEVEL * (1 + exposure.iloc[m:] * underlying_returns.iloc[m:]).cumprod()
    np.testing.assert_allclose(price.iloc[1:], attendu)            
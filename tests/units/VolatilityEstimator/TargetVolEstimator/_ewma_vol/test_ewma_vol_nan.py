import numpy as np
import pandas as pd
import pytest

from src.Config.IndexParams import IndexParams
from src.VolatilityEstimator.EwmaMaxVolatilityEstimator import EwmaMaxVolatilityEstimator

"""Ce test s'assure que les K-1 premières valeurs de la volatilité sont NaN et que les suivantes sont définies.
"""

def test_ewma_vol_first_k_minus_1_values_are_nan(params):
    K = params.K
    idx = pd.bdate_range("2022-01-03", periods=K + 50)
    returns = pd.Series(np.random.default_rng(0).normal(0, 0.01, len(idx)), index=idx)

    sigma = EwmaMaxVolatilityEstimator(params)._ewma_vol(returns, 0.94, "sigma")

    assert sigma.iloc[:K - 1].isna().all()      # les K-1 premières valeurs sont NaN
    assert sigma.iloc[K - 1:].notna().all()     # ensuite la volatilité est définie
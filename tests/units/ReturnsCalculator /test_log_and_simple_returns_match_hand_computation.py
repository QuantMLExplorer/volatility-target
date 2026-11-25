import numpy as np
import pandas as pd
from dataclasses import replace

from src.Returns.ReturnsCalculator import ReturnsCalculator

"""Ce test s'assure que le rendement log vaut ln(S(k)/S(k-1)) et que le rendement simple
vaut S(k)/S(k-1) - 1, sur un petit exemple calculé à la main.
"""
def test_log_and_simple_returns_match_hand_computation(params):
    params_sans_cash = replace(params, index_type="price_return", cash_rate=None, day_count=None)
    idx = pd.bdate_range("2022-01-03", periods=4)
    prices = pd.Series([100.0, 110.0, 99.0, 99.0], index=idx)

    calc = ReturnsCalculator(prices, params_sans_cash)

    # S(k)/S(k-1) = 1.1, 0.9, 1 ; le premier rendement est NaN (pas de S(-1))
    attendu_simple = [np.nan, 0.1, -0.1, 0.0]
    attendu_log = [np.nan, 0.0953102, -0.1053605, 0.0]          # ln(1.1), ln(0.9), ln(1) calculés à la main

    np.testing.assert_allclose(calc.underlying_returns(), attendu_simple, atol=1e-12)
    np.testing.assert_allclose(calc.log_returns(), attendu_log, atol=1e-6)
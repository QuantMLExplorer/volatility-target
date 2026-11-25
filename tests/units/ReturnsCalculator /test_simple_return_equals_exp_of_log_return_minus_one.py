import numpy as np
import pandas as pd
from dataclasses import replace

from src.Returns.ReturnsCalculator import ReturnsCalculator

"""Ce test s'assure repose sur l'égalité : 
        exp(ln(x)) - 1 = x - 1
 log vaut ln(S(k)/S(k-1)) et que le rendement simple
vaut S(k)/S(k-1) - 1, sur un petit exemple calculé à la main.
"""
def test_simple_return_equals_exp_of_log_return_minus_one(params):
    params_sans_cash = replace(params, index_type="price_return", cash_rate=None, day_count=None)
    idx = pd.bdate_range("2022-01-03", periods=200)

    r = np.random.default_rng(0).normal(0, 0.01, 200)       # [r(1), ..., r(200)] : rendements aléatoires
    c = r.cumsum()                                          # [r(1), r(1)+r(2), ..., r(1)+...+r(200)] = [c(1), ..., c(200)]
    prices = pd.Series(np.exp(c), index=idx)          # [exp(c(1)), ..., exp(c(200))] : prix strictement positifs

    calc = ReturnsCalculator(prices, params_sans_cash)

    #   ln( S(k) / S(k-1) ) = ln( exp(c(k)) / exp(c(k-1)) )     
    #                       = ln( exp(c(k) - c(k-1)) )
    #                       = c(k) - c(k-1)
    #                       = r(k)
    # np.exp(log_returns)  : exp(r(k)) = S(k)/S(k-1)
    # exp(r(k)) - 1        : S(k)/S(k-1) - 1 = rendement simple, calculé par underlying_returns()
    np.testing.assert_allclose(np.exp(calc.log_returns()) - 1, calc.underlying_returns())
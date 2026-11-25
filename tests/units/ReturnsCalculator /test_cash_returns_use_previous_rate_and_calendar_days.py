import numpy as np
import pandas as pd

from src.Returns.ReturnsCalculator import ReturnsCalculator


"""Ce test s'assure que rC(t) = r(t-1) × d(t,t-1) / DayCount : le taux appliqué est celui
de la veille, et les jours calendaires comptent le week-end (3 jours pour un lundi).
"""

def test_cash_returns_use_previous_rate_and_calendar_days(params):
    idx = pd.DatetimeIndex(["2026-11-19", "2026-11-20", "2026-11-23", "2026-11-24"])   # jeu, ven, lun, mar
    prices = pd.Series(100.0, index=idx)                          # les prix n'interviennent pas dans rC
    cash_rate = pd.Series([0.01, 0.02, 0.03, 0.04], index=idx)    # un taux différent par jour, pour repérer le jour utilisé

    rC = ReturnsCalculator(prices, params, cash_rate).cash_returns()

    D = params.day_count                                          
    attendu = [
        np.nan,                # jeudi 19 : pas de veille, donc pas de rendement
        0.01 * 1 / D,          # vendredi 20 : taux de jeudi (0.01), 1 jour calendaire
        0.02 * 3 / D,          # lundi 23 : taux de vendredi (0.02), 3 jours (20 → 23 novembre, week-end inclus)
        0.03 * 1 / D,          # mardi 24 : taux de lundi (0.03), 1 jour
    ]
    np.testing.assert_allclose(rC, attendu)
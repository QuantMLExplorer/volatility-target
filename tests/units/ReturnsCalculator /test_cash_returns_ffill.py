import numpy as np
import pandas as pd

from src.Returns.ReturnsCalculator import ReturnsCalculator

"""Ce test s'assure que, quand le taux de cash d'une date est absent, c'est le dernier taux
connu qui est reporté (ffill) : le lundi utilise le taux de jeudi si celui de vendredi manque.
"""

def test_cash_returns_carry_forward_last_known_rate(params):
    idx = pd.DatetimeIndex(["2026-11-19", "2026-11-20", "2026-11-23", "2026-11-24"])   # jeu, ven, lun, mar
    prices = pd.Series(100.0, index=idx)
    # le taux du vendredi 20 est absent (jour sans publication) : seules 3 dates sur 4 ont un taux
    cash_rate = pd.Series([0.01, 0.03, 0.04],
                          index=pd.DatetimeIndex(["2026-11-19", "2026-11-23", "2026-11-24"]))

    rC = ReturnsCalculator(prices, params, cash_rate).cash_returns()

    D = params.day_count
    attendu = [
        np.nan,                # jeudi 19 : pas de veille, donc pas de rendement
        0.01 * 1 / D,          # vendredi 20 : taux de jeudi (0.01), 1 jour calendaire
        0.01 * 3 / D,          # lundi 23 : le taux de vendredi est absent, on reporte celui de jeudi (0.01), 3 jours
        0.03 * 1 / D,          # mardi 24 : taux de lundi (0.03), 1 jour
    ]
    np.testing.assert_allclose(rC, attendu)
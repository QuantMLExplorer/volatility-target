import numpy as np
import pandas as pd

from src.Exposure.ExposureModel import ExposureModel

"""Ce test s'assure que, avec des rendements de volatilité connue, E(t) est constante
et vaut la valeur théorique min(LM, vol_target / (c × √252)).
"""

def test_exposure_constant_returns_matches_theoretical_value(params):
    n = params.K + 100
    c = 0.02                                                   # rendement quotidien de ±2 %
    idx = pd.bdate_range("2022-01-03", periods=n)
    returns = pd.Series(c * np.where(np.arange(n) % 2 == 0, 1, -1), index=idx)

    E = ExposureModel(params).compute(returns)

    sigma = c * np.sqrt(252)                                   # σS = σL = σMAX, car r² = c² à chaque jour  # ≈ 0,3175 
    attendu = min(params.LM, params.vol_target / sigma)     
    premiere_valeur = params.K - 1 + params.T - 1 + params.d   # fenêtres K et T, puis décalage d
    # vol_target = 0.12 # LM = 1 
    assert attendu < params.LM                        # vol_target / sigma  ≈  0,12 / 0,3175 ≈ 0,378  
    assert E.iloc[:premiere_valeur].isna().all()     # test aussi que E est NaN pendant les premières lignes (fenêtre K, T et décalage d)
    assert np.allclose(E.iloc[premiere_valeur:], attendu)
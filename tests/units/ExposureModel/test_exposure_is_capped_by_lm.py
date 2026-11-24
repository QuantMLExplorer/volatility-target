import numpy as np
import pandas as pd

from src.Exposure.ExposureModel import ExposureModel

"""Ce test s'assure que : 

    -  l'exposition E(t) ne dépasse jamais LM là où elle est définie.
    - E(t) vaut LM quand la volatilité est faible,
    - E(t) est strictement inférieure à LM quand la volatilité est forte.
"""

def test_exposure_is_capped_by_lm(params):
    n = params.K + 200
    mid = n // 2
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2022-01-03", periods=n)
    #  Premier régime : régime calme avec une volatilité faible : sigma_annualise = 0.002*√252 ≈3 %  => E = LM
    # Deuxième régime : régime agitée avec une volatilite forte :  sigma_annualise = 0.02*√252≈32 % => E = vol_target / sigma_max
    valeurs = np.concatenate([rng.normal(0, 0.002, n // 2), rng.normal(0, 0.02, n - n // 2)])
    returns = pd.Series(valeurs, index=idx)

    E = ExposureModel(params).compute(returns)

    premiere_valeur = params.K - 1 + params.T - 1 + params.d     # fenêtres K et T, puis décalage d
    marge = 30                                                   # jours laissés à la volatilité pour monter

    assert E.iloc[:premiere_valeur].isna().all()
    assert (E.dropna() <= params.LM).all()          # E <= LM
    assert (E.iloc[premiere_valeur:mid] == params.LM).all()          # régime calme : plafond actif
    assert (E.iloc[mid + params.d + marge:] < params.LM).all()       # régime agité : plafond inactif

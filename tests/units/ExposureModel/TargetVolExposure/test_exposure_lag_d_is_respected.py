import numpy as np
import pandas as pd

from src.Exposure.TargetVolExposure import TargetVolExposure

"""Ce test s'assure que le décalage d est respecté : modifier un rendement au jour k0
ne change pas E avant k0 + d, mais change E(k0 + d).
"""

def test_exposure_lag_d_is_respected(params):
    premiere_valeur = params.K - 1 + params.T - 1 + params.d   # fenêtres K et T, puis décalage d
    k0 = premiere_valeur + 50                                   # jour du choc, 50 jours après le début de E
    n = k0 + params.d + 100
    rng = np.random.default_rng(0)
    idx = pd.bdate_range("2022-01-03", periods=n)
    base = pd.Series(rng.normal(0, 0.02, n), index=idx)         # régime où E < LM, donc E réagit à σMAX

    choc = base.copy()
    choc.iloc[k0] = 0.2                                         # rendement extrême : σMAX bondit dès k0

    model = TargetVolExposure(params) 
    E_base = model.compute(base)
    E_choc = model.compute(choc)

    d = params.d
    np.testing.assert_allclose(E_choc.iloc[:k0 + d], E_base.iloc[:k0 + d])   # rien ne change avant k0 + d
    assert E_choc.iloc[k0 + d] < E_base.iloc[k0 + d]                         # E réagit exactement à k0 + d
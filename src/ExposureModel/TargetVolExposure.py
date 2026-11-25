# src/Exposure/TargetVolExposure.py
import numpy as np
import pandas as pd
from src.Config.IndexParams import IndexParams
from src.Exposure.BaseExposureModel import BaseExposureModel
from src.VolatilityEstimator.BaseVolatilityEstimator import BaseVolatilityEstimator
from src.VolatilityEstimator.EwmaMaxVolatilityEstimator import EwmaMaxVolatilityEstimator


class TargetVolExposure(BaseExposureModel):
    """Calcule l'exposition E(t) de l'indice à partir des rendements logarithmiques.

    E(t) = min(LM, vol_target / σMAX(t-d))

    - LM : levier maximal
    - vol_target : volatilité cible
    - d : décalage en jours de calcul
    """

    def __init__(self, params: IndexParams, estimator: BaseVolatilityEstimator = None):
        super().__init__(params, estimator or EwmaMaxVolatilityEstimator(params))

    def compute(self, log_returns: pd.Series) -> pd.Series:
        """Renvoie la série E(t) = min(LM, vol_target / σMAX(t-d))."""
        sigma_max = self.estimator.compute(log_returns)
        lagged = sigma_max.shift(self.params.d)        # d en jours de calcul (lignes de la série)
        return np.minimum(self.params.LM, self.params.vol_target / lagged).rename("E")

    
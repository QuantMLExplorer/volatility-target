import numpy as np 
import pandas as pd 
from src.Config.IndexParams import IndexParams
from src.Exposure.VolatilityEstimator import VolatilityEstimator

class ExposureModel:
    """Calcule l'exposition E(t) de l'indice à partir des rendements logarithmiques.

    E(t) = min(LM, vol_target / σMAX(t-d))

    - LM : levier maximal
    - vol_target : volatilité cible
    - d : décalage en jours de calcul
    """

    def __init__(self, params: IndexParams, estimator: VolatilityEstimator = None):
        self.params = params
        self.estimator = estimator or VolatilityEstimator(params)

    def compute(self, log_returns: pd.Series) -> pd.Series:
        """Renvoie la série E(t) = min(LM, vol_target / σMAX(t-d))."""
        sigma_max = self.estimator.sigma_max(log_returns)
        lagged = sigma_max.shift(self.params.d)        # d en jours de calcul (lignes de la série)
        return np.minimum(self.params.LM, self.params.vol_target / lagged).rename("E")

    
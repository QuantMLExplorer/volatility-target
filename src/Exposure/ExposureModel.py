import numpy as np 
import pandas as pd 
from src.Config.Config import IndexParams
from src.Exposure.VolatilityEstimator import VolatilityEstimator

class ExposureModel:
    """E(t) = min(LM, vol_target / sigma_MAX(t-d))."""

    def __init__(self, params: IndexParams, estimator: VolatilityEstimator = None):
        self.params = params
        self.estimator = estimator or VolatilityEstimator(params)

    def compute(self, log_returns: pd.Series) -> pd.Series:
        sigma_max = self.estimator.sigma_max(log_returns)
        lagged = sigma_max.shift(self.params.d)        # d en jours de calcul (lignes de la série)
        return np.minimum(self.params.LM, self.params.vol_target / lagged).rename("E")

    
from abc import ABC, abstractmethod
import pandas as pd
from src.Config.IndexParams import IndexParams
from src.VolatilityEstimator.BaseVolatilityEstimator import BaseVolatilityEstimator


class BaseExposureModel(ABC):
    """Commun à tous les modèles d'exposition : reçoit les paramètres de l'indice et un estimateur
    de volatilité, et renvoie la série d'exposition E(t) au sous-jacent.
    """

    def __init__(self, params: IndexParams, estimator: BaseVolatilityEstimator):
        self.params = params
        self.estimator = estimator

    @abstractmethod
    def compute(self, log_returns: pd.Series) -> pd.Series:
        """Renvoie la série d'exposition E(t) à partir de la série de rendements."""
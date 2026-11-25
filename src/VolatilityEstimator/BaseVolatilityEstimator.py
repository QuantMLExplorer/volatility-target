from abc import ABC, abstractmethod
import pandas as pd
from src.Config.IndexParams import IndexParams

class BaseVolatilityEstimator(ABC):
    """Commun à tous les estimateurs : reçoit une série de rendements (de n'importe quel type)
    et renvoie la série de volatilité annualisée σ(t).
    """

    def __init__(self, params: IndexParams):
        self.params = params

    @abstractmethod
    def compute(self, returns: pd.Series) -> pd.Series:
        """Renvoie la série de volatilité annualisée σ(t) à partir de la série de rendements `returns`."""
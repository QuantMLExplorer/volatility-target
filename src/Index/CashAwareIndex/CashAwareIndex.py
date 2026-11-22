from abc import ABC
import pandas as pd
from src.Index.BaseVolTargetIndex import BaseVolTargetIndex

class CashAwareIndex(BaseVolTargetIndex, ABC):
    """Classe mère des indices qui utilisent le rendement du cash rC(t)."""
    def __init__(self, params, exposure, underlying_returns, cash_returns: pd.Series):
        super().__init__(params, exposure, underlying_returns)
        if not cash_returns.index.equals(exposure.index):
            raise ValueError("cash_returns doit avoir le même index de dates que exposure")
        self.rC = cash_returns
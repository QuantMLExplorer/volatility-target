from src.Index.BaseVolTargetIndex import BaseVolTargetIndex
from src.Index.PriceReturnIndex import PriceReturnIndex
from src.Index.CashAwareIndex.CashAwareIndex import CashAwareIndex
from src.Index.CashAwareIndex.TotalReturnIndex import TotalReturnIndex
from src.Index.CashAwareIndex.ExcessReturnIndex import ExcessReturnIndex

class IndexFactory:
    """Construit l'indice du bon type (Price Return, Total Return ou Excess Return) selon index_type du JSON."""
    
    _REGISTRY = {
        "price_return": PriceReturnIndex,
        "total_return": TotalReturnIndex,
        "excess_return": ExcessReturnIndex,
    }

    @classmethod
    def create(cls, params, exposure, underlying_returns, cash_returns=None) -> BaseVolTargetIndex:
        """Renvoie un objet indice (BaseVolTargetIndex) du type donné par params.index_type"""
        klass = cls._REGISTRY[params.index_type]
        if issubclass(klass, CashAwareIndex):
            if cash_returns is None:
                raise ValueError(f"{params.index_type} nécessite cash_returns")
            return klass(params, exposure, underlying_returns, cash_returns)
        return klass(params, exposure, underlying_returns)
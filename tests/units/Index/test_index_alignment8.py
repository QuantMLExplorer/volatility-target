import numpy as np
import pandas as pd
import pytest

from src.Index.PriceReturnIndex import PriceReturnIndex
from src.Index.CashAwareIndex.CashAwareIndex import CashAwareIndex
from src.Index.CashAwareIndex.TotalReturnIndex import TotalReturnIndex
from src.Index.CashAwareIndex.ExcessReturnIndex import ExcessReturnIndex

N = 50
IDX = pd.bdate_range("2022-01-03", periods=N)
MAL_ALIGNES = {
    "dates_decalees": pd.bdate_range("2022-01-04", periods=N),   # même longueur, décalées d'un jour
    "serie_plus_courte": IDX[:-1],                               # 49 dates
}

def serie(index, valeur=0.01):
    return pd.Series(valeur, index=index)



"""Ce test s'assure qu'un index de dates différent entre exposure et  underlying_returns est détecté à la construction (ValueError).
"""
@pytest.mark.parametrize("autre_index", MAL_ALIGNES.values(), ids=MAL_ALIGNES.keys())
@pytest.mark.parametrize("Index", [PriceReturnIndex, TotalReturnIndex, ExcessReturnIndex])
def test_misaligned_underlying_returns_is_detected(params, Index, autre_index):
    exposure = serie(IDX, 1.0)
    underlying_returns = serie(autre_index)                      # mal aligné : c'est la seule erreur
    cash = (serie(IDX, 0.0002),) if issubclass(Index, CashAwareIndex) else ()   # cash aligné, si l'indice en prend un

    with pytest.raises(ValueError, match="même index de dates"):
        Index(params, exposure, underlying_returns, *cash)
        

"""Ce test s'assure qu'un index de dates différent entre exposure et cash_returns est détecté à la construction (ValueError).
"""
@pytest.mark.parametrize("autre_index", MAL_ALIGNES.values(), ids=MAL_ALIGNES.keys())
@pytest.mark.parametrize("Index", [TotalReturnIndex, ExcessReturnIndex])
def test_misaligned_cash_returns_is_detected(params, Index, autre_index):
    exposure = serie(IDX, 1.0)
    underlying_returns = serie(IDX)                              # bien aligné sur exposure
    cash_returns = serie(autre_index, 0.0002)                    # mal aligné : c'est la seule erreur

    with pytest.raises(ValueError, match="cash_returns"):
        Index(params, exposure, underlying_returns, cash_returns)
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

INDEX_TYPES = {"price_return", "total_return", "excess_return"}
CASH_AWARE_TYPES = {"total_return", "excess_return"}


@dataclass(frozen=True)
class IndexParams:
    name: str
    index_type: str            # price_return | total_return | excess_return
    vol_target: float          # alpha_T
    lam_S: float               # facteur de décroissance court terme
    lam_L: float               # facteur de décroissance long terme
    K: int                     # fenêtre de calcul des volatilités (jours)
    T: int                     # fenêtre du maximum des volatilités (jours)
    LM: float                  # exposition maximale (levier max)
    d: int                     # décalage (jours)
    cash_rate: Optional[str] = None   # ex. "SONIA", "FedFunds" ; None = pas de cash (rC = 0)
    day_count: Optional[int] = None   # 360 ou 365

    def __post_init__(self):
        if self.index_type not in INDEX_TYPES:
            raise ValueError(f"{self.name}: index_type inconnu '{self.index_type}'")
        if not 0 < self.lam_S < self.lam_L <= 1:
            raise ValueError(f"{self.name}: il faut 0 < lam_S < lam_L <= 1")
        if self.vol_target <= 0 or self.LM <= 0:
            raise ValueError(f"{self.name}: vol_target et LM doivent être > 0")
        if self.K < 1 or self.T < 1 or self.d < 0:
            raise ValueError(f"{self.name}: K, T >= 1 et d >= 0")
        if self.index_type in CASH_AWARE_TYPES:
            if self.cash_rate is None or self.day_count not in (360, 365):
                raise ValueError(f"{self.name}: {self.index_type} exige cash_rate et day_count (360 ou 365)")
        elif self.cash_rate is not None or self.day_count is not None:
            raise ValueError(f"{self.name}: price_return n'utilise pas de cash, retirez cash_rate et day_count")

    @property
    def uses_cash(self) -> bool:
        return self.index_type in CASH_AWARE_TYPES



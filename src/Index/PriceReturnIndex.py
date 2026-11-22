from src.Index.BaseVolTargetIndex import BaseVolTargetIndex

class PriceReturnIndex(BaseVolTargetIndex):
    "PI(t) = PI(t-1) x (1 + E(t) x rU(t))"
    def daily_factor(self):
        return 1 + self.E * self.rU




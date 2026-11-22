from src.Index.CashAwareIndex.CashAwareIndex import CashAwareIndex

class ExcessReturnIndex(CashAwareIndex):
    """EI(t) = EI(t-1) x [1 + E(t) x (rU(t) - rC(t))]"""
    def daily_factor(self):
        return 1 + self.E * (self.rU - self.rC)
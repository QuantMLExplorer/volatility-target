from src.Index.CashAwareIndex.CashAwareIndex import CashAwareIndex

class TotalReturnIndex(CashAwareIndex):
    """TRI(t) = TRI(t-1) x [1 + E(t) x rU(t) + (1 - E(t)) x rC(t)]"""
    def daily_factor(self):
        return 1 + self.E * self.rU + (1 - self.E) * self.rC
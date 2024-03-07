from valuation import models


class Valuation:
    def __init__(self, cost_centers: list[models.CostCenter]):
        self.cc = cost_centers

    def balance_sheet(self) -> list[models.BalanceSheet]:
        pass

    def income_statements(self):
        pass

    def chash_flow(self):
        pass

    def free_cash_flow(self):
        pass

    def valuation(self):
        pass

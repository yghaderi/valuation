from valuation import models
from valuation import algo


class Valuation:
    def __init__(self, param: models.Valuation):
        self.param = param

    def handel_generator(self):
        for cc in self.param.cost_centers:
            if cc.input.fixed_asses:
                for fa in cc.input.fixed_asses:
                    self.g_fa = algo.FixedAsset(param=fa).generate()
        return self

    def balance_sheet(self) -> list[models.BalanceSheet]:
        records = []
        for length in range(self.param.financial_year.length):
            bs = models.BalanceSheet(
                fixed_asset=next(self.g_fa).book_value
            )
        return records

    def income_statements(self):
        pass

    def chash_flow(self):
        pass

    def free_cash_flow(self):
        pass

    def valuation(self):
        pass

from valuation import models
from valuation import algo


class Valuation:
    def __init__(self, param: models.Valuation):
        self.param = param
        self.bs_records = []
        self.is_records = []

    def fit_generator(self):
        length = range(self.param.financial_year.length)
        self.g_valuation = models.GenValuation()
        for cc in self.param.cost_centers:
            gcc = models.GenCostCenter(id=cc.id)
            g_input = models.GenInput()
            if cc.input.fixed_asses:
                for fa in cc.input.fixed_asses:
                    fa_algo = algo.FixedAsset(param=fa)
                    g_input.fixed_asses.append(
                        [
                            models.GenFixedAsset(
                                year=year + 1, **next(fa_algo.generate()).model_dump()
                            )
                            for year in length
                        ]
                    )

            gcc.inputs.append(g_input)
            self.g_valuation.cost_centers.append(gcc)
        return self

    def handel_fixed_asset(self):

        for cc in self.g_valuation.cost_centers:
            for input_ in cc.inputs:
                if input_.fixed_asses:
                    fixed_asses: list[list[models.GenFixedAsset]] = input_.fixed_asses
                    for fa in fixed_asses:
                        self.bs_records.append(
                            [{"year": i.year, "fixed_asses": i.book_value} for i in fa]
                        )
                        self.is_records.append(
                            [
                                {"year": i.year, "depreciation": i.depreciation}
                                for i in fa
                            ]
                        )

    def balance_sheet(self) -> list[models.BalanceSheet]:
        records = []
        return records

    def income_statements(self):
        pass

    def chash_flow(self):
        pass

    def free_cash_flow(self):
        pass

    def valuation(self):
        pass

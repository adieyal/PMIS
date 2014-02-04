from datetime import datetime
from functools import partial
from dateutil.relativedelta import relativedelta
from _baseprojectparser import BaseProjectParser

financial_year = range(4, 13) + range(1,4)

class RetentionProjectParser(BaseProjectParser):
    def __init__(self, sheet, month, fyear):
        self.sheet = sheet
        self.month = month
        self.fyear = fyear
        self._monthcols = ["O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

    def _actual(self, row):
        idx = financial_year.index(self.month)
        months = range(0, 12)[0:idx + 1]

        one_month = relativedelta(months=1)
        start_date = datetime(year=self.fyear - 1, month=4, day=1)
        return [
            {
                "progress" : 100,
                "expenditure" : self._to_currency(self._cell(row, el)),
                "date" : start_date + one_month * i
            }
            for i, el in zip(months, self._monthcols)
        ]

    def parse(self, project_range):
        row = project_range["start_row"]
        cell = partial(self._cell, row)
        cell_as_date = partial(self._cell_as_date, row)
        to_currency = self._to_currency
        to_percentage = self._to_percentage

        total_actual = to_currency(cell("AA"))
        total_anticipated = to_currency(cell("AC"))
        final_account = total_anticipated - total_actual

        details = {
            "state": "retention",
            "fyear" : self.fyear,
            "description" : cell("C"),
            "contract" : cell("D"),
            "circuit" : "",
            "scope" : cell("F"),
            "implementing_agent" : cell("G"),
            "municipality" : cell("I"),
            "district" : project_range["district"],
            "programme" : project_range["programme"],
            "actual_start" : cell_as_date("K"),
            "planned_start" : cell_as_date("K"),
            "actual_completion" : cell_as_date("M"),
            "planned_completion" : cell_as_date("M"),
            "actual_final_accounts" : None,
            "planned_final_accounts" : None,
            "allocated_budget_for_year" : to_currency(cell("N")),
            "final_account" : final_account,
            "actual" : self._actual(row),
            "comments" : "",
            "remedial_action" : "",
        }

        return details

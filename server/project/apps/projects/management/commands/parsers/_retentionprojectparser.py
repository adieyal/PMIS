from datetime import datetime
from functools import partial
from dateutil.relativedelta import relativedelta
from _baseprojectparser import BaseProjectParser

class RetentionProjectParser(BaseProjectParser):
    def __init__(self, sheet, fyear):
        self.sheet = sheet
        self.fyear = fyear

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
            "fyear" : self.fyear,
            "description" : cell("C"),
            "contract" : cell("D"),
            "circuit" : cell("E"),
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
        }

        return details

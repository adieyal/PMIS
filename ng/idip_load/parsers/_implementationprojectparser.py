from datetime import datetime
from functools import partial
from dateutil.relativedelta import relativedelta
from _baseprojectparser import BaseProjectParser

class ImplementationProjectParser(BaseProjectParser):
    def __init__(self, sheet, fyear):
        self.sheet = sheet
        self.fyear = fyear
        self._monthcols = ["Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB"]

    def _planning(self, row):
        one_month = relativedelta(months=1)
        start_date = datetime(year=self.fyear - 1, month=4, day=1)
        return [
            {
                "expenditure" : self._to_currency(self._cell(row, el)),
                "progress" : self._to_percentage(self._cell(row, el, 1)),
                "date" : start_date + one_month * i
            }
            for i, el in enumerate(self._monthcols)
        ]

    def _actual(self, row):
        one_month = relativedelta(months=1)
        start_date = datetime(year=self.fyear - 1, month=4, day=1)
        return [
            {
                "progress" : self._to_percentage(self._cell(row, el, 4)),
                "expenditure" : self._to_currency(self._cell(row, el, 5)),
                "date" : start_date + one_month * i
            }
            for i, el in enumerate(self._monthcols)
        ]


    def parse(self, project_range):
        row = project_range["start_row"]
        cell = partial(self._cell, row)
        cell_as_date = partial(self._cell_as_date, row)
        to_currency = self._to_currency
        to_percentage = self._to_percentage
        planning = partial(self._planning, row)
        actual = partial(self._actual, row)

        details = {
            "phase": "implementation",
            "fyear" : self.fyear,
            "description" : cell("D"),
            "district" : project_range["district"],
            "programme" : project_range["programme"],
            "contract" : cell("D", 1),
            "municipality" : cell("D", 2),
            "location" : cell("D", 3),
            "circuit" : cell("D", 3),
            "source" : cell("D", 4),
            "manager" : cell("D", 5),

            "total_anticipated_cost" : to_currency(cell("J")),
            "total_previous_expenses" : to_currency(cell("K")),
            "allocated_budget_for_year" : to_currency(cell("L")),
            "expenditure_in_year" : to_currency(cell("N")),
            "expenditure_to_date" : to_currency(cell("O")),
            
            "expenditure_percent_of_budget" : to_percentage(cell("O", 1)),

            "planning" : planning(),
            "actual" : actual(),

            "comments" : cell("AF"),
            "remedial_action" : cell("AG"),

            "implementing_agent" : cell("F", 1),
            "principal_agent" : cell("F", 3),
            "contractor" : cell("F", 5),

            "scope" : cell("G"),

            "actual_start" : self.sheet.cell_as_date("AC%d" % (row + 3)),

            "planned_start" : cell_as_date("AC", 1),
            "planned_completion" : cell_as_date("AD", 1),
            "planned_final_accounts" : cell_as_date("AE", 1),
            "actual_start" : cell_as_date("AC", 4),
            "revised_completion" : cell_as_date("AD", 4),
            "actual_completion" : cell_as_date("AE", 4),
            "actual_final_accounts" : cell_as_date("AE", 3),
            "implementation_handover" : cell_as_date("AC", 4),
        }

        return details

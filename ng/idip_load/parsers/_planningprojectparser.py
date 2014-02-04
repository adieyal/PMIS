from _implementationprojectparser import ImplementationProjectParser
from functools import partial

class PlanningProjectParser(ImplementationProjectParser):
    def __init__(self, *args, **kwargs):
        super(PlanningProjectParser, self).__init__(*args, **kwargs)

        self._monthcols = ["R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC"]

    def parse(self, *args, **kwargs):
        project_range = args[0]
        row = project_range["start_row"]
        to_currency = self._to_currency
        to_percentage = self._to_percentage
        cell = partial(self._cell, row)
        cell_as_date = partial(self._cell_as_date, row)

        details = super(PlanningProjectParser, self).parse(*args, **kwargs)
        details["state"] = "planning"
        details["total_previous_expenses"] = to_currency(cell("L"))
        details["allocated_budget_for_year"] = to_currency(cell("M"))
        details["comments"] = cell("AG")
        details["remedial_action"] = cell("AH")

        details["planned_start"] = cell_as_date("AD", 1)
        details["planned_completion"] =  cell_as_date("AE", 1)
        details["planned_final_accounts"] =  cell_as_date("AF", 1)
        details["actual_start"] =  cell_as_date("AD", 3)
        details["actual_completion"] =  cell_as_date("AE", 3)
        details["actual_final_accounts"] =  cell_as_date("AF", 3)

        return details
        
        

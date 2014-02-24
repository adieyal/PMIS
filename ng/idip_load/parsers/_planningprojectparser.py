from _implementationprojectparser import ImplementationProjectParser
from functools import partial

class PlanningProjectParser(ImplementationProjectParser):
    def __init__(self, *args, **kwargs):
        super(PlanningProjectParser, self).__init__(*args, **kwargs)

        self._monthcols = ["R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC"]

    def parse(self, *args, **kwargs):
        project_range = args[0]
        
        row = project_range["start_row"]
        cell = partial(self._cell, row)
        cell_as_date = partial(self._cell_as_date, row)
        to_currency = self._to_currency
        to_percentage = self._to_percentage
        planning = partial(self._planning, row)
        actual = partial(self._actual, row)

        details = {
            "phase": "planning",
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
            "total_confirmed_budget" : to_currency(cell("K")),
            "total_previous_expenses" : to_currency(cell("L")),
            "allocated_budget_for_year" : to_currency(cell("M")),
            "total_anticipated_in_year" : to_currency(cell("N")),
            "expenditure_in_year" : to_currency(cell("O")),
            "expenditure_to_date" : to_currency(cell("P")),
            
            "expenditure_percent_of_budget" : to_percentage(cell("O", 1)),

            "planning" : planning(),
            "actual" : actual(),

            "comments" : cell("AG"),
            "remedial_action" : cell("AH"),

            "implementing_agent" : cell("F", 1),
            "principal_agent" : cell("F", 3),

            "scope" : cell("G"),

            "planning_start" : cell_as_date("AD", 1),
            "planning_completion" : cell_as_date("AE", 1),
            "contract_award_date" : cell_as_date("AF", 1),
        }

        return details
        
        

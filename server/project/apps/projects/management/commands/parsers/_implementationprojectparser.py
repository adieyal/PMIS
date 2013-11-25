from datetime import datetime
from dateutil.relativedelta import relativedelta

class ImplementationProjectParser(object):
    def __init__(self, sheet, fyear):
        self.sheet = sheet
        self.fyear = fyear

    def parse(self, project_range):
        row = project_range["start_row"]

        description = self.sheet.cell("D%d" % row)
        contract = self.sheet.cell("D%d" % (row + 1))
        municipality = self.sheet.cell("D%d" % (row + 2))
        circuit = self.sheet.cell("D%d" % (row + 3))
        source = self.sheet.cell("D%d" % (row + 4))
        manager = self.sheet.cell("D%d" % (row + 5))

        def to_currency(x):
            try:
                return float(x) * 1000
            except ValueError:
                return 0

        def to_percentage(x):
            try:
                return float(x)
            except ValueError:
                return 0

        def cell(col, idx=0):
            return self.sheet.cell("%s%d" % (col, row + idx))

        def planning():
            one_month = relativedelta(months=1)
            start_date = datetime(year=self.fyear - 1, month=4, day=1)
            return [
                {
                    "expenditure" : to_currency(cell(el)),
                    "progress" : to_percentage(cell(el, 1)),
                    "date" : start_date + one_month * i
                }
                for i, el in enumerate(["Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB"])
            ]

        return {
            "fyear" : self.fyear,
            "description" : description,
            "contract" : contract,
            "district" : project_range["district"],
            "programme" : project_range["programme"],
            "municipality" : municipality,
            "circuit" : circuit,
            "source" : source,
            "manager" : manager,
            "total_anticipated_cost" : to_currency(cell("J")),
            "total_previous_expenses" : to_currency(cell("K")),
            "allocated_budget_for_year" : to_currency(cell("L")),
            "planning" : planning(),
            "comments" : cell("AD"),
            "remedial_action" : cell("AE"),
            "implementing_agent" : cell("AF", 1),
            "principal_agent" : cell("AF", 3),
            "contractor" : cell("AF", 5),
            "scope" : cell("AG"),
            "planned_start" : self.sheet.cell_as_date("AA%d" % (row + 1)),
            "planned_completion" : self.sheet.cell_as_date("AB%d" % (row + 1)),
            "planned_final_accounts" : self.sheet.cell_as_date("AC%d" % (row + 1)),
            "actual_start" : self.sheet.cell_as_date("AA%d" % (row + 4)),
            "actual_completion" : self.sheet.cell_as_date("AB%d" % (row + 4)),
            "actual_final_accounts" : self.sheet.cell_as_date("AC%d" % (row + 4)),
        }

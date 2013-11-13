class ImplementationProjectParser(object):
    def __init__(self, sheet):
        self.sheet = sheet

    def parse(self, project_range):
        row = project_range["start_row"]

        description = self.sheet.cell("D%d" % row)
        contract = self.sheet.cell("D%d" % (row + 1))
        municipality = self.sheet.cell("D%d" % (row + 2))
        circuit = self.sheet.cell("D%d" % (row + 3))
        source = self.sheet.cell("D%d" % (row + 4))
        manager = self.sheet.cell("D%d" % (row + 5))

        return {
            "description" : description,
            "contract" : contract,
            "municipality" : municipality,
            "circuit" : circuit,
            "source" : source,
            "manager" : manager,
            "comments" : self.sheet.cell("AD%d" % row),
            "remedial_action" : self.sheet.cell("AE%d" % row),
            "implementing_agent" : self.sheet.cell("AF%d" % (row + 1)),
            "principal_agent" : self.sheet.cell("AF%d" % (row + 3)),
            "contractor" : self.sheet.cell("AF%d" % (row + 5)),
            "scope" : self.sheet.cell("AG%d" % row),
            "planned_start" : self.sheet.cell_as_date("AA%d" % (row + 1)),
            "planned_completion" : self.sheet.cell_as_date("AB%d" % (row + 1)),
            "planned_final_accounts" : self.sheet.cell_as_date("AC%d" % (row + 1)),
            "actual_start" : self.sheet.cell_as_date("AA%d" % (row + 4)),
            "actual_completion" : self.sheet.cell_as_date("AB%d" % (row + 4)),
            "actual_final_accounts" : self.sheet.cell_as_date("AC%d" % (row + 4)),
        }

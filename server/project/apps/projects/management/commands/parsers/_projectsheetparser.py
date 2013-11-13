class ProjectSheetParser(object):
    def __init__(self, sheet):
        self.sheet = sheet
        self.state = self.start_state
        self.programme = None
        self.district = None
        self.start_row = None
        self.skip_input = "Skip"

    def _isnumber(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def _containsdistrict(self, value):
        value = value.upper()
        if "GERT SIBANDE" in value or "NKANGALA" in value or "EHLANZENI" in value or "ALL DISTRICTS" in value:
            return True
        return False

    @property
    def projects(self):
        for i in range(0, self.sheet.nrows):
            value = self.skip_input
            while value == self.skip_input:
                value = self.state(i)
                if type(value) == tuple:
                    yield {
                        "start_row" : value[0],
                        "end_row" : value[1],
                        "programme" : self.programme,
                        "district" : self.district
                    }
                    break

    def start_state(self, row):
        bvalue = self.sheet.cell("B%d" % row)
        if bvalue == "No":
            self.state = self.gobble_until_programme_state

    def gobble_until_programme_state(self, row):
        bvalue = self.sheet.cell("B%d" % row)

        if bvalue != "":
            self.state = self.programme_state
            return self.skip_input

    def programme_state(self, row):
        self.programme = self.sheet.cell("B%d" % row)
        self.state = self.district_state

    def district_state(self, row):
        self.district = self.sheet.cell("B%d" % row)
        self.state = self.gobble_before_project

    def gobble_before_project(self, row):
        cvalue = self.sheet.cell("C%d" % row)
        bvalue = self.sheet.cell("B%d" % row)

        if cvalue == "Project Description":
            self.state = self.project_state
            return self.skip_input
        elif self._containsdistrict(bvalue):
            self.state = self.district_state
            return self.skip_input

    def project_state(self, row):
        value = self.sheet.cell("C%d" % row)
        if value == "Project Description":
            self.start_row = row
        elif value == "Responsible Project Manager":
            rng = (self.start_row, row)
            self.state = self.gobble_after_project
            return rng

    def gobble_after_project(self, row):
        cvalue = self.sheet.cell("C%d" % row)
        bvalue = self.sheet.cell("B%d" % row)

        if cvalue == "Project Description":
            self.state = self.project_state
            return self.skip_input
        elif self._containsdistrict(bvalue):
            self.state = self.district_state
            return self.skip_input
        elif bvalue != "" and not self._isnumber(bvalue):
            self.state = self.programme_state
            return self.skip_input


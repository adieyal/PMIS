import logging
from _basesheetparser import BaseSheetParser
logger = logging.getLogger(__name__)

class ImplementationProjectSheetParser(BaseSheetParser):

    def start_state(self, row):
        logger.info("Row %d - Start State" % row)
        bvalue = self.sheet.cell("B%d" % row)
        if bvalue == "No":
            self.next_state = self.programme_state
            self.state = self.gobble_white_space

    def gobble_white_space(self, row):
        logger.info("Row %d - Gobbling white space" % row)
        bvalue = self.sheet.cell("B%d" % row)

        if bvalue != "":
            self.state = self.next_state
            return self.skip_input

    def programme_state(self, row):
        logger.info("Row %d - Programme State" % row)
        self.programme = self.sheet.cell("B%d" % row)
        self.state = self.gobble_white_space
        self.next_state = self.district_state

    def district_state(self, row):
        logger.info("Row %d - District State" % row)
        self.district = self.sheet.cell("B%d" % row)
        self.next_state = self.project_or_district
        self.state = self.gobble_white_space

    def project_or_district(self, row):
        logger.info("Row %d - Project or District State" % row)
        cvalue = self.sheet.cell("C%d" % row)
        bvalue = self.sheet.cell("B%d" % row)

        if cvalue == "Project Description":
            self.state = self.project_state
            return self.skip_input
        elif self._containsdistrict(bvalue):
            self.state = self.district_state
            return self.skip_input

    def project_state(self, row):
        logger.info("Row %d - Project State" % row)
        value = self.sheet.cell("C%d" % row)
        value = " ".join(value.split())
        if value == "Project Description":
            self.start_row = row
        elif "Responsible" in value and "Manager" in value:
            rng = (self.start_row, row)
            self.state = self.gobble_white_space
            self.next_state = self.project_district_programme
            return rng

    def project_district_programme(self, row):
        logger.info("Row %d - Project District Programme State" % row)
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


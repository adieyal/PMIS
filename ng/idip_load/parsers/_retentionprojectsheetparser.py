import logging
from _basesheetparser import BaseSheetParser
logger = logging.getLogger(__name__)

class RetentionProjectSheetParser(BaseSheetParser):

    def start_state(self, row):
        logger.info("Row %d - Start State" % row)
        bvalue = self.sheet.cell("B%d" % row)
        if bvalue == "No":
            self.next_state = self.programme_state
            self.state = self.gobble_white_space

    def gobble_white_space(self, row):
        logger.info("Row %d - Gobbling white space" % row)
        cvalue = self.sheet.cell("C%d" % row)

        if cvalue != "":
            self.state = self.next_state
            return self.skip_input

    def programme_state(self, row):
        logger.info("Row %d - Programme State" % row)
        self.programme = self.sheet.cell("C%d" % row)
        self.state = self.gobble_white_space
        self.next_state = self.retention_state

    def retention_state(self, row):
        logger.info("Row %d - Retention State" % row)
        cvalue = self.sheet.cell("C%d" % row)
        if "Retention Projects" not in cvalue:
            raise Exception("Expected to be in the retention state")

        self.state = self.gobble_white_space
        self.next_state = self.programme_state
        try:
            num_projects = int(self.sheet.cell("E%d" % row))
            if num_projects > 0:
                self.next_state = self.project_state
            
        except ValueError:
            pass

    def project_state(self, row):
        logger.info("Row %d - Project State" % row)
        cvalue = self.sheet.cell("C%d" % row)
        bvalue = self.sheet.cell("B%d" % row)
        self.district = self.sheet.cell("J%d" % row)

        if cvalue.strip() == "":
            self.state = self.gobble_white_space
            self.next_state = self.programme_state
            return self.skip_input
        elif "TOTAL - RETENTION PROJECTS" in bvalue.strip():
            self.state = self.gobble_rows
        else:
            self.state = self.project_state
            return (row, row)

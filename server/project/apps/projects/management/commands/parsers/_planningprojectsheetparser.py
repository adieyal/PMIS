import logging
from _projectsheetparser import ImplementationProjectSheetParser

logger = logging.getLogger(__name__)
class PlanningProjectSheetParser(ImplementationProjectSheetParser):
    def project_state(self, row):
        logger.info("Row %d - Project State" % row)
        value = self.sheet.cell("C%d" % row)
        value = " ".join(value.split())
        if value == "Project Description":
            self.start_row = row
        elif "Project Manager" in value:
            rng = (self.start_row, row)
            self.state = self.gobble_white_space
            self.next_state = self.project_district_programme
            return rng

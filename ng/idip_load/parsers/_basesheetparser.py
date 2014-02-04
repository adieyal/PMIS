class BaseSheetParser(object):
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
        if "GERT SIBANDE" in value or "NKANGALA" in value or "EHLANZENI" in value or "ALL DISTRICTS" in value or "BOHLABELA" in value:
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
        raise NotImplementedException("Need to override this base parser")

    def gobble_rows(self, row):
        logger.info("Row %d - Gobbling row" % row)

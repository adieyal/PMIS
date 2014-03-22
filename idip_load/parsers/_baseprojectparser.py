class BaseProjectParser(object):
    def _cell(self, row, col, idx=0):
        address = "%s%d" % (col, row + idx)
        return self.sheet.cell(address)

    def _cell_as_date(self, row, col, idx=0):
        address = "%s%d" % (col, row + idx)
        return self.sheet.cell_as_date(address)

    def _to_currency(self, x):
        try:
            return float(x) * 1000
        except ValueError:
            return None

    def _to_percentage(self, x):
        try:
            return float(x)
        except ValueError:
            return None


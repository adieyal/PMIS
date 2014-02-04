import re 
from datetime import datetime
import xlrd

re_cell = re.compile("([A-Z]+)([0-9]+)", re.I)
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

class Spreadsheet(object):
    def __init__(self, sheet, datemode=0):
        self.sheet = sheet
        self.datemode = datemode

    def _letter2number(self, cols):
        cols = cols.upper()
        if cols == "":
            return -1

        tail, head = cols[0:-1], cols[-1]

        return (1 + self._letter2number(tail)) * 26 + letters.index(head)

    def _c2c(self, cell):
        col, row = re_cell.search(cell).groups()
        c_row = int(row) - 1
        c_col = self._letter2number(col)
        
        return c_col, c_row

    def cell(self, cell):
        col, row = self._c2c(cell)
        return self.cellxy(col, row)

    def cellxy(self, col, row):
        return self.sheet.cell(row, col).value

    def cell_as_date(self, cell):
        return self.cellxy_as_date(*self._c2c(cell))

    def cellxy_as_date(self, col, row):
        try:
            val = self.cellxy(col, row)
            return datetime(*xlrd.xldate_as_tuple(val, self.datemode))
        except ValueError:
            return None
        
    @property
    def name(self):
        return self.sheet.name

    def __getattr__(self, attribute):
        return getattr(self.sheet, attribute)
    
class WorkBook(object):
    def __init__(self, filename):
        self.workbook = xlrd.open_workbook(filename)

    def sheets(self):
        for sheet in self.workbook.sheets():
            yield Spreadsheet(sheet, self.workbook.datemode)

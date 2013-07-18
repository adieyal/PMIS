import xlrd
import json
from datetime import datetime
import sys
import re

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

re_cell = re.compile("([A-Z]+)([0-9]+)", re.I)

def to_float(x):
    try:
        return float(x)
    except ValueError:
        return 0

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
        return self.sheet.cell(row, col).value

    def cell_as_date(self, cell):
        return datetime(*xlrd.xldate_as_tuple(self.cell(cell), self.datemode))
        
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

def dump_to_json(data):
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    return json.dumps(data, default=dthandler, indent=4)

def process_file(filename):
    all_projects = []
    workbook = WorkBook(filename)
    for sheet in workbook.sheets():
        #yesno = raw_input("Process this sheet? ")
        #if yesno.lower() == "y":
        if "(ONGOING)" in sheet.name or "(COMPLETE" in sheet.name:
            projects = process_sheet(sheet)
            all_projects.extend(projects)
        else:
            print sheet.name
    print dump_to_json(all_projects)

def process_sheet(sheet):
    projects = []
    try:
        programme = sheet.cell("A6")
        
        current_district = ""
        for i in range(7, sheet.nrows):
            cell = "A%s" % i
            try:
                value = sheet.cell(cell)
                if "NKANGALA" in str(value).upper():
                    current_district = "NKANGALA"
                elif "EHLANZENI" in str(value).upper():
                    current_district = "EHLANZENI"
                elif "GERT SIBANDE" in str(value).upper():
                    current_district = "GERT SIBANDE"

                num = int(sheet.cell(cell))
                project = process_project(sheet, cell, current_district, programme)
                projects.append(project)
            except ValueError:
                pass
            
    except IndexError:
        pass
    return projects

def parse_progress(sheet, current_row):
    planned_expenditure_row = current_row
    planned_progress_row = current_row + 1
    actual_progress_row = current_row + 4
    actual_expenditure_row = current_row + 5

    month_cols = "KLMNOPQRSTUV"

    planned_expenditure = [
        to_float(sheet.cell("%s%s" % (col, planned_expenditure_row))) * 1000
        for col in month_cols
    ]

    planned_progress = [
        to_float(sheet.cell("%s%s" % (col, planned_progress_row))) 
        for col in month_cols
    ]

    actual_expenditure = [
        to_float(sheet.cell("%s%s" % (col, actual_expenditure_row))) * 1000
        for col in month_cols
    ]

    actual_progress = [
        to_float(sheet.cell("%s%s" % (col, actual_progress_row))) 
        for col in month_cols
    ]

    progress = []
    for (yy, mm), pe, pp, ae, ap in zip(months, planned_expenditure, planned_progress, actual_expenditure, actual_progress):
        progress.append({
            "year" : yy,
            "month" : mm,
            "planned_expenditure" : pe,
            "planned_progress" : pp,
            "actual_expenditure" : ae,
            "actual_progress" : ap,
        })
    return progress

def process_project(sheet, start_cell, district, programme):
    col, row = re_cell.search(start_cell).groups()
    row = int(row)
    project_name = sheet.cell("B%s" % row)
    total_anticipated_cost = sheet.cell("D%s" % row)
    prev_year_expenditure = sheet.cell("E%s" % row)
    allocated_budget = sheet.cell("F%s" % row)
    expenditure_to_date_current = sheet.cell("G%s" % row)
    expenditure_to_date = sheet.cell("H%s" % row)

    if sheet.cell("B%s" % (row + 1)) == "Start Date":
        start_date = sheet.cell_as_date("C%s" % (row + 1))

    if sheet.cell("B%s" % (row + 2)) == "Completion Date":
        completion_date = sheet.cell_as_date("C%s" % (row + 2))

    if sheet.cell("B%s" % (row + 3)) in ["Revised Completion Date", "Actual Practical Completion Date"]:
        revised_completion = sheet.cell_as_date("C%s" % (row + 3))

    progress = parse_progress(sheet, row)

    completion_row = row + 2
    revised_completion_row = row + 3
    date_cols = "WXY"
    completion_dates = [
        sheet.cell_as_date("%s%s" % (col, completion_row))
        for col in date_cols
    ]

    revised_completion_dates = [
        sheet.cell_as_date("%s%s" % (col, revised_completion_row))
        for col in date_cols
    ]

    comment = sheet.cell("Z%s" % row)
    mitigation = sheet.cell("AA%s" % row)

    consultant = str(sheet.cell("AB%s" % row))
    if ":" in consultant:
        consultant = consultant.split(":")[1].strip()
    else:
        consultant = ""

    contractor = str(sheet.cell("AB%s" % (row + 3)))
    if ":" in contractor:
        contractor = contractor.split(":")[1].strip()
    else:
        contractor = ""

    return {
        "year" : year,
        "month" : month,
        "project" : project_name,
        "district" : district,
        "programme" : programme,
        "total_anticipated_cost" : total_anticipated_cost * 1000,
        "prev_year_expenditure" : prev_year_expenditure * 1000,
        "allocated_budget" : allocated_budget * 1000,
        "allocated_planning_budget" : 0 * 1000,
        "expenditure_to_date_current" : expenditure_to_date_current * 1000,
        "expenditure_to_date" : expenditure_to_date * 1000,
        "start_date" : start_date,
        "completion_date" : completion_date,
        "revised_completion" : revised_completion,
        "progress" : progress,
        "comment" : comment,
        "mitigation" : mitigation,
        "completion_dates" : completion_dates,
        "revised_completion_dates" : revised_completion_dates,
        "consultant" : consultant,
        "contractor" : contractor,
    }

if __name__ == "__main__":
    filename = sys.argv[1]
    year = int(sys.argv[2])
    month = int(sys.argv[3])
    financial_year_months = range(4, 13) + range(1, 4)
    months = zip([year - 1] * 9 + [year] * 3, financial_year_months)
    process_file(filename)
#sheet = self.workbook.sheet_by_name(sheet_name)
#data = ftypes.list(*self._load_data())


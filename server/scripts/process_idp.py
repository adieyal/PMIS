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

def process_file(filename, processor):
    all_projects = []
    workbook = WorkBook(filename)
    for sheet in workbook.sheets():
        #yesno = raw_input("Process this sheet? ")
        #if yesno.lower() == "y":
        #if "(ONGOING)" in sheet.name or "(COMPLETE" in sheet.name:
        for label in ["ONGOING", "ON GOING", "ON-GOING", "ON-GO"]:
            if label in sheet.name.upper():
                
                projects = process_sheet(sheet, processor)
                all_projects.extend(projects)
                break
        #else:
        #    print sheet.name
    print dump_to_json(all_projects)

def process_sheet(sheet, processor_class):
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
            except ValueError:
                continue

            _, row = sheet._c2c(cell)
            processor = processor_class(sheet, row + 1)
            project = processor.process_project(current_district, programme)
            projects.append(project)
            
    except IndexError:
        pass
    return projects

class ProjectProcessor(object):
    def __init__(self, sheet, row):
        self.sheet = sheet
        self.row = row

    @property
    def municipality(self):
        return ""


    @property
    def scope_of_work(self):
        return []


    @property
    def parse_progress(self):

        month_cols = self.activity_month_cols

        planned_expenditure = [
            to_float(self.sheet.cell("%s%s" % (col, self.row + self.planned_expenditure_row))) * 1000
            for col in month_cols
        ]

        planned_progress = [
            to_float(self.sheet.cell("%s%s" % (col, self.row + self.planned_progress_row))) 
            for col in month_cols
        ]

        actual_expenditure = [
            to_float(self.sheet.cell("%s%s" % (col, self.row + self.actual_expenditure_row))) * 1000
            for col in month_cols
        ]

        actual_progress = [
            to_float(self.sheet.cell("%s%s" % (col, self.row + self.actual_progress_row))) 
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

    def process_project(self, district, programme):

        return {
            "year" : year,
            "month" : month,
            "project" : self.project_name,
            "project_code" : self.project_code,
            "district" : district,
            "municipality" : self.municipality,
            "programme" : programme,
            "total_anticipated_cost" : self.total_anticipated_cost,
            "prev_year_expenditure" : self.prev_year_expenditure,
            "allocated_budget" : self.allocated_budget,
            "allocated_planning_budget" : 0,
            "expenditure_to_date_current" : self.expenditure_to_date_current,
            "expenditure_to_date" : self.expenditure_to_date,
            "start_date" : self.start_date,
            "completion_date" : self.completion_date,
            "revised_completion" : self.revised_completion_date,
            "progress" : self.parse_progress,
            "comment" : self.comment,
            "mitigation" : self.mitigation,
            "completion_dates" : self.completion_dates,
            "revised_completion_dates" : self.revised_completion_dates,
            "consultant" : self.consultant,
            "contractor" : self.contractor,
            "scope_of_work" : self.scope_of_work,
        }

class BasicProcessor(ProjectProcessor):

    @property
    def activity_month_cols(self):
        return "KLMNOPQRSTUV"

    @property
    def planned_expenditure_row(self):
        return 0

    @property
    def planned_progress_row(self):
        return 1
        
    @property
    def actual_progress_row(self):
        return 4

    @property
    def actual_expenditure_row(self):
        return 5

    @property
    def project_name(self):
        return self.sheet.cell("B%s" % self.row)

    @property
    def project_code(self):
        return self.sheet.cell("C%s" % self.row)

    @property
    def total_anticipated_cost(self):
        try:
            return float(self.sheet.cell("D%s" % self.row)) * 1000
        except ValueError:
            return None

    @property
    def prev_year_expenditure(self):
        return float(self.sheet.cell("E%s" % self.row)) * 1000

    @property
    def allocated_budget(self):
        return float(self.sheet.cell("F%s" % self.row)) * 1000

    @property
    def expenditure_to_date_current(self):
        return float(self.sheet.cell("G%s" % self.row)) * 1000

    @property
    def expenditure_to_date(self):
        return float(self.sheet.cell("H%s" % self.row)) * 1000

    def _date(self, row, string):
        date = None
        if self.sheet.cell("B%s" % row) == string:
            date = self.sheet.cell_as_date("C%s" % row)
        return date
        
    @property
    def start_date(self):
        return self._date(self.row + 1, "Start Date")

    @property
    def completion_date(self):
        return self._date(self.row + 2, "Completion Date")

    @property
    def revised_completion_date(self):
        return self._date(self.row + 3, "Revised Completion Date") or self._date(self.row + 3, "Actual Practical Completion Date")

    def _dates(self, row):
        date_cols = "WXY"
        dates = [
            self.sheet.cell_as_date("%s%s" % (col, row))
            for col in date_cols
        ]
        return dates
        
    @property
    def completion_dates(self):
        return self._dates(self.row + 2)

    @property
    def revised_completion_dates(self):
        return self._dates(self.row + 3)

    @property
    def comment(self):
        return self.sheet.cell("Z%s" % self.row)
        
    @property
    def mitigation(self):
        return self.sheet.cell("AA%s" % self.row)

    @property
    def consultant(self):
        consultant = str(self.sheet.cell("AB%s" % self.row))
        if ":" in consultant:
            consultant = consultant.split(":")[1].strip()
        return consultant

    @property
    def contractor(self):
        contractor = str(self.sheet.cell("AB%s" % (self.row + 3)))
        if ":" in contractor:
            contractor = contractor.split(":")[1].strip()
        return contractor

class DSDProcessor(BasicProcessor):

    @property
    def municipality(self):
        return self.sheet.cell("B%s" % (self.row + 4))

    @property
    def consultant(self):
        return str(self.sheet.cell("F%s" % (self.row + 4)))
     
    @property
    def contractor(self):
        return str(self.sheet.cell("F%s" % (self.row + 5)))

class ModernProcessor(BasicProcessor):

    @property
    def activity_month_cols(self):
        return "NOPQRSTUVWXY"

    @property
    def planned_expenditure_row(self):
        return 0

    @property
    def planned_progress_row(self):
        return 2
        
    @property
    def actual_progress_row(self):
        return 5

    @property
    def actual_expenditure_row(self):
        return 6

    @property
    def municipality(self):
        return self.sheet.cell("C%s" % self.row)
    
    @property
    def project_code(self):
        return self.sheet.cell("D%s" % self.row)

    @property
    def total_anticipated_cost(self):
        return to_float(self.sheet.cell("E%s" % self.row)) * 1000

    @property
    def prev_year_expenditure(self):
        return to_float(self.sheet.cell("F%s" % self.row)) * 1000

    @property
    def allocated_budget(self):
        return to_float(self.sheet.cell("G%s" % self.row)) * 1000

    @property
    def expenditure_to_date_current(self):
        return to_float(self.sheet.cell("J%s" % self.row)) * 1000

    @property
    def expenditure_to_date(self):
        return to_float(self.sheet.cell("K%s" % self.row)) * 1000

    def _date(self, row, string):
        date = None
        try:
            if self.sheet.cell("B%s" % row) == string:
                date = self.sheet.cell_as_date("D%s" % row)
        except ValueError:
            pass
        return date
        
    @property
    def start_date(self):
        return self._date(self.row + 2, "Start Date")

    @property
    def completion_date(self):
        return self._date(self.row + 3, "Completion Date")

    @property
    def revised_completion_date(self):
        return self.completion_date(self.row)

    def _dates(self, row):
        date_cols = ["Z", "AA", "AB"]
        dates = [
            self.sheet.cell_as_date("%s%s" % (col, row))
            for col in date_cols
        ]
        return dates
        
    @property
    def completion_dates(self):
        try:
            return self._dates(self.row + 3)
        except ValueError:
            return []

    @property
    def revised_completion_dates(self):
        return self.completion_dates(self.row)

    @property
    def comment(self):
        return self.sheet.cell("AC%s" % self.row)
        
    @property
    def mitigation(self):
        return self.sheet.cell("AD%s" % self.row)

    @property
    def consultant(self):
        return self.sheet.cell("F%s" % (self.row + 4))

    @property
    def contractor(self):
        return self.sheet.cell("F%s" % (self.row + 5))

    @property
    def scope_of_work(self):
        scope_str = self.sheet.cell("F%s" % (self.row + 6))
        return scope_str.split(",")

processors = {
    "modern" : ModernProcessor,
    "dsd" : DSDProcessor,
}


if __name__ == "__main__":
    filename = sys.argv[1]
    year = int(sys.argv[2])
    month = int(sys.argv[3])
    processor = sys.argv[4]

    processor = processors[processor]
    financial_year_months = range(4, 13) + range(1, 4)
    calc_year = (year + 1) if month > 3 else year 
    months = zip([calc_year - 1] * 9 + [calc_year] * 3, financial_year_months)
    process_file(filename, processor)


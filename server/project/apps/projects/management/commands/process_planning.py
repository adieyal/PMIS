import sys
from datetime import datetime
from pprint import pprint

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from project.apps.projects import models

import spreadsheet
import utils

consultant = models.Role.objects.get(name="Consultant")
contractor = models.Role.objects.get(name="Contractor")

def save_project(project, params ):
    p, _ = models.Project.objects.get_or_create(name=project["project"], programme=project["programme"])
    p.code = project["project_code"]
    p.municipality = project["municipality"]
    p.save()

    pf, _ = models.ProjectFinancial.objects.get_or_create(project=p)
    pf = p.project_financial
    pf.total_anticipated_cost = project["total_anticipated_cost"]
    pf.previous_expenses = project["prev_year_expenditure"]
    pf.save()

    budget, _ = models.Budget.objects.get_or_create(project=p, year=2014)
    budget.allocated_budget = project["allocated_budget"]
    budget.allocated_planning_budget = project["allocated_planning_budget"]
    budget.save()

    if project["consultant"]:
        c, _ = models.Entity.objects.get_or_create(name=project["consultant"])
        models.ProjectRole.objects.get_or_create(project=project, role=consultant, entity=c)

    if project["contractor"]:
        c, _ = models.Entity.objects.get_or_create(name=project["contractor"])
        models.ProjectRole.objects.get_or_create(project=project, role=contractor, entity=c)

    for submission in project["progress"]:
        if submission["year"] == params["year"] and submission["month"] < params["month"]:
            try:
                s = models.MonthlySubmission.objects.get(
                    project=p, date__month=params["month"], date__year=params["year"]
                )
            except models.MonthlySubmission.DoesNotExist:
                s = models.MonthlySubmission(
                    project=p, date__month=params["month"], date__year=params["year"]
                )

            s.actual_expenditure = project["actual_expenditure"]
            s.actual_progress = project["actual_progress"]

            if submission["month"] == params["month"]:
                s.remedial_action = project["mitigation"]
                s.comment = project["comment"]
            s.save()

        pl, _ = models.Planning.objects.get_or_create(
            project=p, date__month=params["month"], date__year=params["year"]
        )

        pl.planned_expenditure = project["planned_expenditure"]
        pl.planned_progress = project["planned_progress"]
        pl.save()

def print_project(project):
    def pjust(s):
        s = str(s)
        sys.stdout.write(s.ljust(12))

    def pjustln(s):
        pjust(s)
        print ""

    print "Name: " + project["project"]
    print "Code: " + project["project_code"]
    print "District: " + project["district"]
    print "Municipality: " + str(project["municipality"])
    print "Programme: " + str(project["programme"])
    print "Total Anticipated Cost: %s" % project["total_anticipated_cost"]
    print "Prev Year Expenditure: %s" % project["prev_year_expenditure"]
    print "Overall Budget: %s" % project["allocated_budget"]
    print "Planning Budget: %s" % project["allocated_planning_budget"]
    print "Consultant: %s" % project["consultant"]
    print "Contractor: %s" % project["contractor"]
    print "Comment: %s" % project["comment"]
    print "Mitigation: %s" % project["mitigation"]

    pjust("Apr"); pjust("May"); pjust("Jun"); pjust("Jul");
    pjust("Aug"); pjust("Sep"); pjust("Oct"); pjust("Nov");
    pjust("Dec"); pjust("Jan"); pjust("Feb"); pjust("Mar");
    print ""

    for submission in project["progress"]:
        pjust(submission["actual_expenditure"])

    print ""

    for submission in project["progress"]:
        pjust(submission["planned_expenditure"])

    print ""

    for submission in project["progress"]:
        pjust(submission["actual_progress"])

    print ""

    for submission in project["progress"]:
        pjust(submission["planned_progress"])

    print ""

def process_file(filename, params):
    all_projects = []
    workbook = spreadsheet.WorkBook(filename)
    for sheet in workbook.sheets():
        if ask_process_sheet(sheet):
            projects = process_sheet(sheet, params)
        #        all_projects.extend(projects)
        #        break
        ##else:
        ##    print sheet.name
    return
    #print utils.dump_to_json(all_projects)

def ask_process_sheet(sheet):
    if "PLANNING" in sheet.name.upper():
        print sheet.name
        yesno = raw_input("Process this sheet?\n")

        if yesno.lower() == "n": return False
        return True

def ask_client():
    clients = list(models.Client.objects.all())
    for i, client in enumerate(clients):
        print "%d) %s" % (i, client.name)
        
    index = raw_input("Which client are you processing?\n")
    return clients[int(index)]

def ask_programme(programme, params):
    client = params["client"]
    programmes = list(models.Programme.objects.filter(client=client))
    for i, prog in enumerate(programmes):
        print "%d) %s" % (i, prog.name)

    print ""
    index = raw_input("Which programme is this: %s\n" % programme)
    return programmes[int(index)]

def ask_proceed_with_project(project):
    yesno = raw_input("Proceed with this project?\n")
    if yesno == "y":
        return True
    else:
        return False

def ask_project_ok(project):
    print_project(project)
    yesno = raw_input("Is this project ok?\n")
    if yesno == "y":
        return project
    else:
        print "Time to fix the project manually"
        import pdb; pdb.set_trace()
        return project

def process_sheet(sheet, params):
    projects = []
    params["programme"] = ask_programme(sheet.name, params)
    
    current_district = ""
    for i in range(12, sheet.nrows):
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
        params["district"] = current_district
        processor_class = params["processor"]
        processor = processor_class(params, sheet, row + 1)
        project = processor.process_project()
        if not ask_proceed_with_project: continue

        project = ask_project_ok(project)
        save_project(project, params)
        projects.append(project)
    return projects

class ProjectProcessor(object):
    def __init__(self, params, sheet, row):
        self.params = params
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
            utils.to_float(self.sheet.cell("%s%s" % (col, self.row + self.planned_expenditure_row))) * 1000
            for col in month_cols
        ]

        planned_progress = [
            utils.to_float(self.sheet.cell("%s%s" % (col, self.row + self.planned_progress_row))) 
            for col in month_cols
        ]

        actual_expenditure = [
            utils.to_float(self.sheet.cell("%s%s" % (col, self.row + self.actual_expenditure_row))) * 1000
            for col in month_cols
        ]

        actual_progress = [
            utils.to_float(self.sheet.cell("%s%s" % (col, self.row + self.actual_progress_row))) 
            for col in month_cols
        ]

        progress = []
        for (yy, mm), pe, pp, ae, ap in zip(self.params["fmonths"], planned_expenditure, planned_progress, actual_expenditure, actual_progress):
            progress.append({
                "year" : yy,
                "month" : mm,
                "planned_expenditure" : pe,
                "planned_progress" : pp,
                "actual_expenditure" : ae,
                "actual_progress" : ap,
            })
        return progress

    def process_project(self):
        programme = self.params["programme"]
        return {
            "year" : self.params["fyear"],
            "month" : self.params["month"],
            "project" : self.project_name,
            "project_code" : self.project_code,
            "district" : self.params["district"],
            "municipality" : self.municipality,
            "programme" : programme,
            "total_anticipated_cost" : self.total_anticipated_cost,
            "prev_year_expenditure" : self.prev_year_expenditure,
            "allocated_budget" : self.allocated_budget,
            "allocated_planning_budget" : self.allocated_planning_budget,
            "expenditure_to_date_current" : self.expenditure_to_date_current,
            "expenditure_to_date" : self.expenditure_to_date,
            "start_date" : self.start_date,
            "completion_date" : self.completion_date,
            "final_accounts" : self.final_accounts,
            "progress" : self.parse_progress,
            "comment" : self.comment,
            "mitigation" : self.mitigation,
            "consultant" : self.consultant,
            "contractor" : self.contractor,
        }

class ModernProcessor(ProjectProcessor):
    @property
    def project_name(self):
        return self.sheet.cell("B%s" % self.row)

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
        return 3

    @property
    def actual_expenditure_row(self):
        return 4

    @property
    def municipality(self):
        munic1 = self.sheet.cell("C%s" % self.row)
        munic2 = self.sheet.cell("C%s" % (self.row + 1))

        try:
            return models.Municipality.objects.get(name__icontains=munic1)
        except Exception:
            pass

        try:
            return models.Municipality.objects.get(name__icontains=munic2)
        except Exception:
            pass

        return None
    
    @property
    def project_code(self):
        code = self.sheet.cell("C%s" % self.row)
        if "PWRT" in code:
            return code.strip()
        code = self.sheet.cell("C%s" % (self.row + 1))
        if "PWRT" in code:
            return code.strip()
        return ""

    @property
    def total_anticipated_cost(self):
        return utils.to_float(self.sheet.cell("D%s" % self.row)) * 1000

    @property
    def prev_year_expenditure(self):
        return utils.to_float(self.sheet.cell("E%s" % self.row)) * 1000

    @property
    def allocated_budget(self):
        return utils.to_float(self.sheet.cell("F%s" % self.row)) * 1000

    @property
    def allocated_planning_budget(self):
        return utils.to_float(self.sheet.cell("G%s" % self.row)) * 1000

    @property
    def expenditure_to_date_current(self):
        return utils.to_float(self.sheet.cell("H%s" % self.row)) * 1000

    @property
    def expenditure_to_date(self):
        return utils.to_float(self.sheet.cell("K%s" % self.row)) * 1000

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
        dt = self.sheet.cell("W%s" % (self.row + 1))
        return utils.to_date(dt)

    @property
    def completion_date(self):
        dt = self.sheet.cell("X%s" % (self.row + 1))
        return utils.to_date(dt)

    @property
    def final_accounts(self):
        dt = self.sheet.cell("Y%s" % (self.row + 1))
        return utils.to_date(dt)

    @property
    def comment(self):
        return self.sheet.cell("Z%s" % self.row)
        
    @property
    def mitigation(self):
        return self.sheet.cell("AD%s" % self.row)

    @property
    def consultant(self):
        consultant = self.sheet.cell("F%s" % (self.row + 3)).strip()
        if consultant == "": return None
        entity, _ = models.Entity.objects.get_or_create(name=consultant)
        return entity

    @property
    def contractor(self):
        contractor = self.sheet.cell("F%s" % (self.row + 4)).strip()
        if contractor == "": return None
        entity, _ = models.Entity.objects.get_or_create(name=contractor)
        return entity

    @property
    def scope_of_work(self):
        scope_str = self.sheet.cell("F%s" % (self.row + 6))
        return scope_str.split(",")

processors = {
    "modern" : ModernProcessor,
}

client = None
class Command(BaseCommand):
    args = "<filename> <year> <month> <modern>"
    help = "load planning data"

    def handle(self, *args, **options):
        params = {}
        filename = args[0]
        params["year"] = int(args[1])
        params["month"] = int(args[2])
        processor = args[3]

        params["client"] = ask_client()
        params["processor"] = processors[processor]

        params["fyear"] = utils.fyear(params["month"], params["year"])
        params["fmonths"] = utils.fmonths(params["fyear"])
        process_file(filename, params)


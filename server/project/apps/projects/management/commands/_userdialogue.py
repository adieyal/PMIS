import os
from datetime import datetime
import json
from project.apps.projects import models
import dateutil.parser as dateparser

x = [2013] *9 + [2014] * 3
y = range(4,13) + range(1,4)
z = [30,31,30,31,31,30,31,30,31,31,28,31]
dates = [datetime(y,m,d) for y,m,d in zip(x,y,z)]
all_zeros = [0,0,0,0,0,0,0,0,0,0,0,0]

class SkipException(Exception): pass
    
class ModelsEncoder(json.JSONEncoder):
    def default(self, obj):
        if obj.__class__ in (
            models.Programme, models.District, models.Municipality, 
            models.Milestone, models.Project
        ):
            return obj.id
        return json.JSONEncoder.default(self, obj)

class UserDialogue(object):
    def __init__(self):
        self.progmap = {}
        self.distmap = {}
        self.municmap = {}
        self.nextmilestonemap = {}
        self.projectmap = {}
        self.cache_path = "/tmp/pmis-dialogue.cache"
        self.load_cache()

    def save_cache(self, map, key, val):
        if val: map[key] = val

        f = open(self.cache_path, "w")
        js = json.dumps({
            "programmes" : self.progmap,
            "districts" : self.distmap,
            "municipalities" : self.municmap,
            "next_milestones" : self.nextmilestonemap,
            "projects" : self.projectmap,
        }, f, cls=ModelsEncoder, indent=4)
        f.write(js)
        f.close()

    def load_cache(self):
        def load_obj(model, id):
            try:
                return model.objects.get(id=id)
            except model.DoesNotExist:
                return None

        sections = {
            "programmes" : {
                "map" : self.progmap,
                "model" : models.Programme
            },
            "districts" : {
                "map" : self.distmap,
                "model" : models.District
            },
            "municipalities" : {
                "map" : self.municmap,
                "model" : models.Municipality
            },
            "next_milestones" : {
                "map" : self.nextmilestonemap,
                "model" : models.Milestone
            },
            "projects" : {
                "map" : self.projectmap,
                "model" : models.Project
            },
        }
        if os.path.exists(self.cache_path):
            js = json.load(open(self.cache_path))
            for section in js.keys():
                details = sections[section]
                for key, val in js[section].items():
                    obj = load_obj(details["model"], int(val))
                    if obj:
                        details["map"][key] = obj

    def _listresponse(self, lst, allow_none=False):
        while True:
            i = 0
            for i, el in enumerate(lst):
                print "%d) %s" % (i, el)
            ignore = i + 1
            none = ignore + 1

            print "%d) Skip this item" % ignore
            if allow_none:
                print "%d) None match" % none

            try:
                result = int(raw_input(""))
                index = int(result)
                if index == ignore:
                    raise SkipException()
                elif index == none:
                    return None

                return lst[index]

            except (ValueError, IndexError, TypeError):
                print ""
                print "%s was not one of the available options - please choose again:" % result

    def _ask(self, lst, input=None, map=None):
        if input == None:
            return self._listresponse(lst, allow_none=True)
        else:
            if not input in map:
                print input
                print ""
                result = self._listresponse(lst, allow_none=True)
                return result
            return self.map[input]

    def _ask_yesno(self, question=""):
        while True:
            result = raw_input(question)
            if result.lower().strip() in ["n", "no"]:
                return False
            elif result.lower().strip() in ["y", "yes"]:
                return True
            print "Expected Yes or No, please try again"

    def ask_month(self):
        while True:
            try:
                print "What month are you processing? (1 - 12): "
                month = raw_input("")
                return int(month)
            except ValueError:
                print "Expected an integer, please try again"

    def ask_year(self):
        while True:
            try:
                return int(raw_input("Which financial year are you processing? (e.g 2013): "))
            except ValueError:
                print "Expected an integer, please try again"


    def ask_client(self):
        clients = models.Client.objects.all()
        return self._ask(clients)

    def ask_programme(self, prog=None, client=None):
        programmes = models.Programme.objects.all()
        print "Which programme?"
        if client:
            programmes = programmes.filter(client=client)
        if prog == None:
            return self._ask(programmes)
        else:
            return self._ask(programmes, input=prog, map=self.progmap)

    def ask_district(self, dist=None):
        districts = models.District.objects.all()
        print "Which district are you processing?"
        return self._ask(districts)

    def ask_municipality(self, district=None, munic=None):
        print "Which municipalities are you processing?"
        municipalities = models.Municipality.objects.all()
        if district:
            municipalities = municipalities.filter(district=district)
        if munic:
            return self._ask(municipalities, input=munic, map=self.municmap)
        else:
            return self._ask(municipalities)

    def ask_project(self, proj=None, **kwargs):
        print "Which project are you processing?"
        projects = models.Project.objects.filter(**kwargs)
        if proj:
            return self._ask(projects, input=proj, map=self.projectmap)
        else:
            return self._ask(projects)

    def ask_financials(self, project):
        try:
            return project.project_financial
        except models.ProjectFinancial.DoesNotExist:
            while True:
                try:
                    print "Lets create the project financials"
                    print "For the following questions, enter only numbers - no formatting"
                    total_anticipated_cost = int(raw_input("What is the total project budget? ")) * 1000
                    previous_expenses = int(raw_input("What were the previous expenses? ")) * 1000
                    final_accounts = int(raw_input("What are the final accounts? ")) * 1000
                    return models.ProjectFinancial(
                        project=project, total_anticipated_cost=total_anticipated_cost,
                        previous_expenses=previous_expenses, final_accounts=final_accounts
                    )
                except ValueError:
                    print "Ensure that you enter in integers where needed. Please try again"

    def ask_budget(self, project, year):
        try:
            return project.budgets.get(year=year)
        except models.Budget.DoesNotExist:
            while True:
                try:
                    print "Lets create a budget for %s" % year
                    print "For the following questions, enter only numbers - no formatting"
                    allocated_budget = int(raw_input("What is the total allocated budget? ")) * 1000
                    allocated_planning_budget = int(raw_input("What is the allocated planning budget? ")) * 1000
                    return models.Budget(
                        project=project, year=year, allocated_planning_budget=allocated_planning_budget, 
                        allocated_budget=allocated_budget
                    )
                except ValueError:
                    print "Ensure that you enter in integers where needed. Please try again"

    def ask_next_milestone(self, comments=None, **kwargs):
        milestones = models.Milestone.objects.filter(**kwargs)
        print "What is the next milestone for this project?"
        if comments:
            print ""
            print "What is the next milestone for this project?"
            print "Here are the comments from the IDIP:"
            print comments
            return self._ask(milestones, input=comments, map=self.nextmilestonemap)
        else:
            return self._ask(milestones)

    def _ask_months(self):
        print "Was any progress in the current financial year? "
        if self._ask_yesno():
            while True:
                try:
                    print "Please enter in an array of 12 numbers, one for each month, starting from April"
                    print "The array should contain the progress for each month"
                    print "values should be in percentage values - e.g. 30% should be entered as 30"
                    print "The array should be formatted like this: 10,15,20,20,20,21,22,30,40,50,60,70"
                    result = raw_input("")
                    progress = [float(el) for el in result.split(",")]
                    progress = (progress + progress[-1:] * 12)[0:12]
                    break
                except ValueError:
                    print "Please ensure that you enter in the array correctly"
        else:
            progress = all_zeros

        print "Were any payments in the current financial year? "
        if self._ask_yesno():
            while True:
                try:
                    print "Please enter in an array of 12 numbers, one for each month, starting from April"
                    print "The array should contain the payment for each month"
                    print "values should be in unformatted numbers and should be in thousands"
                    print "e.g. 150 would actually be 150000"
                    print "The array should be formatted like this: 150,0,0,0,25,0,0,0,0,60,0,0"
                    result = raw_input("")
                    payments = [float(el) * 1000 for el in result.split(",")]
                    payments = (payments + payments[-1:] * 12)[0:12]
                    break 
                except ValueError:
                    print "Please ensure that you enter in the array correctly"
        else:
            payments = all_zeros
        return (progress, payments)

    def ask_planning(self, project):
        progress, payments = self._ask_months()

        return [
            models.Planning(date=d, planned_expenses=pay, planned_progress=prog, project=project)
            for d, pay, prog in zip(dates, payments, progress)
        ]

    def ask_monthly_submissions(self, project):
        progress, payments = self._ask_months()

        return [
            models.MonthlySubmission(
                date=d, actual_expenditure=pay, actual_progress=prog, project=project
            )
            for d, pay, prog in zip(dates, payments, progress)
        ]

    def ask_milestone_date(self, project, milestone):
        while True:
            try:
                result = raw_input("Please enter in a date (yyyy-mm-dd) for milestone: %s: " % milestone.name)
                date = dateparser.parse(result)

                return models.ProjectMilestone(project=project, completion_date=date, milestone=milestone)
            except Exception:
                print "Some error occurred when entering the date. Please try again"

    def ask_project_role(self, project, role):
        entities = models.Entity.objects.filter(project_roles__role=role).distinct()
        if len(entities) < 10:
            entity = self._ask(entities)
        else:
            query = raw_input("Enter in a string to search for: ")
            filtered_entities = entities.filter(name__icontains=query.lower())
            entity = self._ask(filtered_entities)
            if entity == None:
                name = raw_input("Ok, let's create a new entity. Please enter in the entity name: ")
                entity, _ = models.Entity.objects.get_or_create(name=name)
            
        return models.ProjectRole(project=project, role=role, entity=entity) 
        
        

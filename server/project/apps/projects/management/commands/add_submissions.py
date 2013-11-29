from project.apps.projects.management.commands._userdialogue import UserDialogue
from django.db import transaction
import sys
from datetime import datetime
from project.apps.projects import models

ud = UserDialogue()

def find_project(municipality, programme):
    project = None
    project_name = raw_input("What is the name of the project? ")
    project_num = raw_input("Does the project have a project number? (Enter No or the project number): ")
    print ""

    if project_num.lower().strip() not in ["n", "no"]:
        project = ud.ask_project(project_number=project_num)
    else:
        project_num = None

    if project == None:
        project = ud.ask_project(municipality=municipality, programme=programme)

    if project == None:
        project = models.Project.objects.create(
            name=project_name, project_number=project_num or "",
            programme=programme, municipality=municipality 
        )

        print "Created a new project"

    print "Project Details"
    print "==============="
    print "Name: %s" % project.name
    print "Project Number: %s" % project.project_number
    print "Municipality: %s" % project.municipality
    print "Programme: %s" % project.programme
    print ""

    return project

def save_next_milestone(project):
    milestone = ud.ask_next_milestone()
    project.current_step = milestone
    project.save()

year = ud.ask_year()
month = ud.ask_month()
client = ud.ask_client()

while True:

    with transaction.commit_on_success():
        print ""
        print "New project"
        print "=" * 10

        programme = ud.ask_programme(client=client)
        district = ud.ask_district()
        municipality = ud.ask_municipality(district)
        project = find_project(municipality, programme)
        save_next_milestone(project) 
        financials = ud.ask_financials(project)
        financials.save()
        budget = ud.ask_budget(project, year)
        budget.save()

        print "Lets create planning entries"
        plannings = ud.ask_planning(project)
        [p.save() for p in plannings]

        print "Lets create monthly submisssion"
        submissions = ud.ask_monthly_submissions(project)
        [m.save() for m in submissions]

        print "Added comments and remedial action for the current month"
        submission = [s for s in submissions if s.date.month == month][0]
        comment = raw_input("What was the comment for this month? ")
        remedial_action = raw_input("What was the remedial_action for this month? ")
        submission.comment = comment
        submission.remedial_action = remedial_action
        submission.save()

        if ud._ask_yesno("Do you want to add a start date for the project? "):
            ud.ask_milestone_date(project, models.Milestone.start_milestone()).save()
        if ud._ask_yesno("Do you want to add a practical completion date for the project? "):
            ud.ask_milestone_date(project, models.Milestone.practical_completion()).save()
        if ud._ask_yesno("Do you want to add a final completion date for the project? "):
            ud.ask_milestone_date(project, models.Milestone.final_completion()).save()
        if ud._ask_yesno("Do you want to add a final accounts date for the project? "):
            ud.ask_milestone_date(project, models.Milestone.final_accounts()).save()

        if ud._ask_yesno("Do you want to add an implementing agent for the project? "):
            ud.ask_project_role(project, models.Role.objects.get(id=1)).save()
        if ud._ask_yesno("Do you want to add a consultant for the project? "):
            ud.ask_project_role(project, models.Role.objects.get(id=2)).save()
        if ud._ask_yesno("Do you want to add a contractor for the project? "):
            ud.ask_project_role(project, models.Role.objects.get(id=3)).save()
    
    print "Any more projects to enter? (Y/N)"
    if not ud._ask_yesno():
        break
    

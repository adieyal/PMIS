#from project.apps.projects import models
from _implementationprojectsaver import ImplementationProjectSaver

class RetentionProjectSaver(ImplementationProjectSaver):
    def save_planning(self, project, details):
        pass
        
    def save_submissions(self, project, details):
        pass

    def save_entities(self, project, details):
        pass

    def save_next_milestone(self, project, details):
        project.current_step = models.Milestone.final_accounts()
        project.save()

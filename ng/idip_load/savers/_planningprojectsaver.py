from _implementationprojectsaver import ImplementationProjectSaver

class PlanningProjectSaver(ImplementationProjectSaver):
    def save_next_milestone(self, project, details):
        print details
        milestone = self.ud.ask_next_milestone(details["comments"])
        project.current_step = milestone
        project.save()

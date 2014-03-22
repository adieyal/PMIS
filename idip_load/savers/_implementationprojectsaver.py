from backend import connection
from database import Project

class SaverException(Exception):
    pass

class ProjectSaver(object):
    def __init__(self, userdialog):
        self.ud = userdialog

    def save_project(self, client, details):
        p = Project(details)
        p.save()


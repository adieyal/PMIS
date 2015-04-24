from project.libs.database.database import Project

project_ids = Project.list()

print '%s rows found' % len(project_ids)

raise Hell

def findProject(p):
    for project in projects:
        if (project.cluster == p.cluster and
            project.district == p.district and
            project.municpality == p.municpality and
            project.name == p.description):
            return project

projects = []
for project_id in project_ids:
    project = Project.get(project_id)
    projects.append(project)

counter = 0
for project in projects:
    if not project.name:
        counter += 1

        if findProject(project):
            print 'Found project with same name as description'

        print '%s - %s: %s' % (project.timestamp, project.cluster, project.description)

print '%s rows found without names' % counter

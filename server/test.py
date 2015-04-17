from project.libs.database.database import Project

project_ids = Project.list()

print '%s rows found' % len(project_ids)

counter = 0

for project_id in project_ids:
    project = Project.get(project_id)

    if not project.name:
        counter += 1
        print '%s - %s: %s' % (project.timestamp, project.cluster, project.description)

print '%s rows found without names' % counter

from django.core.management.base import BaseCommand, CommandError

import xlrd
from uuid import uuid4
from datetime import datetime
from scripts.spreadsheet import Spreadsheet
from project.libs.database.database import Project


clusters = {
    'DoE': 'Education',
    'DoH': 'Health',
    'DSD': 'Social Development',
    'DCSR': 'Culture, Sports, Science and Recreation',
    'DCSSL': 'Community Safety, Security and Liaison'
}

fieldsOfInterest = {
    'cluster': [
        lambda cell: True,
        lambda cell, cluster_id: 'Department of %s' % clusters[cluster_id]
    ],
    'name': [
        lambda cell: 'Project' in cell.value and 'Name' in cell.value,
        lambda cell, cluster_id: splitIt(cell.value, 0) if cluster_id == 'DoH' else cell.value
    ],
    'description': [
        lambda cell: 'Project' in cell.value and 'Description' in cell.value,
        lambda cell, cluster_id: splitIt(cell.value, 1) if cluster_id == 'DoH' else cell.value
    ],
    'district': [
        lambda cell: 'District' in cell.value and 'Municipality' in cell.value,
        lambda cell, cluster_id: cell.value
    ],
    'municipality': [
        lambda cell: 'Local' in cell.value and 'Municipality' in cell.value,
        lambda cell, cluster_id: cell.value
    ],
    'source': [
        lambda cell: 'Funding' in cell.value and 'Source' in cell.value,
        lambda cell, cluster_id: cell.value
    ],
    'circuit': [
        lambda cell: 'Circuit' in cell.value,
        lambda cell, cluster_id: cell.value
    ],
    'implementing_agent': [
        lambda cell: 'Implementing' in cell.value and 'Agent' in cell.value,
        lambda cell, cluster_id: cell.value
    ]
}

class WorkBook(object):
    """
    Workbook class from spreadsheet module above, slightly rewritten
    so it doesn't use generators for the sheets collection.
    """
    def __init__(self, filename):
        self.workbook = xlrd.open_workbook(filename)

    def sheets(self):
        return [Spreadsheet(sheet, self.workbook.datemode) for sheet in self.workbook.sheets()]

def getProjectRange(sheet):
    """
    Return the start and stop rows for the projects, based on
    whether the first cell is a number or not
    """
    start = None
    stop = None

    nrows = sheet.nrows

    for rowx in range(nrows):
        row = sheet.row(rowx)

        if start is None:
            if row[0].ctype == xlrd.XL_CELL_NUMBER:
                start = rowx

        if start is not None:
            if row[0].ctype != xlrd.XL_CELL_NUMBER:
                stop = rowx
                break

    return (start, stop)

def getHeadingRow(sheet):
    """
    Locate the heading row by it's first cell with No or variants
    """
    nrows = sheet.nrows

    for rowx in range(nrows):
        row = sheet.row(rowx)

        if row[0].value in [ 'No', 'No.', 'Nr', 'Nr.' ]:
            return row

    return None

def splitIt(value, index):
    """
    Split a value by - and return the indexed item from the resulting array
    """
    parts = value.split('-')
    if len(parts) > index + 1:
        return parts[index]
    else:
        if index == 0:
            """
            If we are looking for name and there is not a split with '-'
            then use the whole field value as name instead
            """
            return value

def getColumnsOfInterest(sheet):
    """
    Loop through the cells in the heading row, looking for the
    fields we are interested in (by using a lambda)
    """
    headings = getHeadingRow(sheet)

    columnsOfInterest = {}
    for fieldName, lambdas in fieldsOfInterest.iteritems():
        for column, cell in enumerate(headings):
            if lambdas[0](cell):
                columnsOfInterest[fieldName] = column
                break

    return columnsOfInterest

projects = []
project_ids = Project.list()
for project_id in project_ids:
    project = Project.get(project_id)
    projects.append(project)

print '%s projects found' % len(projects)

def samify(value):
    if value is None:
        return ''
    else:
        return value.strip().lower()

def projectExists(project):
    for p in projects:
        if (samify(project['cluster']) == samify(p.cluster) and
            samify(project.get('name')) == samify(p.name) and
            samify(project['district']) == samify(p.district) and
            samify(project['municipality']) == samify(p.municipality)):
            return True
    return False

def insertProject(details):
    project = Project(details)
    project.save()

class Command(BaseCommand):
    args = 'filename'
    help = 'Imports projects from the combined cluster *.XLS spreadsheet'

    def handle(self, *args, **options):
        workbook = WorkBook(args[0])
        sheets = workbook.sheets()

        import_time = str(datetime.now())

        for sheet in sheets:
            cluster_id = sheet.name

            if cluster_id != 'Summary':
                columnsOfInterest = getColumnsOfInterest(sheet.sheet)

                (start, stop) = getProjectRange(sheet.sheet)

                for rowx in range(start, stop):
                    row = sheet.sheet.row(rowx)

                    year = datetime.today().year
                    month = datetime.today().month

                    if month < 3:
                        year -= 1

                    details = {
                        '_uuid': str(uuid4()),
                        'import_time': import_time,
                        'planning': [
                            { 'expenditure': None, 'progress': None, 'date': '%04d-04-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-05-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-06-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-07-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-08-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-09-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-10-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-11-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-12-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-01-01T00:00:00' % (year+1) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-02-01T00:00:00' % (year+1) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-03-01T00:00:00' % (year+1) },
                        ],
                        'actual': [
                            { 'expenditure': None, 'progress': None, 'date': '%04d-04-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-05-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-06-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-07-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-08-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-09-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-10-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-11-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-12-01T00:00:00' % (year) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-01-01T00:00:00' % (year+1) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-02-01T00:00:00' % (year+1) },
                            { 'expenditure': None, 'progress': None, 'date': '%04d-03-01T00:00:00' % (year+1) },
                        ]
                    }

                    for name, lambdas in fieldsOfInterest.iteritems():
                        if name in columnsOfInterest:
                            column = columnsOfInterest[name]
                            value = lambdas[1](row[column], cluster_id)
                            details[name] = value

                    if projectExists(details):
                        print "FOUND %s - %s" % (details['cluster'], details['name'])
                    else:
                        print "INSERT %s - %s" % (details['cluster'], details['name'])
                        insertProject(details)

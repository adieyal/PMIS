import xlrd
from scripts.spreadsheet import Spreadsheet

    
class WorkBook(object):
    def __init__(self, filename):
        self.workbook = xlrd.open_workbook(filename)

    def sheets(self):
        return [Spreadsheet(sheet, self.workbook.datemode) for sheet in self.workbook.sheets()]

workbook = WorkBook('spreadsheet.xlsx')
sheets = workbook.sheets()

def getProjectRange(sheet):
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
    nrows = sheet.nrows

    for rowx in range(nrows):
        row = sheet.row(rowx)

        if row[0].value in [ 'No', 'No.', 'Nr', 'Nr.' ]:
            return row

    return None

def splitIt(value, index):
    parts = value.split('-')
    if len(parts) > index + 1:
        return parts[index]

clusters = {
    'DoE': 'Education',
    'DoH': 'Health',
    'DSD': 'Social Development',
    'DCSR': 'Culture, Sport and Recreation',
    'DCSSL': 'Community, Security, Safety and Liaison'
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

def getColumnsOfInterest(sheet):
    headings = getHeadingRow(sheet)

    columnsOfInterest = {}
    for fieldName, lambdas in fieldsOfInterest.iteritems():
        for column, cell in enumerate(headings):
            if lambdas[0](cell):
                columnsOfInterest[fieldName] = column
                break

    return columnsOfInterest

for sheet in sheets:
    cluster_id = sheet.name

    if cluster_id != 'Summary':
        print 'cluster = %s' % sheet.name
        columnsOfInterest = getColumnsOfInterest(sheet.sheet)
        print 'fields of interest = %s' % fieldsOfInterest

        (start, stop) = getProjectRange(sheet.sheet)
        for rowx in range(start, stop):
            row = sheet.sheet.row(rowx)

            project = {}

            for name, lambdas in fieldsOfInterest.iteritems():
                if name in columnsOfInterest:
                    column = columnsOfInterest[name]
                    value = lambdas[1](row[column], cluster_id)
                    project[name] = value

            print project

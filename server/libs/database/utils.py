from dateutil import parser
from dateutil.relativedelta import relativedelta
from datetime import datetime
import json as json

monthdelta = relativedelta(months=1)
daydelta = relativedelta(days=1)

def to_float(x):
    try:
        return float(x)
    except ValueError:
        return 0

def dump_to_json(data):
    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else None
    return json.dumps(data, default=dthandler, indent=4)

def fyear(month, year):
    return (year + 1) if month > 3 else year 

def fmonths(fyear):
    financial_year_months = range(4, 13) + range(1, 4)
    return zip([fyear - 1] * 9 + [fyear] * 3, financial_year_months)

def to_date(dt):
    parts = dt.split()
    dt = parts[0] + " 20" + parts[1]
    dt = parser.parse(dt)
    dt = dt + monthdelta
    dt = datetime(dt.year, dt.month, 1)
    dt = dt - daydelta
    return dt

    


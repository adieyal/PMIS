from datetime import datetime
import json

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

from django.http import HttpResponse
from decimal import Decimal
import json

def handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return float(obj)
    else:
        raise TypeError, 'Object of type %s with value of %s is not JSON serializable' % (type(obj), repr(obj))

class JsonResponse(HttpResponse):
    def __init__(self, content={}, mimetype=None, status=None, content_type=None):
        if not content_type:
            content_type = 'application/json'
        super(JsonResponse, self).__init__(
            json.dumps(content, indent=4, default=handler), mimetype=mimetype, status=status, content_type=content_type
        )

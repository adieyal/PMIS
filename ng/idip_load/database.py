import json
import uuid
import time
from datetime import datetime
from uuid import uuid1, uuid4
from slugify import slugify

from backend import connection
from _utils import dump_to_json

__all__ = ['Project', 'DoesNotExistError']

# UUID v1 Custom Class

# get offset in seconds between the UUID timestamp Epoch (1582-10-15) and the Epoch used on this computer
DTD_SECS_DELTA = (datetime(*time.gmtime(0)[0:3])-datetime(1582, 10, 15)).days * 86400

class UUID(uuid.UUID):
    def timestamp(self):
        """Return a datetime.datetime object that represents the timestamp
        portion of a uuid1."""
        
        secs_uuid1 = self.time / 1e7
        secs_epoch = secs_uuid1 - DTD_SECS_DELTA
        return datetime.fromtimestamp(secs_epoch)

# Database access code

class DoesNotExistException(Exception):
    pass

class Project(object):
    _uuids = {}
    
    def __init__(self, details):
        self._details = details
    
    def _build_uuids(self):
        uuids = {}
        keys = connection.smembers('/project')
        if keys:
            items = [Project.get(uuid)._details for uuid in keys]
            for p in items:
                contract = p.get('contract', '').strip()
                description = p.get('description', '').strip()
                if contract != '':
                    uuids['contract:%s' % (contract)] = p['_uuid']
                if description != '':
                    uuids['description:%s' % (description)] = p['_uuid']
        return uuids
                    
    def _get_uuid(self):
        if self._details.has_key('_uuid'):
            return self._details['_uuid']
            
        contract = self._details.get('contract', '').strip()
        description = self._details.get('description', '').strip()
        
        if contract != '':
            if self._uuids.has_key('contract:%s' % (contract)):
                return self._uuids['contract:%s' % (contract)]
        
        if description != '':
            if self._uuids.has_key('description:%s' % (description)):
                return self._uuids['description:%s' % (description)]
        
        return str(uuid4())
        
    @property
    def _uuid(self):
        if not getattr(self, '__uuid', None):
            self.__uuid = self._get_uuid()
        return self.__uuid
        
    @property
    def _uuids(self):
        if not getattr(self, '__uuids', None):
            self.__uuids = self._build_uuids()
        return self.__uuids
        
    def revisions(self):
        revisions = connection.smembers('/project/%s' % (self._uuid))
        return revisions
        
    def save(self):
        uuid = self._uuid
        timestamp = str(uuid1())
        self._details['_uuid'] = uuid
        self._details['_timestamp'] = timestamp
        data = dump_to_json(self._details)
        connection.sadd('/project', uuid)
        connection.sadd('/project/%s' % (uuid), timestamp)
        connection.set('/project/%s/%s' % (uuid, timestamp), data)
    
    @classmethod
    def get(cls, uuid):
        revisions = connection.smembers('/project/%s' % (uuid))
        if not revisions:
            raise DoesNotExistException('There is no data for project %s.' % (uuid))

        revision_map = [{ 
            'timestamp': UUID(r.split('/')[-1]).timestamp(),
            'key': '/project/%s/%s' % (uuid, r)
        } for r in revisions]
        revision_map.sort(key=lambda x: x['timestamp'], reverse=True)
        
        data = connection.get(revision_map[0]['key'])
        details = json.loads(data)
        return cls(details)

        keys = connection.keys('/project/%s/*' % (uuid))
        if not keys:
            raise DoesNotExistException('There is no data for project %s.' % (uuid))
        
        timestamps = [{ 
            'timestamp': UUID(k.split('/')[-1]).timestamp(),
            'key': k
        } for k in keys]
        timestamps.sort(key=lambda x: x['timestamp'], reverse=True)
        
        data = connection.get(timestamps[0]['key'])
        details = json.loads(data)
        return cls(details)

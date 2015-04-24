# A simple singleton implementation for the Redis connection used to
# save all the data imported in the database. This should also make it
# easy to add any other storage backend using the python redis client
# api as a reference.

from django.conf import settings
import redis

connection = redis.Redis(**settings.REDIS)

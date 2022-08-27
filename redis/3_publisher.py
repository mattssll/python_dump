# publisher.py  - messages are not persisted
from conn import redis_connect


r = redis_connect()

r.publish('user-1', 'my data')
r.publish('user-2', 'new data')
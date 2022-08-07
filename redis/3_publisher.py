# publisher.py
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

r.publish('user-1', 'my data')
r.publish('user-2', 'new data')
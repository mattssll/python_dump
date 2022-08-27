# subscriber.py
import redis
import time
from conn import redis_connect


r = redis_connect()


p = r.pubsub()
p.psubscribe('user-*')  # subscribe to all user-* channels, where * is a wildcard


while True:
  message = p.get_message()
  if message:
    print(message)
  time.sleep(0.01)
# subscriber.py
import redis
import time


r = redis.Redis(host='localhost', port=6379, db=0)

p = r.pubsub()

# p.subscribe('user-1')  # subscribe to user-1 channel
p.psubscribe('user-*')  # subscribe to all user-* channels, where * is a wildcard

while True:
  message = p.get_message()
  if message:
    print(message)
  time.sleep(0.01)
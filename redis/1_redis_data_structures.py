import redis 
from client import redis_connect

redis = redis_connect()


# strings
redis.set('mykey', 'Hello from Python!')
value = redis.get('mykey')
print("printing my string \n", value)


# list
redis.lpush('mylist', 'Hello from Python!')
redis.lpush('mylist', 'first message')
redis.rpush('mylist', 'last message')
list_values = redis.lrange('mylist', 0, -1)
print("printing my list \n", list_values)


# set 
redis.sadd('myset', 'Hello from Python!')
redis.sadd('myset', 'second message')
set_values = redis.smembers('myset')
print("printing my set \n", set_values)

# sorted set
redis.zadd('vehicles', {'car' : 0})
redis.zadd('vehicles', {'bike' : 1})
vehicles = redis.zrange('vehicles', 0, -1)
print("printing my sorted set \n", vehicles)


# hashes (or dicts)
mydict = {'name' : 'John', 'age' : 30, 'children' : 0}
redis.hmset('myhash', mydict) # hmset is a convenience method for hset, same as hset('myhash', None, None, mydict)
dict_from_redis = redis.hgetall('myhash')
print("printing my dict/hash \n", dict_from_redis)


# clear all keys
redis.flushall()

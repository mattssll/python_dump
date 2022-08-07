#!/usr/bin/env python
from conn import get_connection


connection = get_connection()
channel = connection.channel()
# creates a queue named 'myqueue' if it doesn't already exist
channel.queue_declare(queue='myqueue')


channel.basic_publish(
    exchange='',  # special empty exchange for direct routing
    routing_key='myqueue',  
    body='Hello World!'
)

print(" [x] Sent 'Hello World!'")



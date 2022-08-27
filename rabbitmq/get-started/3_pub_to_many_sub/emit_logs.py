#!/usr/bin/env python
import pika
import sys
from conn import get_connection


#Steps
'''
1. Get Connection
2. Open Channel
3. Declare Exchange
4. Publish message to exchange - an empty routing key means exchange will send message to all queues
'''

connection = get_connection()
channel = connection.channel()

# Exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()
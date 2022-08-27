#!/usr/bin/env python
import pika
from conn import get_connection

# Steps
'''
1. Get Connection
2. Open Channel
3. Declare Exchange
4. Declare a random named Queue
5. Get queue name and bind it to the exchange within our channel
6. Define callback and Start consuming messages
'''

connection = get_connection()
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)  # starting a queue with a random name
# once consumer is closed then the queue is deleted
queue_name = result.method.queue  # retrieve our random queue name

channel.queue_bind(exchange='logs', queue=queue_name)

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

print(' [*] Waiting for logs. To exit press CTRL+C')
channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
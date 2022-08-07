import pika, sys
from conn import get_connection


connection = get_connection()
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel = connection.channel()
channel.queue_declare(queue='durable_queue', durable = True)
channel.basic_publish(
    exchange='',
    routing_key='durable_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
    )
)
print(f" [x] Sent {message}")
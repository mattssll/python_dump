#!/usr/bin/env python
import pika, sys, os, time
from conn import get_connection


def main():
    connection = get_connection()
    channel = connection.channel()
    # creates a queue named 'myqueue' if it doesn't already exist
    channel.queue_declare(queue='durable_queue', durable = True)


    def callback(ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        # Remove message from queue only after acknowledgement
        ch.basic_ack(delivery_tag = method.delivery_tag)

    channel.basic_qos(prefetch_count=1) # 1 message at a time across queues
    channel.basic_consume(queue='durable_queue', on_message_callback=callback)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
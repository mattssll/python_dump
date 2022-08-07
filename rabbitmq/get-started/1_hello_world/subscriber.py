#!/usr/bin/env python
import pika, sys, os
from conn import get_connection


def main():
    connection = get_connection()
    channel = connection.channel()
    # creates a queue named 'myqueue' if it doesn't already exist
    channel.queue_declare(queue='myqueue')

    def callback(ch, method, properties, body):
        """ This is the callback function that is called when a message is received. """
        print(f" [x] Received {body}")

    channel.basic_consume(queue='myqueue', on_message_callback=callback, auto_ack=True)  # auto_ack=True tells RabbitMQ to delete the message from the queue after it has been processed
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
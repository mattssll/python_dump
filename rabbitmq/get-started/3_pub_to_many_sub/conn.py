import pika


def get_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials('myuser', 'mypassword')
    parameters = pika.ConnectionParameters('localhost',5672,'/',credentials)
    connection = pika.BlockingConnection(parameters)
    return connection 

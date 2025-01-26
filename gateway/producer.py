import pika

def publish_message(message):
    # Connect to RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='test_queue', durable=True)
    print('publish message')
    # Publish a message to the queue
    channel.basic_publish(
        exchange='',
        routing_key='test_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        )
    )

    print(f" [x] Sent '{message}'")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    message = "Hello, RabbitMQ!"
    publish_message(message)
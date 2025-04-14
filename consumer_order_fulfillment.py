import pika
import json
from rabbitmq_config import RABBITMQ_HOST, EXCHANGE_NAME  # Importing constants

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f"[{order['student_name']}] Fulfillment: Order {order['order_id']} fulfilled. Events published.")
    
    # Send to order-fulfilled queue
    ch.basic_publish(exchange=EXCHANGE_NAME, routing_key='order-fulfilled', body=json.dumps(order))

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Declare exchange and queue
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
channel.queue_declare(queue='order-fulfillment')
channel.queue_bind(exchange=EXCHANGE_NAME, queue='order-fulfillment', routing_key='payment-applied')

# Start consuming messages
channel.basic_consume(queue='order-fulfillment', on_message_callback=callback, auto_ack=True)
print("Waiting for payment-applied events...")
channel.start_consuming()

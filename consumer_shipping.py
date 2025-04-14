import pika
import json
from rabbitmq_config import RABBITMQ_HOST, EXCHANGE_NAME

def callback(ch, method, properties, body):
    order = json.loads(body)
    print(f"[{order['student_name']}] Shipping: Order {order['order_id']} shipped. Events published.")
    
    # Send to order-shipped queue
    ch.basic_publish(exchange=EXCHANGE_NAME, routing_key='order-shipped', body=json.dumps(order))

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
channel = connection.channel()

# Declare exchange and queue
channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type='topic')
channel.queue_declare(queue='shipping')
channel.queue_bind(exchange=EXCHANGE_NAME, queue='shipping', routing_key='order-fulfilled')

# Start consuming messages
channel.basic_consume(queue='shipping', on_message_callback=callback, auto_ack=True)
print("Waiting for order-fulfilled events...")
channel.start_consuming()

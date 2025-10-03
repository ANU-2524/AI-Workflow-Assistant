from kafka import KafkaProducer
import json

def send_task_to_kafka(task_data):
    # Create the producer inside the function!
    producer = KafkaProducer(
        bootstrap_servers=['kafka:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    producer.send('tasks', task_data)
    producer.flush()

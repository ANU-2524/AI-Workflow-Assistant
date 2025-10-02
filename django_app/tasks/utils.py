from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_task_event(task_data):
    producer.send('tasks', task_data)
    producer.flush()

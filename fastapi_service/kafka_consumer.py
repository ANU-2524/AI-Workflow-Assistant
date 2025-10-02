from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'tasks',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='task_consumer_group'
)

for message in consumer:
    print("Received Task Event:", message.value)

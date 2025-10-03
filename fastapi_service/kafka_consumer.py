from kafka import KafkaConsumer
import json

import os

# KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")

consumer = KafkaConsumer(
    'tasks',
    bootstrap_servers = ['kafka:9092'] ,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='task-consumer-group'
)


print("Kafka consumer started, waiting for events...")
for message in consumer:
    print("Received task event:", message.value)

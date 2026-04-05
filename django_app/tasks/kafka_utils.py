"""
Kafka utilities for task event streaming.
Uses singleton pattern for producer efficiency.
"""

import json
import logging
import os
from kafka import KafkaProducer
from kafka.errors import KafkaError

logger = logging.getLogger(__name__)

# Singleton producer instance
_producer = None


def get_kafka_producer():
    """
    Get or create Kafka producer instance (singleton).
    
    Returns:
        KafkaProducer instance
    """
    global _producer
    
    if _producer is None:
        try:
            bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092').split(',')
            _producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                retries=3,
                max_in_flight_requests_per_connection=1,
            )
            logger.info(f"Kafka producer initialized with servers: {bootstrap_servers}")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {str(e)}")
            raise
    
    return _producer


def send_task_to_kafka(task_data: dict) -> None:
    """
    Send task event to Kafka.
    
    Args:
        task_data: Dictionary containing task information
        
    Raises:
        Exception: If message fails to send after retries
    """
    try:
        producer = get_kafka_producer()
        topic = os.getenv('KAFKA_TASKS_TOPIC', 'tasks')
        
        # Add timestamp for tracking
        task_data['sent_at'] = str(__import__('datetime').datetime.now().isoformat())
        
        future = producer.send(topic, task_data)
        
        # Wait for send to complete
        record_metadata = future.get(timeout=10)
        
        logger.info(
            f"Task sent to Kafka - Topic: {record_metadata.topic}, "
            f"Partition: {record_metadata.partition}, "
            f"Offset: {record_metadata.offset}"
        )
        
    except KafkaError as e:
        logger.error(f"Kafka error sending task: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error sending task to Kafka: {str(e)}")
        raise


def close_producer() -> None:
    """Close Kafka producer connection."""
    global _producer
    
    if _producer is not None:
        try:
            _producer.flush()
            _producer.close(timeout_ms=5000)
            logger.info("Kafka producer closed")
            _producer = None
        except Exception as e:
            logger.error(f"Error closing Kafka producer: {str(e)}")


"""
Kafka consumer module for FastAPI service.
Handles consumption of task and chat events from Kafka topics.
"""

import logging
import json
import os
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from typing import Callable, Optional

logger = logging.getLogger(__name__)


class KafkaTaskConsumer:
    """Kafka consumer for task events."""
    
    def __init__(self, group_id: str = "tasks-consumer"):
        """
        Initialize Kafka consumer.
        
        Args:
            group_id: Consumer group ID
        """
        try:
            bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092').split(',')
            self.consumer = KafkaConsumer(
                os.getenv('KAFKA_TASKS_TOPIC', 'tasks'),
                bootstrap_servers=bootstrap_servers,
                group_id=group_id,
                value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                max_poll_records=100,
            )
            logger.info(f"Kafka consumer initialized for tasks topic with group: {group_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer: {str(e)}")
            raise
    
    def consume_messages(self, callback: Callable, timeout_ms: int = 1000):
        """
        Consume messages from Kafka and apply callback.
        
        Args:
            callback: Function to call for each message
            timeout_ms: Poll timeout in milliseconds
        """
        try:
            for message in self.consumer:
                try:
                    callback(message.value)
                    logger.debug(f"Processed message: {message.value}")
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
        except KafkaError as e:
            logger.error(f"Kafka error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
    
    def close(self):
        """Close Kafka consumer."""
        try:
            self.consumer.close()
            logger.info("Kafka consumer closed")
        except Exception as e:
            logger.error(f"Error closing Kafka consumer: {str(e)}")


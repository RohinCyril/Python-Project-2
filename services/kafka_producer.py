import json
from kafka import KafkaProducer

from config import KAFKA_SERVER


producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


def publish_message(topic, message):
    """
    Publish message to Kafka topic.
    """

    producer.send(topic, message)
    producer.flush()
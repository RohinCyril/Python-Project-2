from services.kafka_producer import publish_message
from config import KAFKA_TOPIC


def track_event(data):
    """
    Publish analytics event to Kafka.
    """

    publish_message(KAFKA_TOPIC, data)

    return {
        "status": "success",
        "message": "Analytics event published"
    }
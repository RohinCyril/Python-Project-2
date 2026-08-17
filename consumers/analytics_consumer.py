import json
import logging
import os
import time

import psycopg2
from kafka import KafkaConsumer
from psycopg2 import sql


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092"
)

KAFKA_TOPIC = os.getenv(
    "KAFKA_TOPIC",
    "analytics"
)

KAFKA_GROUP_ID = os.getenv(
    "KAFKA_GROUP_ID",
    "analytics-consumer-group"
)

POSTGRES_HOST = os.getenv(
    "POSTGRES_HOST",
    "localhost"
)

POSTGRES_PORT = os.getenv(
    "POSTGRES_PORT",
    "5432"
)

POSTGRES_DB = os.getenv(
    "POSTGRES_DB",
    "video_analytics"
)

POSTGRES_USER = os.getenv(
    "POSTGRES_USER",
    "postgres"
)

POSTGRES_PASSWORD = os.getenv(
    "POSTGRES_PASSWORD",
    "postgres"
)


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# PostgreSQL connection
# ---------------------------------------------------------

def get_db_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )


# ---------------------------------------------------------
# Create analytics table
# ---------------------------------------------------------

def create_table(connection):
    """
    Create the video_analytics table if it does not exist.
    """

    query = """
        CREATE TABLE IF NOT EXISTS video_analytics (
            video_id VARCHAR(255) PRIMARY KEY,
            total_views INTEGER DEFAULT 0,
            total_buffers INTEGER DEFAULT 0,
            total_plays INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """

    with connection.cursor() as cursor:
        cursor.execute(query)

    connection.commit()

    logger.info("Analytics table is ready.")


# ---------------------------------------------------------
# Update analytics
# ---------------------------------------------------------

def update_analytics(connection, video_id, event):
    """
    Update analytics for a video based on the Kafka event.
    """

    views = 1 if event == "view" else 0
    buffers = 1 if event == "buffer" else 0
    plays = 1 if event == "play" else 0

    query = """
        INSERT INTO video_analytics (
            video_id,
            total_views,
            total_buffers,
            total_plays,
            updated_at
        )
        VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)

        ON CONFLICT (video_id)
        DO UPDATE SET
            total_views = video_analytics.total_views + EXCLUDED.total_views,
            total_buffers = video_analytics.total_buffers + EXCLUDED.total_buffers,
            total_plays = video_analytics.total_plays + EXCLUDED.total_plays,
            updated_at = CURRENT_TIMESTAMP;
    """

    with connection.cursor() as cursor:
        cursor.execute(
            query,
            (
                video_id,
                views,
                buffers,
                plays
            )
        )

    connection.commit()

    logger.info(
        "Updated analytics: video_id=%s, event=%s",
        video_id,
        event
    )


# ---------------------------------------------------------
# Validate Kafka event
# ---------------------------------------------------------

def validate_event(data):
    """
    Validate the structure of an analytics event.
    """

    if not isinstance(data, dict):
        return False

    if "video_id" not in data:
        return False

    if "event" not in data:
        return False

    if not data["video_id"]:
        return False

    if not data["event"]:
        return False

    return True


# ---------------------------------------------------------
# Process Kafka message
# ---------------------------------------------------------

def process_message(connection, message):
    """
    Process one Kafka message.
    """

    try:
        data = json.loads(message.value.decode("utf-8"))

    except json.JSONDecodeError:
        logger.error(
            "Invalid JSON received: %s",
            message.value
        )
        return

    if not validate_event(data):
        logger.warning(
            "Invalid analytics event: %s",
            data
        )
        return

    video_id = str(data["video_id"])
    event = str(data["event"]).lower()

    update_analytics(
        connection,
        video_id,
        event
    )


# ---------------------------------------------------------
# Start Kafka consumer
# ---------------------------------------------------------

def create_consumer():
    """
    Create and return a Kafka consumer.
    """

    return KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=KAFKA_GROUP_ID,
        auto_offset_reset="earliest",
        enable_auto_commit=True
    )


# ---------------------------------------------------------
# Main consumer loop
# ---------------------------------------------------------

def main():
    """
    Start the analytics consumer.
    """

    logger.info("Starting Analytics Kafka Consumer...")

    connection = None
    consumer = None

    while connection is None:
        try:
            connection = get_db_connection()

            logger.info(
                "Connected to PostgreSQL at %s:%s",
                POSTGRES_HOST,
                POSTGRES_PORT
            )

        except psycopg2.OperationalError as error:
            logger.warning(
                "PostgreSQL is not ready: %s",
                error
            )

            time.sleep(5)

    create_table(connection)

    while consumer is None:
        try:
            consumer = create_consumer()

            logger.info(
                "Connected to Kafka at %s",
                KAFKA_BOOTSTRAP_SERVERS
            )

            logger.info(
                "Subscribed to topic: %s",
                KAFKA_TOPIC
            )

        except Exception as error:
            logger.warning(
                "Kafka is not ready: %s",
                error
            )

            time.sleep(5)

    try:
        logger.info("Waiting for analytics events...")

        for message in consumer:
            logger.info(
                "Received Kafka message: topic=%s partition=%s offset=%s",
                message.topic,
                message.partition,
                message.offset
            )

            try:
                process_message(
                    connection,
                    message
                )

            except Exception as error:
                connection.rollback()

                logger.exception(
                    "Error processing message: %s",
                    error
                )

    except KeyboardInterrupt:
        logger.info("Consumer stopped by user.")

    finally:
        if consumer:
            consumer.close()

        if connection:
            connection.close()

        logger.info("Consumer shutdown complete.")


# ---------------------------------------------------------
# Application entry point
# ---------------------------------------------------------

if __name__ == "__main__":
    main()
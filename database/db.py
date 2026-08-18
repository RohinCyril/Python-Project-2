import os
import logging

import psycopg2


logger = logging.getLogger(__name__)


def get_db_connection():
    """
    Create and return a PostgreSQL database connection.
    """

    connection = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        database=os.getenv("POSTGRES_DB", "video_analytics"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "postgres")
    )

    logger.info("Connected to PostgreSQL")

    return connection


def close_db_connection(connection):
    """
    Close the PostgreSQL database connection.
    """

    if connection:
        connection.close()
        logger.info("PostgreSQL connection closed.")


def create_analytics_table(connection):
    """
    Create the video analytics table if it does not already exist.
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

    try:
        with connection.cursor() as cursor:
            cursor.execute(query)

        connection.commit()

        logger.info("video_analytics table is ready.")

    except Exception as error:
        connection.rollback()

        logger.error(
            "Failed to create analytics table: %s",
            error
        )

        raise
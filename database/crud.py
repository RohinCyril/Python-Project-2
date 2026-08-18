import logging


logger = logging.getLogger(__name__)


def upsert_video_analytics(
    connection,
    video_id,
    event
):
    """
    Insert or update analytics for a video.

    Supported events:
        - view
        - buffer
        - play
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
        VALUES (
            %s,
            %s,
            %s,
            %s,
            CURRENT_TIMESTAMP
        )

        ON CONFLICT (video_id)
        DO UPDATE SET
            total_views =
                video_analytics.total_views
                + EXCLUDED.total_views,

            total_buffers =
                video_analytics.total_buffers
                + EXCLUDED.total_buffers,

            total_plays =
                video_analytics.total_plays
                + EXCLUDED.total_plays,

            updated_at = CURRENT_TIMESTAMP;
    """

    try:
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
            "Analytics updated: video_id=%s, event=%s",
            video_id,
            event
        )

    except Exception as error:
        connection.rollback()

        logger.error(
            "Failed to update analytics: %s",
            error
        )

        raise


def get_video_analytics(connection, video_id):
    """
    Retrieve analytics for a specific video.
    """

    query = """
        SELECT
            video_id,
            total_views,
            total_buffers,
            total_plays,
            updated_at
        FROM video_analytics
        WHERE video_id = %s;
    """

    with connection.cursor() as cursor:
        cursor.execute(query, (video_id,))
        result = cursor.fetchone()

    if result is None:
        return None

    return {
        "video_id": result[0],
        "total_views": result[1],
        "total_buffers": result[2],
        "total_plays": result[3],
        "updated_at": result[4]
    }


def get_all_video_analytics(connection):
    """
    Retrieve analytics for all videos.
    """

    query = """
        SELECT
            video_id,
            total_views,
            total_buffers,
            total_plays,
            updated_at
        FROM video_analytics
        ORDER BY total_views DESC;
    """

    with connection.cursor() as cursor:
        cursor.execute(query)
        results = cursor.fetchall()

    return [
        {
            "video_id": row[0],
            "total_views": row[1],
            "total_buffers": row[2],
            "total_plays": row[3],
            "updated_at": row[4]
        }
        for row in results
    ]
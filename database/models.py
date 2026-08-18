from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class VideoAnalytics:
    """
    Represents aggregated analytics for a video.
    """

    video_id: str
    total_views: int = 0
    total_buffers: int = 0
    total_plays: int = 0
    updated_at: Optional[datetime] = None

    def to_dict(self):
        """
        Convert the model to a dictionary.
        """

        return {
            "video_id": self.video_id,
            "total_views": self.total_views,
            "total_buffers": self.total_buffers,
            "total_plays": self.total_plays,
            "updated_at": self.updated_at
        }
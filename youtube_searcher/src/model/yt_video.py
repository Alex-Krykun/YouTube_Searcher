from dataclasses import dataclass


@dataclass
class YTVideo:
    video_id: str
    title: str
    context: str = ""

    @property
    def url(self):
        return f"https://www.youtube.com/watch?v={self.video_id}"

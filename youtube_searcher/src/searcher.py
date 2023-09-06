import re
import logging
from typing import List, Optional

from youtube_transcript_api import YouTubeTranscriptApi

from youtube_searcher.src.model.yt_video import YTVideo
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build


class YTSearcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.youtube_client = build("youtube", "v3", developerKey=api_key)

    def _get_channel_id_by_name(self, channel_name: str) -> Optional[str]:
        try:
            search_response = (
                self.youtube_client.search()
                .list(q=channel_name, type="channel", part="id")
                .execute()
            )

            if "items" in search_response:
                channel_id = search_response["items"][0]["id"]["channelId"]
                return channel_id

        except HttpError as e:
            logging.error(f"Error during getting channel_id {e=}")

        return None

    def _get_all_video_from_channel_id(self, channel_id: str) -> List[YTVideo]:
        videos = []

        try:
            channel_response = (
                self.youtube_client.channels()
                .list(part="contentDetails", id=channel_id)
                .execute()
            )

            uploads_playlist_id = channel_response["items"][0]["contentDetails"][
                "relatedPlaylists"
            ]["uploads"]

            playlist_items = self.youtube_client.playlistItems().list(
                part="contentDetails,snippet",
                maxResults=50,  # Adjust as needed
                playlistId=uploads_playlist_id,
            )

            while playlist_items:
                playlist_response = playlist_items.execute()

                for item in playlist_response["items"]:
                    video_id = item["contentDetails"]["videoId"]
                    video_title = item["snippet"]["title"]
                    videos.append(YTVideo(video_id=video_id, title=video_title))

                # Continue to the next page, if available
                playlist_items = self.youtube_client.playlistItems().list_next(
                    playlist_items, playlist_response
                )

        except HttpError as e:
            logging.error(f"Error during getting videos from channel {e=}")

        logging.info(f"Found {len(videos)} videos from {channel_id}")
        return videos

    def get_all_videos_where(
        self, channel_name: str, search_pattern: str, fast_search=False
    ) -> List[YTVideo]:
        channel_id = self._get_channel_id_by_name(channel_name)
        videos = self._get_all_video_from_channel_id(channel_id)

        count = 1
        for video in videos:
            logging.info(f"Processing video {count}/{len(videos)}")
            count += 1
            if re.search(search_pattern, video.title):
                logging.info(f"Found pattern in title of video {video.title=}")

                video.context = "Title"
                yield video
                continue

            subtitles = []
            try:
                subtitles = YouTubeTranscriptApi.get_transcript(video.video_id)
            except HttpError as e:
                logging.error(
                    f"Error during getting video transcript {e=} {video.video_id=}"
                )

            if fast_search:
                subtitles = subtitles[:500]

            for i, subtitle in enumerate(subtitles):
                if re.search(search_pattern, subtitle["text"]):
                    current_sub = subtitle["text"]
                    prev_sub = subtitles[i - 1]["text"] if i > 0 else ""
                    next_sub = (
                        subtitles[i + 1]["text"] if i < len(subtitles) - 1 else ""
                    )
                    video.context = (
                        f"{subtitle['start']}: {prev_sub}, {current_sub}, {next_sub}"
                    )
                    logging.info(
                        f"Found pattern in title of video {video.title=} {video.context}"
                    )
                    yield video
                    break

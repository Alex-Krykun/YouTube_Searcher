import argparse
from youtube_searcher.src.searcher import YTSearcher


def main():
    parser = argparse.ArgumentParser(description="Retrieve YouTube videos from.")

    parser.add_argument("-key", "--api_key", type=str, required=True, help="The YouTube API KEY.")
    parser.add_argument("-c", "--channel_name", type=str, required=True, help="The YouTube channel name.")
    parser.add_argument("-s", "--search", type=str, required=True, help="World that should contain in video.")
    parser.add_argument("-r", "--result_path", type=str, default="result.txt", help="File where to put result")
    parser.add_argument("-f", "--fast_search", type=bool, default=False, help="Scan only first 500 subtitles")

    # Parse the command-line arguments
    args = parser.parse_args()
    api_key = args.api_key
    channel_name = args.channel_name
    fast_search = args.fast_search
    search_world = args.search
    result_path = args.result_path

    searcher = YTSearcher(api_key)

    with open(result_path, "w") as file:
        for video in searcher.get_all_videos_where(channel_name, search_world, fast_search):
            file.write(f"{video.title=}, {video.url}")
            file.write("\n")


if __name__ == "__main__":
    main()

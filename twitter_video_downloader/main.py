import argparse
import logging
from twitter_video_downloader.downloader import TwitterVideoDownloader

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="twitter-video-downloader — by Richard Mwewa  | https://about.me/rly0nheart")
    parser.add_argument("url", help="twitter video url (eg. https://twitter.com/i/status/0101011010010101101")
    args = parser.parse_args()
    logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%H:%M:%S%p', level=logging.DEBUG)
    TwitterVideoDownloader().download_video(args.url)

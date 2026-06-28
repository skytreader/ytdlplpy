import logging
import re
import redis
import socket
import sys
import yt_dlp as youtube_dl

from urllib.error import HTTPError

LIST_NAME = "YTDLPLQ"
DL_DEST = "/root/Videos/ytdlpl"

HTTP_STATUS_ERROR_REGEX = re.compile(r".*HTTP\s+Error\s+(\d+).*")
MAX_FAIL_COUNT = 10
FAIL_COUNTS = {}

logger = logging.getLogger("ytdl")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def parse_http_error(error_msg):
    codeparse = HTTP_STATUS_ERROR_REGEX.match(error_msg)
    if codeparse:
        return int(codeparse.group(1))

    return None

if __name__ == "__main__":
    redis_client = redis.Redis(host="redis", port=6379, db=0)
    ytdl_opts = {
        "outtmpl": DL_DEST + "/%(title)s.%(ext)s",
        "writesubtitles": True,
        "subtitleslangs": ["en"],
        "extractor_args": {
            "generic": {
                "impersonate": [""]
            }
        }
    }
    
    while True:
        logger.info("Waiting for an URL...")
        url = redis_client.blpop(LIST_NAME)
        url = url[1].decode("utf-8")
        FAIL_COUNTS[url] = 0
        logger.info("Got %s, downloading..." % url)
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            try:
                ydl.download([url])
            except HTTPError as httpe:
                logger.exception("Ooops. HTTP error encountered.")

                if httpe.code in (503, 504):
                    logger.info("code is retriable, re-enqueueing...")
                    FAIL_COUNTS[url] += 1
                    if FAIL_COUNTS[url] < MAX_FAIL_COUNT:
                        redis_client.rpush(LIST_NAME, url)
                    else:
                        logger.error("%s has been retried too many times, retiring..." % url)
                else:
                    logger.info("%s can't be retried." % url)
            except socket.gaierror as GAIError:
                logger.exception("Socket error occurred. Probably retriable...")
                FAIL_COUNTS[url] += 1
                if FAIL_COUNTS[url] < MAX_FAIL_COUNT:
                    redis_client.rpush(LIST_NAME, url)
                else:
                    logger.error("%s has been retried too many times, retiring..." % url)
            except youtube_dl.utils.DownloadError as DLError:
                http_status = parse_http_error(sys.exc_info()[1].msg)
                if http_status is not None and 400 <= http_status <= 499:
                    logger.error("Fetching video data failed with client error: %s. Will NOT retry." % http_status)
                else:
                    logger.exception("Super generic error. Will attempt retry...")
                    FAIL_COUNTS[url] += 1
                    if FAIL_COUNTS[url] < MAX_FAIL_COUNT:
                        redis_client.rpush(LIST_NAME, url)
                    else:
                        logger.error("%s has been retried too many times, retiring..." % url)

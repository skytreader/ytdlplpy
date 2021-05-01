import logging
import redis
import socket
import youtube_dl

from urllib.error import HTTPError

LIST_NAME = "YTDLPLQ"
DL_DEST = "/root/Videos/ytdlpl"

logger = logging.getLogger("ytdl")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

if __name__ == "__main__":
    redis_client = redis.Redis(host="redis", port=6379, db=0)
    ytdl_opts = {
        "outtmpl": DL_DEST + "/%(title)s.%(ext)s"
    }
    
    while True:
        logger.info("Waiting for an URL...")
        url = redis_client.blpop(LIST_NAME)
        url = url[1].decode("utf-8")
        logger.info("Got %s, downloading..." % url)
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            try:
                ydl.download([url])
            except HTTPError as httpe:
                logger.exception("Ooops. HTTP error encountered.")

                if httpe.code in (503, 504):
                    logger.info("code is retriable, re-enqueueing...")
                    redis_client.rpush(LIST_NAME, url)
                else:
                    logger.info("%s can't be retried." % url)
            except socket.gaierror as GAIError:
                logger.exception("Socker error occurred. Probably retriable...")
                redis_client.rpush(LIST_NAME, url)
            except youtube_dl.utils.DownloadError as DLError:
                logger.exception("Super generic error. Will attempt retry...")
                redis_client.rpush(LIST_NAME, url)

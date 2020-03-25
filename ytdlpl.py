import logging
import redis
import youtube_dl

LIST_NAME = "YTDLPLQ"
DL_DEST = "~/Videos/ytdlplx"

logger = logging.getLogger("ytdl")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

if __name__ == "__main__":
    redis_client = redis.Redis(host="redis", port=6379, db=0)
    ytdl_opts = {
        "outtmpl": "~/Videos/%(title)s.%(ext)s"
    }
    
    while True:
        logger.info("Waiting for an URL...")
        url = redis_client.blpop(LIST_NAME)
        url = url[1].decode("utf-8")
        logger.info("Got %s, downloading..." % url)
        with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
            # TODO error handling
            ydl.download([url])

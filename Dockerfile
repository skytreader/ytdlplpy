FROM python:3.14.10-alpine3.24
RUN apk add --no-cache ffmpeg git gcc g++ make libffi-dev openssl-dev npm
RUN mkdir -p /root/Videos/ytdlpl
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./ ./ytdlpl
WORKDIR ./ytdlpl
ENTRYPOINT python ytdlpl.py

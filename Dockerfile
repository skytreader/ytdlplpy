FROM python:3.10.6-alpine3.16
RUN apk add --no-cache ffmpeg git gcc g++ make libffi-dev openssl-dev
RUN mkdir -p /root/Videos/ytdlpl
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY ./ ./ytdlpl
WORKDIR ./ytdlpl
ENTRYPOINT python ytdlpl.py

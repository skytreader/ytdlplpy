# ytdlpl

A "playlist" maker for [youtube-dl](https://github.com/ytdl-org/youtube-dl).

## Problem

youtube-dl is versatile enough that it can download whole playlists off YouTube.
It is also versatile enough to work on websites that don't offer a playlist
functionality like YouTube.

(Or, maybe, you just holding out on making a Google account. Whatever.)

ytdlpl (does the name make sense now?) lets you queue up URLs for download,
kind of like building up a playlist as you go.

This was conceived March 2020 while I'm staying at home, helping #flattenthecurve.

## Installation and Usage

Needs you to have Docker and Docker Compose installed. All the commands in this
section are ran from this directory. `sudo` probably necessary.

Install:

```
docker-compose up
```

This will run a daemon-type process that will download video files from
supported URLs in the background. By default the files will be downloaded to
`~/Videos/ytdlpl`.

To enqueue a URL for downloading, simply

```
./ytdlplnq https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## License

MIT

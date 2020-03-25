# ytdlpl

A "playlist" maker for [youtube-dl](https://github.com/ytdl-org/youtube-dl).

## Problem

youtube-dl is versatile enough that it can download whole playlists off YouTube.
It is also versatile enough to work on websites other than YouTube that may not
offer a playlist functionality.

(Or, maybe, you're just holding out on making a Google account. Or you are 
downloading from various sources. Whatever.)

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

Note that there are a lot of options to customize youtube-dl's behavior but
such pass-through behavior is not yet implemented here.

## Configuration

**Note:** Needs you to be comfortable with editing and running `docker-compose`.

I want to

- **change the location where my videos are downloaded:** Edit the `volumes`
mounted by the `ytdlpl` service, map your desired directory location to
`/root/Videos/ytdlpl` of the service's image.

## License

MIT

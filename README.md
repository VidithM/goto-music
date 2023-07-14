# goto-music
Ever tired of having to skip the opening of YouTube music videos to get to the song? Fear no more, goto-music has you covered!

## Components
* Browser Plugin - automatically detects a skippable YouTube music video (a video that has been processed and recorded in the database)
* Backend - pulls songs from Billboard Hot 100 across a period of several years, fetches their audio and music videos from YouTube, and finds the skippable portion of the video.

## Credits
github.com/itspoma/audio-fingerprint-identifying-python

This codebase is used throughout this project for Fourier transform/spectogram analysis/matching audio hashes, all of which are used here in order to determine the skippable portion of the music video.

## References
https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf

## FAQ
### How do I run the backend?
* `handle_request.py` is the entry point that reads song names from `songs.out`, fetches their audio/video files, and finds the start point.
### Some of the Python packages used in this project (i.e `pafy`, `youtube_dl`, etc.) are not working correctly. Why?
* Some of these packages are not compatible with Python 3.10+. Please run with Python 3.9. In addition, you may run across some exceptions in `pafy` with KeyErrors with keys such as `average_rating`. This is a current bug with `pafy` that must be fixed. In the meantime, what worked for me was modifying [this file](https://github.com/mps-youtube/pafy/blob/develop/pafy/backend_youtube_dl.py) on lines 47-58 as needed to use `.get()` with a default value. 
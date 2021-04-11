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

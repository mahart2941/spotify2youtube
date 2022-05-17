# spotify2youtube

WIP script to transfer my spotify playlists to youtube music

Might expand in the future. YMMV


## Installation

The project is created using `poetry`, which will take care of both installing and creating a virtual environment for you.

First, clone the repo

```bash
git clone git@github.com:mahart2941/spotify2youtube.git
cd spotify2youtube
```
Install poetry if not already installed

```bash
pip install poetry
```

If you would like the virtual environment to be installed at the folder itself, run the following command to change your poetry configuration:

```bash
poetry config virtualenvs.in-project true
```
The `-- local` flag, if provided, will apply the config change just to this specific project.

And then install the dependencies:

```bash
poetry install
```

Setup authentication to youtube and spotify
1. Youtube: The script assumes you followed: https://ytmusicapi.readthedocs.io/en/latest/setup.html and created the headers_auth.json in this directory
2. Spotify: The script assumes you've created environmental variables SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET generated from https://developer.spotify.com/dashboard/

Make the desired changes to the variables SPOTIFY_PLAYLIST_ID, YOUTUBE_PLAYLIST_NAME, and YOUTUBE_PLAYLIST_DESCRIPTION


```bash
poetry run python main.py
import os
import spotipy
import logging
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic
from utils import get_spotify_tracks, get_song_search_string, parse_vid

# Fill in as needed
SPOTIFY_PLAYLIST_ID = 'SPID'
YOUTUBE_PLAYLIST_NAME = 'NAME'
YOUTUBE_PLAYLIST_DESCRIPTION = 'DESC'

# Assumes you've created environmental variables from
# https://developer.spotify.com/dashboard/
CID = os.environ.get('SPOTIFY_CLIENT_ID')
CS = os.environ.get('SPOTIFY_CLIENT_SECRET')

# Assumes you followed: https://ytmusicapi.readthedocs.io/en/latest/setup.html
yt = YTMusic('headers_auth.json')
manager = SpotifyClientCredentials(client_id=CID, client_secret=CS)
sp = spotipy.Spotify(auth_manager=manager)

# logging
logging.basicConfig(
    filename='info.log', filemode='w',
    format='%(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    ids = []
    spotify_tracks = get_spotify_tracks(sp, SPOTIFY_PLAYLIST_ID)

    for track in spotify_tracks:
        song_search_string = get_song_search_string(track)
        # TODO determine if and when rate limiting occurs for
        # hitting the search endpoint. Handle as needed.
        # the limit parameter of the search function does not seem to work so
        # slice the response
        song_results = yt.search(query=song_search_string, filter='songs')[0:3]
        video_id = parse_vid(song_results)
        if video_id:
            ids.append(video_id)
    logging.info(f'Found: {len(ids)} videoIds. Attempting to create playlist')
    # TODO determine what the max number of video_ids you can send to
    # create/playlist endpoint at once.
    response = yt.create_playlist(
        title=YOUTUBE_PLAYLIST_NAME,
        description=YOUTUBE_PLAYLIST_DESCRIPTION,
        video_ids=ids
    )
    logging.info(response)


if __name__ == "__main__":
    main()

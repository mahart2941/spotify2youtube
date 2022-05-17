import os
import spotipy
import logging
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic
from typing import List
from utils import * # noqa

# Assumes you've created environmental variables from https://developer.spotify.com/dashboard/
CID = os.environ.get('SPOTIFY_CLIENT_ID')
CS = os.environ.get('SPOTIFY_CLIENT_SECRET')

auth_manager = SpotifyClientCredentials(client_id=CID,client_secret=CS)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Assumes you followed: https://ytmusicapi.readthedocs.io/en/latest/setup.html
yt = YTMusic('headers_auth.json')

logging.basicConfig(filename='info.log', filemode='w', format='%(levelname)s - %(message)s', level=logging.INFO)

SPOTIFY_PLAYLIST_ID = '2iS9UxbzovWxLbpLvKvs8V'
YOUTUBE_PLAYLIST_NAME = 'Sanch Test'
YOUTUBE_PLAYLIST_DESCRIPTION = 'pog'
YOUTUBE_PLAYLIST_ID = yt.create_playlist(YOUTUBE_PLAYLIST_NAME,YOUTUBE_PLAYLIST_DESCRIPTION)

def main():
    ids = []
    spotify_tracks = get_spotify_tracks(sp, SPOTIFY_PLAYLIST_ID)
    print(len(spotify_tracks))
    for track in spotify_tracks:
        song_search_string = get_song_search_string(track)
        # the limit parameter of search does not seem to work so slice the response
        song_results = yt.search(query=song_search_string, filter='songs')[0:3]
        video_id = parse_vid(song_results)
        if video_id:
            ids.append(video_id)
    logging.info(f'Found: {len(ids)} videoIds. Attempting to create playlist')
    response = yt.create_playlist(title=YOUTUBE_PLAYLIST_NAME,description=YOUTUBE_PLAYLIST_DESCRIPTION,video_ids=ids)
    logging.info(response)

if __name__ == "__main__":
    main()
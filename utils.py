import logging
import spotipy
from typing import List, Optional


log = logging.getLogger(__name__)

'''
TODO: get_song_search_string() is super simple but works. could be improved by
comparing attributes of the spotify track and youtube song (name, artists,
seconds duration, explicit bool, release/upload date)
Sigma does this here:
https://github.com/sigma67/spotifyplaylist_to_ytmusic/blob/b08f3b5b0b6b2d0f3d87686fb9a1e6a848c92684/YouTube.py#L21
'''


def get_song_search_string(song_dict: dict) -> str:
    """Parses a Spotify API song dictionary and returns a string joining the
    name and all artists

    Example: Return to Oz by Monolink, ARTBAT

    Args:
        song_dict (dict): the `track` dictionary that the Spotify API returns.
        The default returned fields should contain name and artists

    Returns:
        str: the song search string
    """

    '''
    Split the name on `(` to get the song base name removing extra info.
    Example: Mother Nature (feat. NOISY). We don't need to know featured
    artists as it will be in the artists dict. May cause issues for more
    niche songs.
    '''
    song_name = song_dict['name'].split(' (')[0]
    song_artists = ', '.join([artist['name'] for artist in song_dict['artists']])
    logging.info(f'Created song string: {song_name} by {song_artists}')
    return(f"{song_name} by {song_artists}")


def parse_vid(songs: list) -> Optional[str]:
    """Attempts to find a videoId given a list of songs

    Args:
        songs (list): list of song dictionaries returned by Youtube Music API

    Returns:
        str: the videoId
    """
    for i, song in enumerate(songs):
        vid = song.get('videoId')
        if vid:
            logging.info(f'Found videoId in index: {i} -> {vid}')
            return vid

        return None


def get_spotify_tracks(spotify_client: spotipy.Spotify, spotify_id: str) -> List[dict]:
    """Get all tracks from the given spotify playlist id
    Args:
        spotify_client (spotipy.Spotify): Spotify Client object
        spotify_id (str): The spotify guid for the playlis

    Returns:
        List[dict]: A list of track dictionaries which will include
        track name and track artists
    """
    '''create a range for the number of requests it will take to get total
    tracks in a playlist. max requested tracks at a time is 100'''
    total_songs = spotify_client.playlist_items(spotify_id, fields='total')['total']
    iteration_range = range(int(total_songs)/100 + 1)
    playlist_tracks = []

    offset = 0
    for i in iteration_range:
        ''' fields to expand on later: items.track.name,
        items.track.artists.name, items.track.duration_ms,
        items.track.release_date, items.track.explicit'''
        current_tracks = spotify_client.playlist_items(
            spotify_id, fields='items.track.name, items.track.artists.name',
            offset=offset
        )['items']
        '''"flatten" results so that each dict in the playlist tracks list
        just contains a dict with the keys: name, artists'''
        playlist_tracks.extend([track['track'] for track in current_tracks])
        offset += 100
    logging.info(f'We found a total of: {len(playlist_tracks)} songs')
    return playlist_tracks

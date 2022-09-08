from pprint import pprint
import requests
from secrets import *
import base64, json
import pandas as pd

auth_URL = "https://accounts.spotify.com/api/token"
auth_header = {}
auth_data = {}


def get_access_token(client_id, client_secret):
    """
    Takes secrets and generates a Client Credentials Flow access token.

    :param client_id: Spotify's API app client ID.
    :param client_secret: Spotify's API app secret ID.

    :return: Client Credentials Flow access token.
    """
    # Base64 encode Client ID and Client Secret...
    message = f"{CLIENT_ID}:{CLIENT_SECRET}"
    message_bytes = message.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode("ascii")

    # Check what base64 token is
    print(base64_message)

    auth_header['Authorization'] = "Basic " + base64_message
    auth_data['grant_type'] = "client_credentials"
    resp_json = requests.post(auth_URL, headers=auth_header, data=auth_data)

    # Response 200 is a successful request
    response_object = resp_json.json()
    pprint(json.dumps(response_object, indent=2))

    access_token = response_object['access_token']

    return access_token




def get_playlist_tracks_number(token, playlist_id):
    """
    Gets a tracks from playlist from Spotify's API.

    :param token: Access token generated using secrets and base64 encoding,
    :param playlist_id: Playlist ID for the playlist you want to get.

    :return:
    """

    playlist_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields=total"
    get_header = {"Authorization": f"Bearer {token}"}

    resp_json = requests.get(playlist_endpoint, headers=get_header)
    playlist_object = resp_json.json()

    num_tracks: int = playlist_object['total']

    return num_tracks


def get_playlist_tracks(token, playlist_id, num_tracks: int):
    """
    Gets a tracks from playlist from Spotify's API.

    :param token: Access token generated using secrets and base64 encoding,
    :param playlist_id: Playlist ID for the playlist you want to get.

    :return:
    """
    playlist_dict = {}

    for i in range(0, num_tracks, 100):
        playlist_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={i}"
        get_header = {"Authorization": f"Bearer {token}"}
        resp_json = requests.get(playlist_endpoint, headers=get_header)
        playlist_dict[i] = resp_json.json()

    return playlist_dict

# API requests
my_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
my_playlist_id = "6ZWdA2cosw0MzqSdY9EHqP"

num_tracks = get_playlist_tracks_number(my_token, my_playlist_id)
playlist_dict = get_playlist_tracks(my_token, my_playlist_id, num_tracks)
print(playlist_dict[0])
# Write results into file
with open("track_list.json", "w") as f:
    json.dump(playlist_dict[0], f)

items = playlist_dict[0]["items"]
items2 = playlist_dict[100]["items"]


def getMainData(playlist_obj: dict):

    # informacion a recopilar
    # La fecha de incorporacion.
    added_date = playlist_obj['added_at']

    # Ficha de la cancion
    track_dict = playlist_obj['track']

    # Tabla del Artista
    # Puede venir mas de uno.
    artists: dict = track_dict['artists'][0]

    # Tabla del album
    album: dict = track_dict['album']

    # Generamos la tabla con la informacion principal de la cancion
    track_keys = ["disc_number", "duration_ms", 'explicit', 'id', 'name', "track_number", "type", "popularity"]
    track_dict_main = {key: track_dict[key] for key in track_keys}
    track_tb_main = pd.DataFrame.from_dict(track_dict_main, orient='index', columns=["spotify"]).transpose()

    return track_tb_main, added_date, artists, album

def getArtistData(artists: dict):
    # Tabla del artista
    artist_tb = pd.DataFrame.from_dict(artists)
    artist_tb.columns = ["artist_" + a for a in artist_tb.columns]

    return artist_tb

def getAlbumData(album):
    # Tabla del album
    album["album_type"]
    album_keys = ["id", "album_type", "name", "release_date", "release_date_precision", "total_tracks", "type"]
    album_dict_main = {key: album[key] for key in album_keys}
    album_tb_1 = pd.DataFrame.from_dict(album_dict_main, orient='index', columns=["spotify"]).transpose()
    album_tb_1.columns = ["album_" + a for a in album_tb_1.columns]
    album_tb_1
    album_tb_2 = pd.DataFrame.from_dict(album["artists"][0])
    album_tb_2.columns = ["album_artist_" + a for a in album_tb_2.columns]
    album_tb_2
    album_tb = pd.concat([album_tb_1, album_tb_2], axis=1, join='outer')

    return album_tb

def getAllInfo(playlist_obj):

    track_dict_main, added_date, artists, album = getMainData(playlist_obj)
    artist_data= getArtistData(artists)
    album_data = getAlbumData(album)

    track_tb = pd.concat([track_dict_main, artist_data, album_data], axis=1, join='outer')
    track_tb["added_date"] = added_date

    return track_tb

def getData(items):

    list_items=[]
    for i in range(0,len(items)):
        track_tb = getAllInfo(items[i])
        list_items.append(track_tb)

    tracks_tb = pd.concat(list_items)

    return tracks_tb

def mainData(playlist_dict):
    all_items=[]
    for key in playlist_dict.keys():
        track_tb = getData(playlist_dict[key]["items"])
        all_items.append(track_tb)

    tracks_tb = pd.concat(all_items)

    return tracks_tb

tracks = mainData(playlist_dict)

print(tracks)
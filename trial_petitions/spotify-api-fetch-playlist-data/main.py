from pprint import pprint
import requests
from secrets import *
import base64, json


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


def get_playlist_tracks(token, playlist_id):
    """
    Gets a playlist from Spotify's API.

    :param token: Access token generated using secrets and base64 encoding,
    :param playlist_id: Playlist ID for the playlist you want to get.

    :return:
    """
    playlist_endpoint = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    get_header = {"Authorization": f"Bearer {token}"}

    resp_json = requests.get(playlist_endpoint, headers=get_header)

    playlist_object = resp_json.json()

    return playlist_object


# API requests
my_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
my_playlist_id = "6ZWdA2cosw0MzqSdY9EHqP"

track_list = get_playlist_tracks(my_token, my_playlist_id)

pprint(json.dumps(track_list, indent=2))


# Write results into file
#with open("track_list.json", "w") as f:
#    json.dump(track_list, f)


for song in track_list['tracks']['items']:
    print("------------------------")
    print("Track ID: " + song['track']['id'])
    artists_names = ", ".join([artist['name'] for artist in song['track']['artists']])
    print("Artist: " + artists_names)
    song_name = song['track']['name']
    print("Song: " + song_name)

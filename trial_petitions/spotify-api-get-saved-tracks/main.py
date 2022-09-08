from pprint import pprint
import requests

SPOTIFY_GET_USER_SAVED_TRACKS_URL = "https://api.spotify.com/v1/118192051/tracks?offset=0&limit=50"
ACCESS_TOKEN = "BQAUwxyOJx6mYBvipYZrEv4NLgA_buYHcIlo-9BM_3RtjW6ycqcRMLh72AXzrJI06mxyH9bcvaGjyutm3WRWqgkIm9EhDVjct_uSYnMu5f8FQKQrBKDHrBlhs6AnIIq46LeobxjhfBk63GzJwIlQkl78sZq52VEI9V2Kp06r2U2L3sUmWcmtR_82kgVtwCDsVmhZr7wTrs-0-knadLql3bEdNRPfRLguqIpR_PPRy8M"


def get_my_spotify_saved_tracks(access_token):
    response = requests.get(
        SPOTIFY_GET_USER_SAVED_TRACKS_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    resp_json = response.json()

    # Parametrisation... TODO: Troubleshoot "Items" KeyError issue to build basic parameters...
    tracks = [resp_json['items'][i]['track'] for i in range(len(resp_json['items']))]
    track_ids = [[track_id for track_id in tracks[i]['id']] for i in range(len(resp_json['items']))]
    track_names = [[track_name for track_name in tracks[i]['name']] for i in range(len(resp_json['items']))]
    artists = [[track['artists'] for track in tracks[i]] for i in range(len(resp_json['items']))]
    artists_names = [", ".join([artist['name'] for artist in artists[i]]) for i in range(len(tracks))]

    saved_tracks_info = {
        "id": track_ids,
        "name": track_names,
        "artists": artists_names
    }

    return saved_tracks_info


def main():
    saved_tracks_info = get_my_spotify_saved_tracks(
        ACCESS_TOKEN
    )

    pprint(saved_tracks_info, indent=4)


if __name__ == "__main__":
    main()

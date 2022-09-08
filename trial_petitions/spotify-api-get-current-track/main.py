from pprint import pprint
import requests


# Should run as an environment variable...
SPOTIFY_ACCESS_TOKEN = "BQAG-LQDcILD3BEpiICkIOTooGgOSSsDuXhtXJIPljftZDJ0zKOGVONOFwiTcd6pltNDukIG5gmWtvPvRm4mASQ1-lZpUw2MGjjcizFdHRHoPwaNb68TRckyt8rzAj98RFSt3vFIzGjq9hEcgxffmJG-vOrBvBRGcUZHb1S7BB4GfNC9UF4NbDTubgOjtF3lSq3m2UZx4Ayzcuz8h9jvtmPaLS6gwdmxCvP3UheuzY8"
SPOTIFY_GET_CURRENT_TRACK_URL = "https://api.spotify.com/v1/118192051/player"


def get_current_track(access_token):
    response = requests.get(
        SPOTIFY_GET_CURRENT_TRACK_URL,
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )
    resp_json = response.json()

    # Processing json parameters...
    track_id = resp_json['item']['id']
    track_name = resp_json['item']['name']
    artists = resp_json['item']['artists']
    artists_names = ", ".join([artist['name'] for artist in artists])
    link = resp_json['item']['external_urls']['spotify']

    current_track_info = {
        "id": track_id,
        "name": track_name,
        "artists": artists_names,
        "link": link
    }

    return current_track_info


def main():
    current_track_info = get_current_track(
        SPOTIFY_ACCESS_TOKEN
    )

    pprint(current_track_info, indent=4)


if __name__ == "__main__":
    main()

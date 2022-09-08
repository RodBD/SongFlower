import requests

# Token needs to be refreshed...
SPOTIFY_CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/118192051/playlists"
ACCESS_TOKEN = "BQClqlBDRbhaaJtN7-a2e65yumqPFmwcMOu746yq57DR4zPOQ37jORyQ5SQ1SjgSS4sn4cEPU26bvg9ebYO6hYI81lVJdxmrdxtlK_6TZjK1uMPeFUA6sH79bIgrWa1QecT6efViMuxg2IW4OwhPeYo4XT41T8RimBYKUYLpLiuOG9mzPctW2IFoNwhZf6wqVhflq1Db-cKFA0UECnmx-6Nu"


def create_playlist_on_spotify(name, public):
    """Creates a spotify playlist given a refreshed access token and the user's playlist directory URL.

    Arguments
    =========
    name (str): Name for the new playlist.
    public (bool): Public state of the new playlist.

    Returns
    =========
    JSON push to Spotify API to create playlist with the given parameters.

    """
    response = requests.post(
        SPOTIFY_CREATE_PLAYLIST_URL,
        headers={
            "Authorization": f"Bearer {ACCESS_TOKEN}"
        },
        json={
            "name": name,
            "public": public
        }
    )
    json_resp = response.json()

    return json_resp


def main():
    playlist = create_playlist_on_spotify(
        name="API playlist 1",
        public=False
    )

    print(f"Playlist: {playlist}")


if __name__ == "__main__":
    main()

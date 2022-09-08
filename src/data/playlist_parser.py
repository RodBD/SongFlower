from API_connection.API_request import ApiRequests
from API_connection.API_request_1 import *
import pandas as pd
import functools
import time


class MotherParser(object):
    TRACK_KEYS_PLUS = ["disc_number", "duration_ms", 'explicit', 'id', 'name', "track_number", "type", "popularity"]
    TRACK_KEYS_PRO = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
                      "instrumentalness", "liveness", "valence", "tempo", "id", "uri", "track_href", "analysis_url",
                      "time_signature"]
    TRACK_KEYS = ["disc_number", "duration_ms", 'explicit', 'id', 'name', "track_number", "type"]
    ALBUM_KEYS = ["id", "album_type", "name", "release_date", "release_date_precision", "total_tracks", "type"]

    # Extraccion de la informacion del album de la cancion.
    @classmethod
    def extract_album_data(cls, album):
        # Tabla del album
        # album: dict = self.track_dict['album']

        album_dict_main = {key: album[key] for key in cls.ALBUM_KEYS}
        album_tb_1 = pd.DataFrame.from_dict(album_dict_main, orient='index', columns=["spotify"]).transpose()
        album_tb_1.columns = ["album_" + a for a in album_tb_1.columns]
        album_tb_2 = pd.DataFrame.from_dict(album["artists"][0])
        album_tb_2.columns = ["album_artist_" + a for a in album_tb_2.columns]
        album_data = pd.concat([album_tb_1, album_tb_2], axis=1, join='outer')
        return album_data

    # Extraccion de la informacion del artista de la cancion.
    @staticmethod
    def extract_artist_data(song):
        # Tabla del Artista, Puede venir mas de uno.
        artists: dict = song['artists'][0]
        # Tabla del artista
        artist_data = pd.DataFrame.from_dict(artists)
        artist_data.columns = ["artist_" + a for a in artist_data.columns]

        return artist_data

    @classmethod
    def extract_tracks_data(cls, track_dict, tracks_keys=None):
        if tracks_keys is None:
            tracks_keys = cls.TRACK_KEYS
        track_dict_main = {key: track_dict[key] for key in tracks_keys}
        track_tb_main = pd.DataFrame.from_dict(track_dict_main, orient='index', columns=["spotify"]).transpose()
        return track_tb_main

    @staticmethod
    def extract_info_from_items_level(with_extract_func, from_item_dict, key):
        return pd.concat([with_extract_func(item) for item in from_item_dict[key]["items"]])


class PlaylistParser(MotherParser):

    def __init__(self, playlist_id):
        #self.playlist_dict = ApiRequests('CCF', 'playlists').get_dict_partitions_artists_playlist(playlist_id)
        self.playlist_dict = PlaylistApi(playlist_id).get_id_partitioned_information()
        self.track_ids = self.get_playlist_data().index.tolist()

    def get_curated_playlist_data(self):

        selected_columns = ['id', 'name', 'artist_name', 'album_name', 'track_number', 'duration_ms', 'explicit',
                            'type', 'popularity', 'artist_id', 'artist_type', 'album_id',
                            'album_album_type', 'album_release_date', 'album_release_date_precision',
                            'album_total_tracks', 'album_type', 'album_artist_href',
                            'album_artist_id', 'album_artist_name', 'album_artist_type', 'added_date', 'danceability',
                            'energy', 'key', 'loudness', 'mode', 'speechiness',
                            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature']

        curated_playlist_data = self.get_playlist_data().join(self.get_track_details(), on="id", how="left")[selected_columns]

        return curated_playlist_data

    def get_track_details(self):
        """ All track specific data from Track IDs in playlist_data. """

        track_details = pd.DataFrame()

        for i in range(0, len(self.track_ids), 100):
            tracks_ids = functools.reduce(lambda x, y: x + "%2C" + y, self.track_ids[i:1+100])
            #album_tracks_dict = ApiRequests('CCF', 'audio-features').get_general_information(tracks_ids)
            album_tracks_dict = AudioFeaturesApi().get_ids_information(tracks_ids)
            tracks_pro_info_df = pd.concat([self.extract_tracks_data(tracks_dict, self.TRACK_KEYS_PRO)
                                            for tracks_dict in album_tracks_dict['audio_features']])
            track_details = track_details.append(tracks_pro_info_df)

        track_details = track_details.set_index('id')

        return track_details

    def get_playlist_data(self):
        """ All information rescue from playlist ID"""

        playlist_data = pd.concat([self.extract_info_from_items_level(
            self.get_specific_track_data,
            self.playlist_dict, key) for key in self.playlist_dict.keys()]).set_index("id")

        return playlist_data

    def get_specific_track_data(self, song):
        """ Extracts a specific track's data using request's JSON. """
        track_tb_main = self.extract_tracks_data(song['track'], self.TRACK_KEYS_PLUS)
        artist_data = self.extract_artist_data(song['track'])
        album_data = self.extract_album_data(song['track']['album'])

        track_data = pd.concat([track_tb_main, artist_data, album_data], axis=1, join='outer')
        track_data["added_date"] = song['added_at']

        return track_data


class ArtistParser(MotherParser):

    def __init__(self, artist_id):
        #self.artists_dict = ApiRequests('CCF', 'artists').get_dict_partitions_artists_playlist(artist_id)
        self.artists_dict = ArtistsApi(artist_id).get_id_partitioned_information()

    @classmethod
    def tracks_partitions(cls, album_tracks_dict):
        return pd.concat([MotherParser.extract_info_from_items_level(cls.extract_tracks_data, album_tracks_dict, key)
                          for key in album_tracks_dict.keys()]).set_index("id")

    def get_album_data(self):
        return pd.concat([self.extract_info_from_items_level(self.extract_album_data, self.artists_dict, key)
                          for key in self.artists_dict.keys()]).set_index("album_id")

    def extract_artists_tracks(self):
        artist_tracks = pd.DataFrame()
        for album_id in self.get_album_data().index:
            #album_tracks_dict = ApiRequests('CCF', 'albums').get_dict_partitions_artists_playlist(album_id)
            album_tracks_dict = AlbumsApi(album_id).get_id_partitioned_information()
            tracks_partition = self.tracks_partitions(album_tracks_dict)
            artist_tracks = artist_tracks.append(tracks_partition)

        return artist_tracks

    def improve_artists_tracks(self):
        artists_tracks_basics = self.extract_artists_tracks()
        artists_tracks_ids = list(artists_tracks_basics.index)
        artists_tracks_pro = pd.DataFrame()

        for i in range(0, len(artists_tracks_ids), 100):
            tracks_ids = functools.reduce(lambda x, y: x + '%2C' + y, artists_tracks_ids[i:i+100])
            album_tracks_dict = AudioFeaturesApi().get_ids_information(tracks_ids)
            tracks_pro_info_df = pd.concat([self.extract_tracks_data(tracks_dict, self.TRACK_KEYS_PRO)
                                            for tracks_dict in album_tracks_dict['audio_features']])
            artists_tracks_pro = artists_tracks_pro.append(tracks_pro_info_df)

        artists_tracks_pro = artists_tracks_pro.set_index('id')

        return pd.concat([artists_tracks_pro, artists_tracks_basics], axis=1, join='outer').columns






#playlistObj = PlaylistParser('6ZWdA2cosw0MzqSdY9EHqP')
#playlistDF = playlistObj.playlist()
#print(playlistDF)

albumObj = ArtistParser('3LfKt6bEMIfFIEryeai8Mm')
tracksDF = albumObj.extract_artists_tracks()
print(tracksDF)

artistsObj = ArtistParser('3LfKt6bEMIfFIEryeai8Mm')
alltracksDF = artistsObj.improve_artists_tracks()
print(alltracksDF)

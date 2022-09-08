import requests
from API_connection.token_generator import TokenGenerator
from abc import ABCMeta, abstractmethod, ABC


class ApiRequests(object, metaclass=ABCMeta):

    def __init__(self, auth_type, api_type, element_type, limit):
        self.token = TokenGenerator(auth_type=auth_type).token

        self.partitioned_offset_information: dict = {}
        self.api_type = api_type
        self.element_type = element_type
        self.limit = limit
        self.query = self.set_basic_query()

    def set_basic_query(self):
        #Main Body of the API Request Url
        return f"https://api.spotify.com/v1/{self.api_type}/"

    def execute_request(self):
        # Method used in any api request to execute the query over the api and keep the output.
        get_header = {"Authorization": f"Bearer {self.token}"}
        resp_json = requests.get(self.query, headers=get_header)

        return resp_json

    @abstractmethod
    # TODO: Try differents id handle invalid id type.
    def get_id_partitioned_information(self):
        """
        Gets a dictionary with all the items under the ids structure belongs. The key will inform the offset number.
        :param _id:
        :return:
        """
        return dict

    @abstractmethod
    def get_total_number_items(self):
        """
        Gets the number of elements for mayor structure as albums from artist or songs from playlists.
        :param _id: id from de structure.
        :return: int: with the number of elements from the structure
        """
        return int

    @abstractmethod
    def get_ids_information(self, _ids):
        """
        Gets a dictionary with all the ids information.
        :param _ids: several ids string concat by %2C
        :return:
                """
        return dict


class PlaylistApi(ApiRequests):

    def __init__(self, _id):
        super().__init__('CCF', "playlists", "tracks", 100)
        self._id = _id

    def get_total_number_items(self):
        self.query = self.set_basic_query() + f"{self._id}/{self.element_type}?fields=total"
        api_respond = self.execute_request()
        num_songs = api_respond.json()['total']

        return num_songs

    def get_id_partitioned_information(self):
        self.query = self.set_basic_query() + f"{self._id}/{self.element_type}"

        for i in range(0, self.get_total_number_items(), self.limit):
            self.query = self.query + f"?offset={i}&limit={self.limit}"
            api_respond = self.execute_request()
            self.partitioned_offset_information[i] = api_respond.json()

        return self.partitioned_offset_information

    def get_ids_information(self, _ids):
        pass


class ArtistsApi(PlaylistApi):

    def __init__(self, _id):
        super(PlaylistApi, self).__init__('CCF', "artists", "albums", 50)
        self._id = _id

    def get_ids_information(self, _ids):
        self.query = self.set_basic_query() + f"?ids={_ids}"
        api_respond = self.execute_request()
        all_ids_information = api_respond.json()

        return all_ids_information


class AlbumsApi(ArtistsApi):

    def __init__(self, _id):
        super(PlaylistApi, self).__init__('CCF', "albums", "tracks", 50)
        self._id = _id

class AudioFeaturesApi(ArtistsApi):

    def __init__(self):
        super(PlaylistApi, self).__init__('CCF', "audio-features", "", 0)




Playlist = PlaylistApi("6ZWdA2cosw0MzqSdY9EHqP")
Artilist = ArtistsApi("3LfKt6bEMIfFIEryeai8Mm")
Albulist = AlbumsApi("5F95mzbai9vB6GMLsWsYuo")

print(Albulist.get_id_partitioned_information())
print(Artilist.get_id_partitioned_information())
print(Playlist.get_id_partitioned_information())

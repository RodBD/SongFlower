import requests
from API_connection.token_generator import TokenGenerator


class ApiRequests():

    def __init__(self, auth_type, api_type):
        self.partitioned_offset_information: dict = {}
        self.num_tracks: int = 0
        self.token = TokenGenerator(auth_type=auth_type).token
        self.api_type = api_type
        #self.set_element_type()
        if self.api_type == 'playlists':
            self.element_type = 'tracks'
            self.limit = 100
        elif self.api_type == 'artists':
            self.element_type = 'albums'
            self.limit = 50
        elif self.api_type == 'albums':
            self.element_type = 'tracks'
            self.limit = 50

    def set_element_type(self,api_type):

        if api_type == 'playlists':
            self.api_type = 'playlists'
            self.element_type = 'tracks'
            self.limit = 100
        elif api_type == 'artists':
            self.api_type = 'artists'
            self.element_type = 'albums'
            self.limit = 50

    def get_dict_partitions_artists_playlist(self, _id):
        """
        Get partitioned information from a big structure with several offsets such as playlist, artists ....

        :param token: Access token generated using secrets and base64 encoding,
        :param _id: id from de structure.

        :return dict: every key is the offset number.
        """
        #TODO: Try differents id handle invalid id type.
        for i in range(0, self.get_number_tracks_albums(_id), self.limit):
            _endpoint = f"https://api.spotify.com/v1/{self.api_type}/{_id}/{self.element_type}" \
                        f"?offset={i}&limit={self.limit}"

            get_header = {"Authorization": f"Bearer {self.token}"}
            resp_json = requests.get(_endpoint, headers=get_header)
            self.partitioned_offset_information[i] = resp_json.json()

        return self.partitioned_offset_information

    def get_number_tracks_albums(self, _id):
        """
        Gets the number of elements for mayor structure as albums from artist or songs from playlists.

        :param token: Access token generated using secrets and base64 encoding,
        :param _id: id from de structure.

        :return: int: with the number of elements from the structure
        """

        total_endpoint = f"https://api.spotify.com/v1/{self.api_type}/{_id}/{self.element_type}?fields=total"
        get_header = {"Authorization": f"Bearer {self.token}"}

        resp_json = requests.get(total_endpoint, headers=get_header)
        total_object = resp_json.json()['total']

        return total_object

    def get_general_information(self, _id):
        """
        Gets the number of elements for mayor structure as albums from artist or songs from playlists.

        :param token: Access token generated using secrets and base64 encoding,
        :param _id: id from de structure.

        :return: int: with the number of elements from the structure
        """

        _endpoint = f"https://api.spotify.com/v1/{self.api_type}?ids={_id}"
        get_header = {"Authorization": f"Bearer {self.token}"}

        resp_json = requests.get(_endpoint, headers=get_header)
        general_object = resp_json.json()

        return general_object

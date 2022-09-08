import requests
import base64


class TokenGenerator(object):
    CLIENT_ID: str = "32dfe559fed14018bbbae1ee7bed1245"
    CLIENT_SECRET: str = "8567cd1905b6403da74e9d4a3a30a493"
    VALID_ACCESS_TYPES = ['CCF']

    def __init__(self, auth_type: str):
        """ Initialises a TokenGenerator object taking the authorisation code to create the necessary token.

        To understand what authorisation your program or workflow need visit Spotify for developers website.

        :param auth_type (str): Spotify's API desired authorisation token type: CCF, ... .
        """
        if auth_type not in self.VALID_ACCESS_TYPES:
            raise ValueError("Invalid authorisation type!")
        self._authorization = auth_type
        self._token = self.generate_token(auth_type)

    def __hash__(self):
        return hash((self._authorization, self._token))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and (self._token == other._token) \
               and (self._authorization == other._authorization)

    def __str__(self):
        return """TokenGenerator:\n access_type: {access_type}\n token: {token}""".format(
            access_type=self._authorization,
            token=self._token
        )

    @property
    def authorization(self):
        """ Authorisation type dependant on the workflow being designed and the permissions it needs.

        :return: Objects instance authorisation type.
        """
        return self._authorization

    @authorization.setter
    def authorization(self, auth_type: str):
        """ Validates authorization type before assigning it to instance attribute.

        :param auth_type (str): Spotify's API desired authorisation token type: CCF, ... .
        :return: Assigns input authorisation type value to authorisation attribute. Returns nothing.
        """
        if auth_type not in TokenGenerator.VALID_ACCESS_TYPES:
            raise ValueError("Invalid authorization type")
        self._authorization = auth_type

    @property
    def token(self):
        """ Current authorisation token to access a specific Spotify API endpoint

        :return (str): Current access token.
        """
        return self._token

    @token.deleter
    def token(self):
        """ Enables deletion of token property attribute using del keyword

        :return: Deletes value stored in token attribute.
        """
        del self._token

    def generate_token(self, auth_type: str):
        """ Calls Spotify API using the function that provides the token for the authorisation requested.

        :param auth_type: Spotify's API desired authorisation token type: CCF, ... .
        :return: Returns the string value of the requested access token.
        """
        if auth_type == "CCF":
            return self._get_client_credentials_flow_token(self.CLIENT_ID, self.CLIENT_SECRET)

    def refresh_token(self):
        """ Refreshes the instance object token attribute by requesting and storing new token petition.

        :return (NoneType): Stores new token in the object's token attribute,
        """
        self._token = TokenGenerator(self._authorization).token

    @staticmethod
    def _encode_client_secrets_b64(client_id: str, client_secret: str):
        """ Encodes client_id:client_secret pair in base64 format to be used when requesting
        Authorization Code Flow (ACF) or Client Credentials Flow (CCF) access tokens.

        :param client_id (str): Spotify's API app client ID.
        :param client_secret (str): Spotify's API app secret ID.
        :return (str): Base64 encoded client secrets.
        """
        # Base64 encode Client ID and Client Secret...
        message = f"{client_id}:{client_secret}"
        message_bytes = message.encode("ascii")
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode("ascii")

        return base64_message

    @classmethod
    def _get_client_credentials_flow_token(cls, client_id: str, client_secret: str):
        """ Takes secrets and generates a Client Credentials Flow (CCF) access token.

        The CCF flow is used in server-to-server authentication. Only endpoints that do not access user information
        can be accessed. Higher rate limit is applied.

        :param client_id (str): Spotify's API app client ID.
        :param client_secret (str): Spotify's API app secret ID.

        :return: Client Credentials Flow access token.
        """
        base64_message = cls._encode_client_secrets_b64(client_id, client_secret)
        auth_url = "https://accounts.spotify.com/api/token"
        auth_header = {"Authorization": "Basic " + base64_message}
        auth_data = {'grant_type': "client_credentials"}
        resp_json = requests.post(auth_url, headers=auth_header, data=auth_data)

        # Response 200 is a successful request
        response_object = resp_json.json()
        # print(response_object)
        access_token = response_object['access_token']

        return access_token


# EXAMPLE OF USE ////

tokenizer = TokenGenerator(auth_type="CCF")
print("Your new token is:", tokenizer.token)

# Token refresh by re instancing the object
tokenizer.refresh_token()
print("Your new token is:", tokenizer.token)

print(isinstance(tokenizer, TokenGenerator))

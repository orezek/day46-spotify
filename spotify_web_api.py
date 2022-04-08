import spotipy
import json


class SpotifyWebAccess:

    def __init__(self):
        """
        Spotify account information - should be secret for each account
        You may use environmental variables instead instance variables
        """

        self.client_id = None  # add your own spotify id
        self.client_secret = None  # add your own spotify secret key
        self.scope = None  # add your own scope
        self.redirect_uri = "http://example.com"    # you can add yor won redirect url but this one is sufficient too

        self.sp_oauth_obj = spotipy.oauth2.SpotifyOAuth(
                                client_id=self.client_id,
                                client_secret=self.client_secret,
                                scope=self.scope,
                                redirect_uri=self.redirect_uri)
        self.spotify = spotipy.Spotify(auth_manager=self.sp_oauth_obj)  # Spotify object for querying Spotify services

    def authenticate_user(self):
        """
        Generates .cache.txt with access token and other data
            1) it will redirect you to a web page and you need to copy the URL
            2) Enter the URL to the prompt and press enter
            3) You get a new .cache file with your access data
        """
        access_token = self.sp_oauth_obj.get_access_token()
        return access_token

    def refresh_access_token(self):
        """Refreshes access token on demand."""
        with open(".cache", "r") as file:
            data = json.loads(file.read())
            refresh_token = data["refresh_token"]
        get_new_token = self.sp_oauth_obj.refresh_access_token(refresh_token)
        return get_new_token

    def get_user_info(self):
        """Retrieves all information about the user including its ID."""
        user_info = self.spotify.current_user()
        return user_info

    def get_user_spotify_id(self):
        """
        Returns the user ID
        """
        return self.get_user_info()["id"]

    def find_id_for_song_name(self, song_name, year):
        """
        Finds URI of a track from a song name

        :param song_name:
            Insert the searech song name.
        :param year:
            Specify a date when the song was released.
        """
        # song_name = f"track:{song_name} date:{year}"   # disabled for better Spotify track search results
        track_uri = self.spotify.search(song_name, limit=1, type="track")
        try:
            return track_uri["tracks"]["items"][0]["id"]
        except IndexError:
            return None

    def add_tracks_to_playlist(self, playist_id, tracks_list):
        """
        Adds track to a playlist specified by its ID
        """
        self.spotify.playlist_add_items(playlist_id=playist_id, items=tracks_list)

    def create_playlist(
            self,
            name_of_the_playlist,
            description="Playlist created by a Python script"
    ):
        """
        Creates a public playlist in the user profile and returns its ID.
        :param name_of_the_playlist:
            Name of the playlist to be created
        :param description:
            Add some text for description of the playlist
        """
        playlist = self.spotify.user_playlist_create(self.get_user_spotify_id(),
                                                     name_of_the_playlist,
                                                     description=description,
                                                     public=True
                                                     )
        return playlist["id"]

    def get_playlist_id(self, name):
        """
        Gets ID of a playlist from give name, if the name is not found return None.

        :param name:
            Name of a playlist to get its ID.
        :return:
            Returns ID of a playlist and None if it does not exist.
        """
        playlists = self.spotify.current_user_playlists()["items"]
        for playlist in playlists:
            if str(playlist["name"]).lower() == name.lower():
                return playlist["id"]
            else:
                return None


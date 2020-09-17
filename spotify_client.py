import requests
import json
import random

# Web API Reference:
# https://developer.spotify.com/documentation/web-api/reference/

# Spotify API URLS
spotify_api_base_url = "https://api.spotify.com"
api_version = "v1"
spotify_api_url = f"{spotify_api_base_url}/{api_version}"


class SpotifyClient(object):
    def __init__(self, access_token, artists_limit, time_range, tracks_limit, playlist_name):
        self.access_token = access_token
        self.artists_limit = artists_limit
        self.time_range = time_range
        self.tracks_limit = tracks_limit
        self.playlist_name = playlist_name

    def get_top_artists(self):
        # Personalization Endpoint - GET https://api.spotify.com/v1/me/top/{type} - Get a User's Top Artists and Tracks.
        print("Getting user's top artists...")
        endpoint = f"{spotify_api_url}/me/top/artists?time_range={self.time_range}&limit={self.artists_limit}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(endpoint, headers=headers)
        artists_json = response.json()
        artists = list()
        for artist in artists_json["items"]:
            artists.append(artist["id"])
        return artists

    def get_top_tracks(self):
        # Artists Endpoint - GET https://api.spotify.com/v1/artists/{id}/top-tracks - Get an Artist's Top Tracks.
        artists = self.get_top_artists()
        tracks = list()
        print("Getting top tracks...")
        for artist in artists:
            endpoint = f"{spotify_api_url}/artists/{artist}/top-tracks?country=GB"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            response = requests.get(endpoint, headers=headers)
            tracks_json = response.json()
            counter = 0
            for track in tracks_json["tracks"]:
                tracks.append(track["uri"])
                counter += 1
                if counter == self.tracks_limit:
                    break
        random.shuffle(tracks)
        return tracks

    def get_user(self):
        # Users Profile Endpoint - GET https://api.spotify.com/v1/me - Get Current User's Profile.
        print("Getting current user's profile...")
        endpoint = f"{spotify_api_url}/me"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(endpoint, headers=headers)
        return response.json()["id"]

    def create_playlist(self):
        # Playlists Endpoint - POST https://api.spotify.com/v1/users/{user_id}/playlists - Create a Playlist.
        user = self.get_user()
        print("Creating a playlist...")
        endpoint = f"{spotify_api_url}/users/{user}/playlists"
        headers = {"Authorization": f"Bearer {self.access_token}",
                   "Content-Type": "application/json"}
        data = json.dumps({
            "name": self.playlist_name,
            "description": "Top songs of my favorite artists!",
            "public": False})
        response = requests.post(endpoint, headers=headers, data=data)
        return response.json()["id"]

    def add_tracks_to_playlist(self):
        # Playlists Endpoint - POST https://api.spotify.com/v1/playlists/{playlist_id}/tracks - Add Items to a Playlist.
        playlist = self.create_playlist()
        tracks = self.get_top_tracks()
        print("Adding tracks to the playlist...")
        endpoint = f"{spotify_api_url}/playlists/{playlist}/tracks"
        headers = {"Authorization": f"Bearer {self.access_token}",
                   "Content-Type": "application/json"}
        for i in range(0, len(tracks), 100):
            data = json.dumps({"uris": tracks[i: i+100]})
            requests.post(endpoint, headers=headers, data=data)
        return

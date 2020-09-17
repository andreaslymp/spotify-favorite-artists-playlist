import requests
from flask import Flask, request, redirect
import click
from urllib.parse import urlencode
from datetime import date
from spotify_client import SpotifyClient

# Authorization guide:
# https://developer.spotify.com/documentation/general/guides/authorization-guide/

# Spotify Client Keys
client_id = ""
client_secret = ""

# Spotify AUTH URLS
spotify_auth_url = "https://accounts.spotify.com/authorize"
spotify_token_url = "https://accounts.spotify.com/api/token"

# AUTH Parameters
client_side_url = "http://127.0.0.1"
port = 8080
redirect_uri = f"{client_side_url}:{port}/callback/"
scope = "user-read-email user-top-read playlist-modify-public playlist-modify-private"

auth_query_parameters = {
    "client_id": client_id,
    "response_type": "code",
    "redirect_uri": redirect_uri,
    # "state": "",
    "scope": scope,
    "show_dialog": True
}


# User's preferences
def get_preferences():
    artists_limit = click.prompt('\nEnter the max. number of your top artists for your playlist (1-50) ',
                                 type=click.IntRange(1, 50), default=20)
    choices = {'short-term', 'medium-term', 'long-term'}
    time_range = click.prompt('\nSpotify will look for your top artists over a specified time range:\n'
                              '\tlong-term: several years of data and including all new data as it becomes available\n'
                              '\tmedium-term: approximately last 6 months\n'
                              '\tshort-term: approximately last 4 weeks\n'
                              'Enter your time range ',
                              type=click.Choice(choices, case_sensitive=False), default='medium-term').replace("-", "_")
    tracks_limit = click.prompt('\nEnter the max. number of tracks per artist for your playlist (1-10) ',
                                type=click.IntRange(1, 10), default=10)
    playlist_name = click.prompt('\nEnter the name of your new playlist ',
                                 default="Favorite Artists {}".format(date.today().strftime("%d/%m/%Y")))
    return artists_limit, time_range, tracks_limit, playlist_name


app = Flask(__name__)


@app.route("/")
def request_authorization():
    print("Requesting Authorization...")
    auth_url = f"{spotify_auth_url}?{urlencode(auth_query_parameters)}"
    return redirect(auth_url)


@app.route("/callback/")
def callback():
    print("Requesting access token...")
    code = request.args["code"]
    data = {
        "grant_type": "authorization_code",
        "code": str(code),
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret}
    response = requests.post(spotify_token_url, data=data)
    response_json = response.json()
    access_token = response_json["access_token"]

    artists_limits, time_range, tracks_limit, playlist_name = get_preferences()

    # Access the Spotify API
    spotify_client = SpotifyClient(access_token, artists_limits, time_range, tracks_limit, playlist_name)
    spotify_client.add_tracks_to_playlist()
    print("Your new playlist is ready, enjoy!")
    return redirect("https://open.spotify.com/collection/playlists")


if __name__ == "__main__":
    app.run(debug=True, port=port)

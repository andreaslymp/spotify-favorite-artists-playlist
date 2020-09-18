# spotify-favorite-artists-playlist  
   
Create a Spotify playlist with the top tracks of your favorite artists.

## Getting started

- Create your Spotify application [here](https://developer.spotify.com/dashboard/ "https://developer.spotify.com/dashboard/"). On your app's settings, add http://127.0.0.1:8080/callback/ as the redirect URI.  

- Clone the repository:  
  
  `git clone https://github.com/andreaslymp/spotify-favorite-artists-playlist.git`  
  `cd spotify-favorite-artists-playlist.git`
  
- Create a virtual environment, activate it and install the requirements,  
   with `venv` (this will create a `venv` folder in your directory):

  `python3.8 -m venv venv`  
  `. venv/bin/activate`  
  `pip install -r requirements.txt`

  or with `pipenv` (this will create a `Pipfile` and a `Pipfile.lock` in your directory):

  `pipenv install`  
  `pipenv shell`  

## Running the app

- Make sure you fill in your application's *Client ID* and *Client Secret* in `main.py`

- Run the app with `python3 main.py` and visit http://127.0.0.1:8080/.

- In your browser, you'll be asked to authorize the app.

- In your console, you'll be asked to specify your preferences for your new playlist: the *number of your favorite artists* over a *time span*, the *number of top tracks per artist* and the *playlist's name*. If you don't want to specify a preference, hit *Enter* and a default value will be applied for that option. 

- Finally, when your playlist is ready, you'll be redirected to your [Spotify account](https://open.spotify.com/collection/playlists "https://open.spotify.com/collection/playlists"). Enjoy!
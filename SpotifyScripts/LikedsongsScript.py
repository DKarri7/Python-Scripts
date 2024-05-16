import spotipy
from spotipy.oauth2 import SpotifyOAuth

import os

def get_liked_songs(client_id, client_secret, redirect_uri="your_redirect_uri"):

    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope="user-library-read")

    token_info = sp_oauth.get_cached_token()
    
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Open this link in your browser to authorize: {auth_url}")

        try:
            code = input("Enter the code from the redirect URL:")
            token_info = sp_oauth.get_access_token(code)
        except Exception as e:
            print(f"Error: {e}")
            return

    token = token_info["access_token"]

    sp = spotipy.Spotify(auth=token)

    with open("liked_songs.txt", "w") as f:
        results = sp.current_user_saved_tracks()
        while results:
            for item in results['items']:
                track = item['track']
                track_name = track['name']
                artist_names = ', '.join([artist['name'] for artist in track['artists']])
                f.write(f"{track_name} by {artist_names}\n")

            if results['next']:
                results = sp.next(results)
            else:
                results = None

    print("Liked songs saved to liked_songs.txt")

client_id = "your_client_id"
client_secret = "your_client_secret"

get_liked_songs(client_id, client_secret)

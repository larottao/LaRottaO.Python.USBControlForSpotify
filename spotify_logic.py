#requires pip install spotipy
#remember to set the redirect URL on the spotify dashboard as http://localhost:8888/callback/
#save your credentials on the json file located at the same path as the app

import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CREDENTIALS_FILE = 'spotify_credentials.json'

def run():
    if not os.path.exists(CREDENTIALS_FILE):
        credentials = {
            'CLIENT_ID': 'your_client_id',
            'CLIENT_SECRET': 'your_client_secret'
        }
        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(credentials, f, indent=4)
        print(f"Created {CREDENTIALS_FILE}. Please fill in your Spotify credentials.")
        exit(1)
    else:
        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = json.load(f)
            return credentials['CLIENT_ID'], credentials['CLIENT_SECRET']

CLIENT_ID, CLIENT_SECRET = run()
REDIRECT_URI = 'http://localhost:8888/callback/'
SCOPE = 'user-modify-playback-state user-read-playback-state'

print("Creating instance of Spotify API...")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope=SCOPE))
print("Spotify API loaded ok.")

def play():
    2
    print("start selected.")

def pause():
    sp.pause_playback()
    print("pause selected.")

def next_track():
    print("next track selected.")
    sp.next_track()

def previous_track():
    sp.previous_track()
    print("previous track selected.")

def print_current_song():
    print("print current song selected.")
    current_track = sp.current_playback()
    if current_track and current_track['item']:
        print(f"Currently playing: {current_track['item']['name']} by {', '.join(artist['name'] for artist in current_track['item']['artists'])}")
    else:
        print("No track currently playing.")

'''
def spot_main():
  
    while True:
        print("\nSpotify Controller")
        print("1. Play")
        print("2. Pause")
        print("3. Next Track")
        print("4. Previous Track")
        print("5. Print Current Song")
        print("6. Exit")

        choice = input("Enter your choice: ")
        
        if choice == '1':
            play()
        elif choice == '2':
            pause()
        elif choice == '3':
            next_track()
        elif choice == '4':
            previous_track()
        elif choice == '5':
            print_current_song()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

spot_main()
            '''



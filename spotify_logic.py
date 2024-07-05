#requires pip install spotipy
#remember to set the redirect URL on the spotify dashboard as http://localhost:8888/callback/
#save your credentials on the json file located at the same path as the app

import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

import threading

import time

CREDENTIALS_FILE = 'spotify_credentials.json'

global sp
global callbacks

def load_credentials():     

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

def format_time(ms):
    # Convert milliseconds to minutes:seconds
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def spotify_worker():
 
    global callbacks   

    CLIENT_ID, CLIENT_SECRET = load_credentials()
    REDIRECT_URI = 'http://localhost:8888/callback/'
    SCOPE = 'user-modify-playback-state user-read-playback-state'

    print("Creating instance of Spotify API...")

    global sp 
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                client_secret=CLIENT_SECRET,
                                                redirect_uri=REDIRECT_URI,
                                                scope=SCOPE))
    print("Spotify API loaded ok.")

   # Example of Spotify logic running continuously
    while True:
        try:
            current_playback = sp.current_playback()
            if current_playback and current_playback['is_playing']:
                print("Currently playing:", current_playback['item']['name'])
                position = current_playback['progress_ms']
                duration = current_playback['item']['duration_ms']
                print(f"Position: {format_time(position)} / {format_time(duration)}")
                # Example: Update screen callback
                callbacks['update_screen']()
            time.sleep(1)  # Query every second
        except Exception as e:
            print(f"Error in Spotify worker: {e}")
            time.sleep(10)  # Retry after 10 seconds on error         

def play():   
    try:
        global sp 
        sp.start_playback()
        callbacks['update_screen']()
    except:
        return

def pause():
    try:
        global sp
        sp.pause_playback()  
        callbacks['reproduction_paused']()
    except:
        return

def next_track():
    try:
        global sp
        sp.next_track()
        callbacks['update_screen']()
    except:
        return


def previous_track():
    try:
        global sp
        sp.previous_track()  
        callbacks['update_screen']() 
    except:
        return

def print_current_song():    
    try:
        global sp
        return sp.current_playback()    
    except:
        return
    

def run(arg_callbacks):
    global callbacks
    callbacks = arg_callbacks

    # Start a separate thread for Spotify logic
    spotify_thread = threading.Thread(target=spotify_worker)
    spotify_thread.daemon = True
    spotify_thread.start()

    # Optionally return the thread object if you need to manage it further
    return spotify_thread
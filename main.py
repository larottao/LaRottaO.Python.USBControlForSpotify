import spotify_logic
import crystalfontz_logic
import time



def print_welcome():
    
    crystalfontz_logic.send_text_to_screen(0, "CrystalFontz plugin", 0, True)
    crystalfontz_logic.send_text_to_screen(1, "for Spotify ", 0, True)
    crystalfontz_logic.send_text_to_screen(2, "", 0, True)
    crystalfontz_logic.send_text_to_screen(3, "by LaRottaO", 0, True)



def print_paused():

        crystalfontz_logic.send_text_to_screen(0, "Paused.", 0, True)
        crystalfontz_logic.send_text_to_screen(1, "", 0, True)
        crystalfontz_logic.send_text_to_screen(2, "", 0, True)
        crystalfontz_logic.send_text_to_screen(3, "", 0, True)
    
def format_time(ms):
    # Convert milliseconds to minutes:seconds
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02}:{seconds:02}"

def update_screen():
    
    current_playback = spotify_logic.sp.current_playback()
   
    if current_playback and current_playback['is_playing'] and current_playback['item']:
   
        position = current_playback['progress_ms']
        duration = current_playback['item']['duration_ms']

        song = current_playback['item']['name'][:20]
        artist = (', '.join(artist['name'] for artist in current_playback['item']['artists']))[:20]    

        crystalfontz_logic.send_text_to_screen(0, song, 0, True)
        crystalfontz_logic.send_text_to_screen(1, artist, 0, True)     
        crystalfontz_logic.send_text_to_screen(2, "", 0, True)  
        crystalfontz_logic.send_text_to_screen(3, format_time(position) + " / " + format_time(duration), 0, True)  
      



def up_button_was_pressed():
    spotify_logic.previous_track()  

def down_button_was_pressed():
    spotify_logic.next_track()

def left_button_was_pressed():
    spotify_logic.previous_track()

def right_button_was_pressed():
    spotify_logic.next_track()

def accept_button_was_pressed():
    spotify_logic.play()

def reject_button_was_pressed():
    spotify_logic.pause()   

callbacks = {    
    'update_screen': update_screen,
    'reproduction_paused' : print_paused,
    'print_welcome' : print_welcome,
    'up': up_button_was_pressed,
    'down': down_button_was_pressed,
    'left': left_button_was_pressed,
    'right': right_button_was_pressed,
    'accept': accept_button_was_pressed,
    'reject': reject_button_was_pressed
}


spotify_logic.run(callbacks)
crystalfontz_logic.run(callbacks)
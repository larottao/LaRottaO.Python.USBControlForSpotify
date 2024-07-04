import spotify_logic
import crystalfontz_logic

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
    'up': up_button_was_pressed,
    'down': down_button_was_pressed,
    'left': left_button_was_pressed,
    'right': right_button_was_pressed,
    'accept': accept_button_was_pressed,
    'reject': reject_button_was_pressed
}



spotify_logic.run()
crystalfontz_logic.run(callbacks)

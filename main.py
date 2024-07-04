#requires pip install spotipy
#remember to set the redirect URL on the spotify dashboard as http://localhost:8888/callback/
#save your credentials on the json file located at the same path as the app

import crystalfontz_logic
import spotify_logic

print("hello from main.py")

spotify_logic.load_credentials()
#crystalfontz_logic.main()
    



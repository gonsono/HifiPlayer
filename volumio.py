import requests
import time

class Volumio:
    """Display class that allow interaction with Volumio"""

    # Default values
    url = "http://localhost:3000"

    def __init__(self, url=url):
        self.url = url
        if self.update_status():
            print "Connected to Volumio on " + self.url
        while True:
            self.update_status()
            time.sleep(1)

    def update_status(self):
        """Get status of Volumio"""
        try:
            state = requests.get(self.url+"/api/v1/getstate").json()
        except:
            print("Could not get Volumio state")
            return False
        self.title = state["title"]
        self.artist = state["artist"]
        self.duration = state["duration"]
        self.seek = int(state["seek"]/1000)
        self.volume = state["volume"]
        self.service = state["service"]
        self.status = state["status"]
        self.mute = state["mute"]
        return True

    def toggle_mute(self):
        """Mute or Unmute"""
        if self.mute == True:
            toggle = "unmute"
        elif self.mute == False:
            toggle = "mute"
        try:
            requests.get(self.url+"/api/v1/commands/?cmd=volume&volume="+toggle).json()
            self.update_status()
        except:
            print("Could not toggle mute/unmute")
            return False
        return True

    def volume_step(self, step):
        """Change volume, step being minus ou plus"""
        try:
            requests.get(self.url+"/api/v1/commands/?cmd=volume&volume="+step).json()
            self.update_status()
        except:
            print("Could not set volume")
            return False
        return True

# State example from Volumio API
#{"status":"play","position":0,"title":"La guerra è finita","artist":"Baustelle",
#"album":"La malavita","albumart":"/albumart?web=Baustelle/La%20malavita/extralarge&path=%2FNAS%2FMusic%2FBaustelle%20-%20La%20Malavita",
#"uri":"mnt/NAS/Music/Baustelle - La Malavita/02 la guerra è finita.mp3","trackType":"mp3","seek":4224,"duration":262,
#"samplerate":"44.1 KHz","bitdepth":"24 bit","channels":2,"random":null,"repeat":null,
#"repeatSingle":false,"consume":false,"volume":41,"mute":false,"stream":"mp3","updatedb":false,"volatile":false,"service":"mpd"}
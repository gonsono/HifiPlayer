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

    def update_status(self):
        """Get status of Volumio"""
        try:
            state = requests.get(self.url+"/api/v1/getstate").json()
        except:
            print("Could not get Volumio state")
            return False
        self.artist = " "
        self.duration = 0
        self.title = state["title"]
        if "artist" in state:
            self.artist = state["artist"]
        if "duration" in state:
            self.duration = state["duration"]
        self.seek = state["seek"]/1000.0
        self.volume = state["volume"]
        self.type = state["trackType"]
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


import requests
import time
import logging

# def get_status(url, last_refresh):
#     players = requests.get(url + "/api/player/status").json()
#     playing = [p["state"] for p in players if p["state"]=="playing"]
#     playing = [p["state"] for p in players if p["state"]=="playing"]
#     if len(playing)==1:
#         track = requests.get(url + "/api/track/metadata").json()
#         if track["title"] is not None: 
#             current = {
#                 "type": track["playerName"],
#                 "title": track["title"],
#                 "artist": track["artist"],
#                 "state": track["playerState"],
#                 "time": get_time()
#             }
#         else:
#             current = {
#                 "type": "none",
#                 "title": "",
#                 "artist": "",
#                 "state": "idle",
#                 "time": get_time()
#             }
#     elif len(playing)==0 and last
#     return current



class HifiBerry:
    """Class that allow interaction with HifiBerry API"""

    url = "http://localhost:81"

    def __init__(self, url=url):
        self.url = url
        self.last_refresh = time.time()
        if self.update_status():
            logging.info("Connected to HifiBerry on " + self.url)

    def update_status(self):
        """Get status of HifiBerry"""
        try:
            players = requests.get(self.url+"/api/player/status").json()
        except:
            logging.error("Could not get list of players")
            return False
        print(players)
        active = [p["state"] for players["players"] in players if p["state"]=="playing" or p["state"]=="paused"]
        print(active)
        if len(active)==1:
            try:
                track = requests.get(self.url + "/api/track/metadata").json()
            except:
                logging.error("Could not get track metadata")
                return False
            self.type = track["playerName"]
            self.title = track["title"]
            self.artist = track["artist"]
            self.state = track["playerState"]
        else:
            self.type = "none"
            self.title = ""
            self.artist = ""
            self.state = "idle"
        return True


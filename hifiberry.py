import requests
import time
import logging
import unidecode

class HifiBerry:
    """Class that allow interaction with HifiBerry API"""

    url = "http://localhost:81"

    def __init__(self, url=url):
        self.url = url
        self.last_pause = 0
        self.state = ""
        if self.update_status():
            logging.info("Connected to HifiBerry on " + self.url)
        
        logging.info(self.type)
        logging.info(self.title)
        logging.info(self.artist)
        logging.info(self.state)

    def update_status(self):
        """Get status of HifiBerry"""
        try:
            players = requests.get(self.url+"/api/player/status").json()
        except:
            logging.error("Could not get list of players")
            return False
        active = len([p["state"] for p in players["players"] if p["state"]=="playing"])
        paused = len([p["state"] for p in players["players"] if p["state"]=="paused"])
        if self.state == "playing" and paused == 1 and active == 0:
            self.last_pause = time.time()
            logging.info("Last Pause="+str(self.last_pause))

        if (active==1) or (paused==1 and self.last_pause > time.time()-60):
            logging.info("Found 1 player")
            try:
                track = requests.get(self.url + "/api/track/metadata").json()
            except:
                logging.error("Could not get track metadata")
                return False
            self.type = track["playerName"]
            if track["title"] is not None:
                self.title = unidecode.unidecode(track["title"])
            else:
                self.title = ""
            if track["artist"] is not None:
                self.artist = unidecode.unidecode(track["artist"])
            else:
                self.artist = ""
            self.state = track["playerState"]
        else:
            logging.info("Idle")
            self.type = "none"
            self.title = ""
            self.artist = ""
            self.state = "idle"
        return True


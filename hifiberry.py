import requests
import time

def get_time():
    current_time = time.strftime("%H:%M")
    return current_time

def get_status(url):
    r = requests.get(url + "/api/track/metadata").json()
    if r["title"] is not None:
        current = {
            "type": r["playerName"],
            "title": r["title"],
            "artist": r["artist"],
            "state": r["playerState"],
            "time": get_time()
        }
    else:
        current = {
            "type": "None",
            "title": "Idle",
            "artist": "",
            "state": "",
            "time": get_time()
        }
    return current

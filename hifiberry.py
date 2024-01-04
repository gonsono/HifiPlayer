import requests

def get_status(url):
    r = requests.get(url + "/api/track/metadata").json()
    if r["title"] is not None:
        current = {
            "type": r["playerName"],
            "title": r["title"],
            "artist": r["artist"]
        }
    else:
        current = {
            "type": "None",
            "title": "Idle",
            "artist": ""
        }
    # logging.debug(current)
    return current
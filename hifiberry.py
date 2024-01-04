import requests

def get_status():
    r = requests.get(url + "/api/track/metadata").json()
    current = {
        "type": r["playerName"],
        "title": r["title"],
        "artist": r["artist"]
    }
    logging.debug(current)
    return current
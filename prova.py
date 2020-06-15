import json
from urllib.request import urlopen

url = "https://api.telegram.org/bot109968/getMe"


def isTokenValid(token):
    url="https://api.telegram.org/bot"+token+"/getMe"
    try:
        response = urlopen(url)
        data = json.loads(response.read())
        if data['ok'] and token not in array:
            return True
        else:
            return False
    except:
        return False
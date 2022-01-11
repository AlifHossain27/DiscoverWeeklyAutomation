import os
import requests

refresh_token= os.getenv("REFRESH_TOKEN")
base_64= os.getenv("BASE_64")

class Refresh:

    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refreshing(self):

        query = "https://accounts.spotify.com/api/token"

        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": refresh_token},
                                 headers={"Authorization": "Basic " + base_64})

        response_json = response.json()

        return response_json["access_token"]


if __name__=="__main__":
    refresh= Refresh()
    refresh.refreshing()
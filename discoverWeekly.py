import os
import json
import requests
from datetime import date
from refresh import Refresh

user_id = os.getenv("USER")
discover_weekly_id = os.getenv("DISCOVER_WEEKLY_ID")

class SaveSongs:

    def __init__(self):
        self.user_id = user_id
        self.token = ""
        self.discover_weekly_id = discover_weekly_id
        self.tracks = ""
        self.new_playlist_id = ""

    def find_songs(self):

        print("Finding songs in discover weekly...")
        # Loop through playlist tracks, add them to list

        query = f"https://api.spotify.com/v1/playlists/{discover_weekly_id}/tracks"

        response = requests.get(query,
                                headers = {"Content-Type": "application/json",
                                         "Authorization": "Bearer {}".format(self.token)})

        response_json = response.json()

        for i in response_json["items"]:
            self.tracks += (i["track"]["uri"] + ",")
        self.tracks = self.tracks[:-1]
        
        self.add_to_playlist()

    
    def create_playlist(self)-> str:
        # Creating a new playlist
        print("Trying to create playlist...")
        today = date.today()

        todayFormatted = today.strftime("%d/%m/%Y")

        query = f"https://api.spotify.com/v1/users/{user_id}/playlists"

        request_body = json.dumps({
            "name": todayFormatted + " discover weekly", "description": "Discover weekly rescued once again from the brink of destruction by your friendly neighbourhood python script", "public": False
        })

        response = requests.post(query, data=request_body, headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token)
        })

        response_json = response.json()

        return response_json["id"]

    def add_to_playlist(self):
        # Adding all songs to new playlist
        print("Adding songs...")

        self.new_playlist_id = self.create_playlist()

        query = "https://api.spotify.com/v1/playlists/{}/tracks?uris={}".format(
            self.new_playlist_id, self.tracks)

        response = requests.post(query, headers={"Content-Type": "application/json",
                                                 "Authorization": "Bearer {}".format(self.token)})

    
    def call_refresh(self):

        print("Refreshing token...")

        refreshCaller = Refresh()

        self.token = refreshCaller.refreshing()
        
        self.find_songs()


if __name__=="__main__":
    songs=SaveSongs()
    songs.call_refresh()

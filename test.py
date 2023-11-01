import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import subprocess
from ytmusicapi import YTMusic
import time
import sys
from flask import Flask

app = Flask(__name__)

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
titles_xotic = []
xoticids = []
liked_videos = []
videotitles = []
videoids = []

total_songs_added = 0
songs_missed = 0


@app.route('/')
def home():
    return("hello world!")

@app.route('/first_account')
def first_account():
    
    client_secrets_file = "csgo.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)

    credentials = flow.run_local_server(port=8080)

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId="LM",
        maxResults=50
    )
    response = request.execute()

    while response:
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_title = item['snippet']['title']
            titles_xotic.append(video_title)
            xoticids.append(video_id)

        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId="LM",
                maxResults=50,
                pageToken=next_page_token
            )

            response = request.execute()
        else:
            break

    return f"Total 'Liked songs' from the first account: {response['pageInfo']['totalResults']}"


@app.route('/xotic_account')
def xotic_account():
    
    client_secrets_file = "csgoto.json"

    scopes2 = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes2)
    credentials = flow.run_local_server(port=8080)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId="LM",
        maxResults=50
    )

    response = request.execute()

    while response:
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video_title = item['snippet']['title']
            titles_xotic.append(video_title)
            xoticids.append(video_id)

        if 'nextPageToken' in response:
            next_page_token = response['nextPageToken']
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId="LM",
                maxResults=50,
                pageToken=next_page_token
            )

            response = request.execute()
        else:
            break

    return f"Total 'Liked songs' from the xotic account: {response['pageInfo']['totalResults']}"




if __name__ == '__main__':
    app.run()




'''

@app.route('/xotic_account')
def xotic_account():
    set_videoids = set(videoids)
    set_xoticids = set(xoticids)

    common_ids = set_videoids & set_xoticids
    uncommon_ids = set_videoids - set_xoticids
    common_ids_list = list(common_ids)
    uncommon_ids_list = list(uncommon_ids)

    print("missing from the second account: " + str(len(uncommon_ids_list)))
    print("common songs: " + str(len(common_ids_list)))

    # ... code for fetching Spotify data goes here ...

    for video_id in uncommon_ids_list:
        try:
            request = youtube.videos().getRating(id=video_id)
            response = request.execute()
            for item in response['items']:
                if item['rating'] == 'none':
                    request = youtube.videos().rate(
                        id=item['videoId'],
                        rating="like"
                    )
                    response = request.execute()
                    print(f"Video {item['videoId']} added to liked music.")
                else:
                    print(f"Video {item['videoId']} is already liked.")
        except googleapiclient.errors.HttpError as e:
            print(f"Error checking or adding videos to liked music: {str(e)}")

    # ... code for fetching Spotify data goes here ...

    print(f"\nTotal songs added: {total_songs_added}")
    print(f"Number of songs missed: {songs_missed}")
    print("Stopping the program.")




'''
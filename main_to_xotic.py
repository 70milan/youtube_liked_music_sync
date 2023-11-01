import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import subprocess
from ytmusicapi import YTMusic
import time
import sys


scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

print("Getting Information from the first account")

client_secrets_file = "csgo.json"

yt_ids = []
yt_titles = []  # To store video titles
yt_songs = []
problematic_videos = []

flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)

credentials = flow.run_local_server(port=8080)

youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

request = youtube.playlistItems().list(
    part="snippet,contentDetails",
    playlistId="LM",
    maxResults=50
)

# Display loading animation
animation = "|/-\\"
for i in range(10):
    time.sleep(0.1)
    sys.stdout.write("\r" + "Loading " + animation[i % len(animation)])
    sys.stdout.flush()


response = request.execute()


print("\nTotal 'Liked songs' from the first account: " + str(response['pageInfo']['totalResults']))


user_input = input("Do you want to continue (yes/no): ")

if user_input.lower() == 'yes':
    print("Continuing...")
    # ... code for fetching Spotify data goes here ...
else:
    print("Stopping the program.")
    sys.exit()

# Get bucket current
videotitles = []
videoids = []


while response:
    # Extract videoIds from the current page and add them to videoids 
    for item in response['items']:
        video_id = item['snippet']['resourceId']['videoId']
        video_title = item['snippet']['title']
        videotitles.append(video_title)
        videoids .append(video_id)
    
    # Check if there are more pages of results
    if 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
        # Make a new request for the next page of results
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId="LM",
            maxResults=50,  # You can adjust this number based on your needs
            pageToken=next_page_token
        )

                # Display loading animation
        animation = "|/-\\"
        for i in range(10):
            time.sleep(0.1)
            sys.stdout.write("\r" + "Loading " + animation[i % len(animation)])
            sys.stdout.flush()

        response = request.execute()
    else:
        # No more pages, exit the loop
        break
################################################################################################################
user_input = input("Do you want to proceed to the next step (yes/no): ")

if user_input.lower() == 'yes':
    print("fetching details from the Xotic account ")
    # ... code for fetching Spotify data goes here ...
else:
    print("Stopping the program.")
    sys.exit()


scopes2 = ["https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "csgo2.json"

# Create the YouTube API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes2)
credentials = flow.run_local_server(port=8080)
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)


request = youtube.playlistItems().list(
    part="snippet,contentDetails",
    playlistId="LM",
    maxResults=50
)

# Display loading animation
animation = "|/-\\"
for i in range(10):
    time.sleep(0.1)
    sys.stdout.write("\r" + "Loading " + animation[i % len(animation)])
    sys.stdout.flush()


response = request.execute()

print("\nTotal 'Liked songs' from the xotic account: " + str(response['pageInfo']['totalResults']))


user_input = input("Do you want to continue (yes/no): ")

if user_input.lower() == 'yes':
    print("Continuing...")
    # ... code for fetching Spotify data goes here ...
else:
    print("Stopping the program.")
    sys.exit()




titles_xotic = []
xoticids = []
liked_videos = []


while response:
    # Extract videoIds from the current page and add them to videoids 
    for item in response['items']:
        video_id = item['snippet']['resourceId']['videoId']
        video_title = item['snippet']['title']
        titles_xotic.append(video_title)
        xoticids .append(video_id)
    
    # Check if there are more pages of results
    if 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
        # Make a new request for the next page of results
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId="LM",
            maxResults=50,  # You can adjust this number based on your needs
            pageToken=next_page_token
        )
        animation = "|/-\\"
        for i in range(10):
            time.sleep(0.1)
            sys.stdout.write("\r" + "Loading " + animation[i % len(animation)])
            sys.stdout.flush()
        
        response = request.execute()
    else:
        break



set_videoids = set(videoids)
set_xoticids = set(xoticids)


animation = "|/-\\"
for i in range(10):
    time.sleep(0.1)
    sys.stdout.write("\r" + "Performing set operations " + animation[i % len(animation)])
    sys.stdout.flush()

common_ids = set_videoids & set_xoticids

uncommon_ids = set_videoids - set_xoticids

common_ids_list = list(common_ids)
uncommon_ids_list = list(uncommon_ids)



print("missing from the second account: " + str(len(uncommon_ids_list)))
print("common songs: " + str(len(common_ids_list)))

user_input = input("Do you want to continue to add missing songs to the xotic account from the first account (yes/no): ")

if user_input.lower() == 'yes':
    print("Continuing...")
    # ... code for fetching Spotify data goes here ...
else:
    print("Stopping the program.")
    sys.exit()



print("Only 100 songs allowed per day!")

total_songs_added = 0
songs_missed = 0

for video_id in uncommon_ids_list:
    try:
        # Check if the video is already liked
        request = youtube.videos().getRating(
            id=video_id
        )
        animation = "|/-\\"
        for i in range(10):
            time.sleep(0.1)
            sys.stdout.write("\r" + "Performing set operations " + animation[i % len(animation)])
            sys.stdout.flush()
        response = request.execute()
       
        for item in response['items']:
            if item['rating'] == 'none':
                # Rate the video as 'like' if it's not already liked
                request = youtube.videos().rate(
                    id=item['videoId'],
                    rating="like"
                )
                animation = "|/-\\"
                for i in range(10):
                    time.sleep(0.1)
                    sys.stdout.write("\r" + "Performing set operations " + animation[i % len(animation)])
                    sys.stdout.flush()
                response = request.execute()
                print(f"Video {item['videoId']} added to liked music.")
                total_songs_added += 1
            else:
                print(f"Video {item['videoId']} is already liked.")
    except googleapiclient.errors.HttpError as e:
        print(f"Error checking or adding videos to liked music: {str(e)}")
        songs_missed += 1

        

print(f"\nTotal songs added: {total_songs_added}")
print(f"Number of songs missed: {songs_missed}")

print("Stopping the program.")

# Timer with animation
animation = "|/-\\"
for i in range(10):
    sys.stdout.write("\r" + "Exiting in " + str(10 - i) + " seconds " + animation[i % len(animation)])
    sys.stdout.flush()
    time.sleep(1)

sys.exit()
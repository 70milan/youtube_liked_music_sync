import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import subprocess
from ytmusicapi import YTMusic

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"

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
response = request.execute()

print(response['pageInfo']['totalResults'])  # total

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
        response = request.execute()
    else:
        # No more pages, exit the loop
        break









# Add videos to Liked Music playlist
# liked_music_playlist_id = "LM"  Replace with the actual playlist ID for Liked Music


scopes2 = ["https://www.googleapis.com/auth/youtube.force-ssl"]
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "csgoto.json"

# Create the YouTube API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes2)
credentials = flow.run_local_server(port=8080)
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Split the videoids list into chunks of 50 (maximum allowed in a single API call)
video_chunks = [videoids[i:i+50] for i in range(0, len(videoids), 50)]



# Iterate through the video chunks and add them to the liked music of the second account
for chunk in video_chunks:
    try:
        # Check if the videos in the chunk are already liked
        request = youtube.videos().getRating(
            id=chunk
        )
        response = request.execute()
        
        # Iterate through the response and check if each video is already liked
        for item in response['items']:
            if item['rating'] == 'none':
                # Rate the video as 'like' if it's not already liked
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






'''



### second account ###


# Create the YouTube API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes2)
credentials = flow.run_local_server(port=8080)
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

# Split the videoids list into chunks of 50 (maximum allowed in a single API call)
video_chunks = [videoids[i:i+50] for i in range(0, len(videoids), 50)]



# Iterate through the video chunks and add them to the liked music of the second account
for chunk in video_chunks:
    try:
        # Check if the videos in the chunk are already liked
        request = youtube.videos().getRating(
            id=chunk
        )
        response = request.execute()
        
        # Iterate through the response and check if each video is already liked
        for item in response['items']:
            if item['rating'] == 'none':
                # Rate the video as 'like' if it's not already liked
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






scopes2 = ["https://www.googleapis.com/auth/youtube.force-ssl"]
client_secrets_file2 = "csgoto.json"



flow2 = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file2, scopes2)

credentials2 = flow2.run_local_server(port=8080)





youtube2 = googleapiclient.discovery.build(api_service_name,
                                           api_version,
                                           credentials=credentials2)


for item in response['items']:
    videoId = item['snippet']['resourceId']['videoId']
    request = youtube2.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": "LM",  # "LM" is the ID for the "liked songs" playlist
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": videoId
                }
            }
        }
    )
    response = request.execute()


'''
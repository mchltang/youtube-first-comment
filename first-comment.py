import os
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors
import time
from datetime import datetime
from pytz import timezone


def current_time():
    return datetime.now(timezone('EST'))


def get_latest_video(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=1
    )
    return request.execute()


def insert_top_level_comment(youtube, video_id, comment_text):
    request = youtube.commentThreads().insert(
        part="snippet",
        body={
            "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                    "snippet": {
                        "textOriginal": comment_text
                    }
                }
            }
        }
    )
    return request.execute()


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret_22372764053-9deei2ifedbr6fpqk355b3jplp66kute.apps.googleusercontent.com.json"

    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    # Beast's youtube uploads playlist
    beast_uploads = "UUX6OQ3DkcsbYNE6H8uQQuVA"

    starting_latest_video = get_latest_video(youtube, beast_uploads)

    # starting video
    starting_video_id = starting_latest_video['items'][0]['snippet']['resourceId']['videoId']
    starting_video_title = starting_latest_video['items'][0]['snippet']['title']
    latest_video_id = starting_latest_video['items'][0]['snippet']['resourceId']['videoId']
    latest_video_title = starting_latest_video['items'][0]['snippet']['title']

    while (latest_video_id == starting_video_id):
        print(current_time(), latest_video_id, latest_video_title)
        time.sleep(0.5)
        response = get_latest_video(youtube, beast_uploads)
        latest_video_id = response['items'][0]['snippet']['resourceId']['videoId']

    # as soon as the latest video is not equal to the starting video (aka, new upload)
    # insert a new top-level comment into the new video
    print("New video found! Inserting top level comment...")
    comment_text = "First!"
    response = insert_top_level_comment(youtube, latest_video_id, comment_text)
    print(response)


if __name__ == "__main__":
    main()

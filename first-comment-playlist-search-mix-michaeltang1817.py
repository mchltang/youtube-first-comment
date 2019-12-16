import os
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors
import time
from datetime import datetime
from pytz import timezone


def current_time():
    return datetime.now(timezone('EST'))


def get_latest_video_playlist(youtube, playlist_id):
    # get first 50 videos and sort by published datetime.
    # the google format for datetime is: 2019-12-14T20:59:57.000Z
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )
    response = request.execute()
    list_videos = response['items']
    list_videos_sorted = sorted(list_videos, key=lambda video: datetime.strptime(video['snippet']['publishedAt'],
                                                                                 '%Y-%m-%dT%H:%M:%S.%fZ'),
                                reverse=True)
    return list_videos_sorted[0]


def get_latest_video_search(youtube, channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        order="date",
        type="video"
    )
    response = request.execute()
    list_videos = response['items']
    return list_videos[0]


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
    client_secrets_file = "client_secret_96743203108-qtb5c7ik9ur3f4qiccqsh3v5kksmov4k.apps.googleusercontent.com.json"

    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    # Beast's youtube uploads playlist
    beast_channel = "UCX6OQ3DkcsbYNE6H8uQQuVA"
    beast_uploads = "UUX6OQ3DkcsbYNE6H8uQQuVA"
    gensoukyou_test_channel = "UCTWE0vIBTAT3F70PhO2EUCw"
    gensoukyou_test_uploads = "UUTWE0vIBTAT3F70PhO2EUCw"

    ############################### SEARCH METHOD ###############################
    starting_latest_video = get_latest_video_search(youtube, gensoukyou_test_channel)

    # starting video
    starting_video_id = starting_latest_video['id']['videoId']
    latest_video_id = starting_latest_video['id']['videoId']
    latest_video_title = starting_latest_video['snippet']['title']
    print(current_time(), latest_video_id, latest_video_title)

    counter = 0
    while (latest_video_id == starting_video_id):
        time.sleep(1)

        if counter % 2 == 0:
            response = get_latest_video_search(youtube, gensoukyou_test_channel)
            latest_video_id = response['id']['videoId']
            latest_video_title = response['snippet']['title']
            print("search", current_time(), latest_video_id, latest_video_title)
        else:
            response = get_latest_video_playlist(youtube, gensoukyou_test_uploads)
            latest_video_id = response['snippet']['resourceId']['videoId']
            latest_video_title = response['snippet']['title']
            print("playlist", current_time(), latest_video_id, latest_video_title)

        counter += 1

    # as soon as the latest video is not equal to the starting video (aka, new upload)
    # insert a new top-level comment into the new video
    comment_text = "Hey Mr. Beast, did I win a thousand bucks?"
    response = insert_top_level_comment(youtube, latest_video_id, comment_text)
    print(response)


if __name__ == "__main__":
    main()

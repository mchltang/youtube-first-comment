import os
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors
import time
from datetime import datetime
from pytz import timezone
import glob


def current_time():
    return datetime.now(timezone('EST'))


def current_timestamp():
    return datetime.now(timezone('EST')).timestamp()


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


def post_comment_on_new_video(youtube, channel_id, uploads_id, comment_text):
    # starting time
    starting_timestamp = current_timestamp()

    # starting video
    starting_latest_video = get_latest_video_search(youtube, channel_id)
    starting_video_id = starting_latest_video['id']['videoId']
    latest_video_id = starting_latest_video['id']['videoId']

    counter = 0
    while latest_video_id == starting_video_id and current_timestamp() < (starting_timestamp + 120):
        time.sleep(1)

        if counter % 2 == 0:
            response = get_latest_video_search(youtube, channel_id)
            latest_video_id = response['id']['videoId']
            latest_video_title = response['snippet']['title']
            print("search", current_time(), latest_video_id, latest_video_title)
        else:
            response = get_latest_video_playlist(youtube, uploads_id)
            latest_video_id = response['snippet']['resourceId']['videoId']
            latest_video_title = response['snippet']['title']
            print("playlist", current_time(), latest_video_id, latest_video_title)

        counter += 1

    # as soon as the latest video is not equal to the starting video (aka, new upload)
    # insert a new top-level comment into the new video
    if latest_video_id == starting_video_id:
        print('Data API script has ran for 2 minutes, stopping to conserve quota!')
    else:
        response = insert_top_level_comment(youtube, latest_video_id, comment_text)
        print(response)


def get_channel_id_from_username(youtube, username):
    request = youtube.channels().list(
        part="id",
        forUsername=username
    )
    response = request.execute()
    return response['items'][0]['id']


def create_youtube_object(client_secrets_file):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    return youtube


def main():
    # Beast's youtube uploads playlist
    beast_channel = "UCX6OQ3DkcsbYNE6H8uQQuVA"
    beast_uploads = "UUX6OQ3DkcsbYNE6H8uQQuVA"

    # ask which client secrets file user wishes to use
    print("List of available client secret files:\n")
    os.chdir("./client_secret_files")
    ints_to_filenames = {}
    client_secret_index = 1
    for file in glob.glob("*.json"):
        print("[" + str(client_secret_index) + "]" + ": " + file)
        ints_to_filenames[client_secret_index] = str(file)
        client_secret_index += 1

    chosen_file_index = input("\nPlease enter the number corresponding to the client secret file you want to use: ")
    client_secret_file = ints_to_filenames[int(chosen_file_index)]
    print(
        "\nOn the page that pops up in your browser, please select the SAME GOOGLE ACCOUNT associated with the client secret file " + client_secret_file + "\n")
    youtube = create_youtube_object(client_secret_file)

    # ask for user to paste the link of the channel in, or use mr. beast's channel
    channel_id = ""
    uploads_id = ""
    channel_link = input(
        "\nPlease paste the link of the channel or user publishing the new video (Press [ENTER] to use Mr. Beast's channel): ")
    if channel_link == "":
        channel_id = beast_channel
        uploads_id = beast_uploads
    else:
        link_type = channel_link.split("youtube.com/")[1].split("/")[0]
        link_data = list(channel_link.split("youtube.com/")[1].split("/")[1])
        if link_type == "channel":
            channel_id = "".join(link_data).strip()
            link_data[1] = 'U'
            uploads_id = "".join(link_data).strip()
        elif link_type == "user":
            channel_id = get_channel_id_from_username(youtube, "".join(link_data).strip())
            uploads_id_list = list(channel_id)
            uploads_id_list[1] = 'U'
            uploads_id = "".join(uploads_id_list)

    print("\nFound channel ID for entered user to be " + channel_id + "\n")

    # [L] to perform a single refresh, [A] to automatically perform refreshes from now on
    input_rate = input(
        "Press:\n[ENTER] to perform a single refresh on this channel's videos,\n[A] to start scanning for new video.\nYour choice: ")
    while input_rate != 'a' and input_rate != 'A':
        response_search = get_latest_video_search(youtube, channel_id)
        latest_video_id_search = response_search['id']['videoId']
        latest_video_title_search = response_search['snippet']['title']
        print("\nSearch query result at " + str(current_time()) + ": " + str(
            latest_video_id_search) + " " + latest_video_title_search)

        time.sleep(1)

        response_playlist = get_latest_video_playlist(youtube, uploads_id)
        latest_video_id_playlist = response_playlist['snippet']['resourceId']['videoId']
        latest_video_title_playlist = response_playlist['snippet']['title']
        print("Playlist query result at " + str(current_time()) + ": " + str(
            latest_video_id_playlist) + " " + latest_video_title_playlist)

        input_rate = input_rate = input(
            "\nPress:\n[ENTER] to perform a single refresh on this channel's videos,\n[A] to start scanning for new video.\nYour choice: ")

    # if user presses [A], ask for comment
    while True:
        comment_text = input(
            '\nPlease enter your comment text (Do not enter a comment like "First", make it longer and more descriptive so it isn\'t flagged as spam):\n')
        comment_confirm = input('\nYour comment will be: "' + comment_text + '".\nIs this okay?\n[Y]es [N]o: ')
        if comment_confirm == 'y' or comment_confirm == 'Y':
            break

    while True:
        autostart = input(
            "\nEnter:\n[A] to automatically start at 3:59:50 PM EST,\n[T] to specify a time at which to start scanning,\n[M] to manually choose when to start scanning\nYour choice: ")
        if autostart == 'm' or autostart == 'M' or autostart == 'a' or autostart == 'A' or autostart == 't' or autostart == 'T':
            break

    if autostart == 'm' or autostart == 'M':
        input(
            "\nPress [ENTER] to begin scanning (if you are doing this for Mr. Beast's challenge, press [ENTER] at 3:59:50 PM): ")
        print("\n")

        post_comment_on_new_video(youtube, channel_id, uploads_id, comment_text)

    elif autostart == 'a' or autostart == 'A':
        beast_timestamp = 1576789190

        print("\nThe current time is " + str(current_time()) + ", " + str(
            (int(beast_timestamp) - int(current_timestamp()))) + " seconds left until scanning starts...")

        while (current_timestamp() < beast_timestamp):
            time.sleep(1)
            print("The current time is " + str(current_time()) + ", " + str(
                (int(beast_timestamp) - int(current_timestamp()))) + " seconds left until scanning starts...")

        post_comment_on_new_video(youtube, channel_id, uploads_id, comment_text)

    elif autostart == 't' or autostart == 'T':
        while True:
            year = input("Year (YYYY): ")
            month = input("Month (MM): ")
            day = input("Day (DD): ")
            hours = input("Hours (on a 24 hour scale, so 00 - 24) (HH): ")
            minutes = input("Minutes (MM): ")
            seconds = input("Seconds (SS): ")
            date_string = year + '-' + month + '-' + day + ' ' + hours + ':' + minutes + ':' + seconds
            target_timestamp = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").timestamp()
            time_confirmation = input(
                "The program will begin scanning at: " + date_string + ", is this okay?\n[Y]es [N]o: ")
            if time_confirmation == 'y' or time_confirmation == 'Y':
                break

        print("\nThe current time is " + str(current_time()) + ", " + str(
            (int(target_timestamp) - int(current_timestamp()))) + " seconds left until scanning starts...")

        while (current_timestamp() < target_timestamp):
            time.sleep(1)
            print("The current time is " + str(current_time()) + ", " + str(
                (int(target_timestamp) - int(current_timestamp()))) + " seconds left until scanning starts...")

        post_comment_on_new_video(youtube, channel_id, uploads_id, comment_text)


if __name__ == "__main__":
    main()

import os
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors
import time
from datetime import datetime
from pytz import timezone
import glob
import urllib.request


def current_time():
    return datetime.now(timezone('EST'))


def current_timestamp():
    return datetime.now(timezone('EST')).timestamp()


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


def reload_page_and_comment(youtube, comment_text):
    urls = [
        # Mr. Beast youtube links
        "https://www.youtube.com/user/MrBeast6000",
        "https://www.youtube.com/user/MrBeast6000/videos",
        "https://www.youtube.com/user/MrBeast6000/featured",
        "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA/videos",
        "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA",
        "https://www.youtube.com/user/MrBeast6000/videos",
        "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA/featured",
        "https://www.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA/videos",

        # # gensoukyou radio channel, for testing
        # "https://www.youtube.com/channel/UCTWE0vIBTAT3F70PhO2EUCw",
        # "https://www.youtube.com/channel/UCTWE0vIBTAT3F70PhO2EUCw/videos",
        # "https://www.youtube.com/channel/UCTWE0vIBTAT3F70PhO2EUCw/featured",
        # "https://www.youtube.com/channel/UCTWE0vIBTAT3F70PhO2EUCw/videos",
    ]

    # Mr. Beast youtube link
    url_for_first_load = "https://www.youtube.com/user/MrBeast6000/videos"

    # # gensoukyou radio channel, for testing
    # url_for_first_load = "https://www.youtube.com/channel/UCTWE0vIBTAT3F70PhO2EUCw/videos"

    user_agent_strings = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
    ]

    # load the page once to get the current latest video
    hdr = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }

    req = urllib.request.Request(url_for_first_load, headers=hdr)
    response = urllib.request.urlopen(req)
    page_contents = response.read()
    decoded_page_contents = page_contents.decode()
    first_video_id = decoded_page_contents.split('"videoId":"')[1]

    latest_video_id = first_video_id.split('"')[0]
    current_video_id = first_video_id.split('"')[0]

    counter = 0
    while current_video_id == latest_video_id:
        hdr = {
            'User-Agent': user_agent_strings[counter % len(user_agent_strings)],
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        req = urllib.request.Request(urls[counter % len(urls)], headers=hdr)
        response = urllib.request.urlopen(req)
        page_contents = response.read()
        decoded_page_contents = page_contents.decode()
        if 'videos' in urls[counter % len(urls)]:
            first_video_id = decoded_page_contents.split('"videoId":"')[1]
            current_video_id = first_video_id.split('"')[0]
        else:
            uploads = decoded_page_contents.split('Uploads')[1]
            first_video_id = uploads.split('"videoId":"')[1]
            current_video_id = first_video_id.split('"')[0]
        print(str(current_time()) + " URL " + str(counter % len(urls)) + " current video ID = " + current_video_id)
        counter += 1

    insert_top_level_comment(youtube, current_video_id, comment_text)
    print("Commented!")


def main():
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

    print("\nMake sure the correct Youtube channel is uncommented in this Python file!")

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

        reload_page_and_comment(youtube, comment_text)

    elif autostart == 'a' or autostart == 'A':
        beast_timestamp = 1576789190

        print("\nThe current time is " + str(current_time()) + ", " + str(
            (int(beast_timestamp) - int(current_timestamp()))) + " seconds left until scanning starts...")

        while (current_timestamp() < beast_timestamp):
            time.sleep(1)
            print("The current time is " + str(current_time()) + ", " + str(
                (int(beast_timestamp) - int(current_timestamp()))) + " seconds left until scanning starts...")

        reload_page_and_comment(youtube, comment_text)

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

        reload_page_and_comment(youtube, comment_text)


if __name__ == "__main__":
    main()

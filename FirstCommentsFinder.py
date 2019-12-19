import os
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors
import time
from datetime import datetime
from pytz import timezone
import glob


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
    video_id = input("Enter the video ID to begin: ")

    request = youtube.commentThreads().list(
        part="id",
        maxResults=100,
        order="time",
        pageToken='QURTSl9pMkx4bThiMjZ6VC1OU0gwNEliWGdOQnZQNUVITF8zcjFsd3pXNUVqOE5qek5xMVdwaUVWNmNnaXk4R3Vyb0ZxWEQzNDV6M25Ca0xHcUNPRE9RUkN6Sk5aUGVubEdXQXNaYTBpb2tNM0F4TWlDejBVZDZOcGdfWnJmYngxanYzSVhLTUNEOXdCTUcxVHVtOGJ3',
        videoId=video_id
    )
    response = request.execute()

    # counter = 1
    # while "nextPageToken" in response:
    #     if response['nextPageToken'] != "":
    #         request = youtube.commentThreads().list(
    #             part="id",
    #             maxResults=100,
    #             order="time",
    #             pageToken=response['nextPageToken'],
    #             videoId=video_id
    #         )
    #         response = request.execute()
    #         print(str(counter * 100) + " comments processed, next pageToken = " + response['nextPageToken'])
    #         counter += 1
    #     else:
    #         break

    print(response)


if __name__ == "__main__":
    main()

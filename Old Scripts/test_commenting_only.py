import os
import googleapiclient.discovery
import google_auth_oauthlib.flow
import googleapiclient.errors


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
    client_secrets_file_mchltang = "client_secret_22372764053-9deei2ifedbr6fpqk355b3jplp66kute.apps.googleusercontent.com.json"
    client_secrets_file_michaeltang1817 = "client_secret_96743203108-qtb5c7ik9ur3f4qiccqsh3v5kksmov4k.apps.googleusercontent.com.json"

    scopes = ['https://www.googleapis.com/auth/youtube.force-ssl']

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file_michaeltang1817,
                                                                               scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    comment_text = "Does this comment even show up? Hope you guys see this."
    response = insert_top_level_comment(youtube, "HjfvTGlcEXI", comment_text)
    print(response)


if __name__ == "__main__":
    main()

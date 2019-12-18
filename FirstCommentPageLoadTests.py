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

def main():
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
    ]

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

    counter = 0
    while counter < 3 * len(urls):
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
            # uploads = decoded_page_contents.split('Play all')[1]
            first_video_id = uploads.split('"videoId":"')[1]
            current_video_id = first_video_id.split('"')[0]
        print(str(current_time()) + " URL " + str(counter % len(urls)) + " current video ID = " + current_video_id)
        counter += 1

    urls = [
        # Mr. Beast youtube links
        "https://m.youtube.com/user/MrBeast6000",
        "https://m.youtube.com/user/MrBeast6000/videos",
        "https://m.youtube.com/user/MrBeast6000/featured",
        "https://m.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA/videos",
        "https://m.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA",
        "https://m.youtube.com/user/MrBeast6000/videos",
        "https://m.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA/featured",
        "https://m.youtube.com/channel/UCX6OQ3DkcsbYNE6H8uQQuVA/videos",
    ]

    user_agent_strings = [
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.116 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.92 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.62 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.143 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.89 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.96 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.62 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3828.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3880.5 Mobile Safari/537.36',
    ]

    counter = 0
    while counter < 3 * len(urls):
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
            # uploads = decoded_page_contents.split('Play all')[1]
            first_video_id = uploads.split('"videoId":"')[1]
            current_video_id = first_video_id.split('"')[0]
        print(str(current_time()) + " URL " + str(counter % len(urls)) + " current video ID = " + current_video_id)
        counter += 1

if __name__ == "__main__":
    main()
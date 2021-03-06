from datetime import datetime
from pytz import timezone
import urllib.request
import random


def current_time():
    return datetime.now(timezone('EST'))


def current_timestamp():
    return datetime.now(timezone('EST')).timestamp()


def main():
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
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; ONEPLUS 6T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.112 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; OnePlus 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.73 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; OnePlus 7 Pro) AppleWebKit/537.36 (KHTML; like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 10; OnePlus 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.186 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; OnePlus 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; OnePlus 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.111 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; OnePlus 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.92 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; OnePlus 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.89 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 9; OnePlus 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.143 Mobile Safari/537.36',
    ]

    counter = 0
    while True:
        hdr = {
            'User-Agent': random.choice(user_agent_strings),
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

import os, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

videos = os.listdir("videos")
if not videos:
    print("No video")
    exit()

video = sorted(videos)[0]

creds = Credentials(
    None,
    refresh_token=os.environ["REFRESH_TOKEN"],
    token_uri="https://oauth2.googleapis.com/token",
    client_id=json.loads(os.environ["CLIENT_SECRET_JSON"])["installed"]["client_id"],
    client_secret=json.loads(os.environ["CLIENT_SECRET_JSON"])["installed"]["client_secret"],
)

youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": video,
            "description": "Auto upload",
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload(f"videos/{video}")
)

request.execute()
os.remove(f"videos/{video}")

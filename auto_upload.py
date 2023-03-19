import requests

def upload_tiktok(access_token, video_file_path):
    video_upload_url = "https://open-api.tiktok.com/video/upload/?access_token=" + access_token
    response = requests.post(video_upload_url, files={'video': open(video_file_path, 'rb')})

    if response.status_code == 200:
        upload_id = response.json()["upload_id"]
        print("Video uploaded successfully with upload ID: " + upload_id)
    else:
        print("Error uploading video: " + response.json()["message"])

    # Publish video
    publish_url = "https://open-api.tiktok.com/video/publish/?access_token=" + access_token

    description = "VIDEO_DESCRIPTION"
    cover_url = "COVER_IMAGE_URL"
    music_id = "MUSIC_ID"
    challenge_id = "CHALLENGE_ID"
    is_ad = "false"
    is_private = "false"

    data = {
        "upload_id": upload_id,
        "description": description,
        "cover_url": cover_url,
        "music_id": music_id,
        "challenge_id": challenge_id,
        "is_ad": is_ad,
        "is_private": is_private
    }

    response = requests.post(publish_url, data=data)

    if response.status_code == 200:
        video_id = response.json()["item_id"]
        print("Video published successfully with video ID: " + video_id)
    else:
        print("Error publishing video: " + response.json()["message"])

if __name__ == "__main__":
    access_token = "YOUR_ACCESS_TOKEN"
    video_file_path = "PATH_TO_VIDEO_FILE"
    upload_tiktok(access_token, video_file_path)
# api_service/tasks.py
import requests
import boto3
from celery import shared_task
from django.conf import settings
from urllib.parse import urlparse, parse_qs
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

META_SERVICE_API=settings.META_SERVICE_API

SERVICE_ACCOUNT_FILE = 'service-account.json'




@shared_task
def process_drive_folder(folder_url):
    
    SCOPES = ['https://www.googleapis.com/auth/drive']
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive_service = build('drive', 'v3', credentials=creds)

    # 1. List files in the folder
    results = drive_service.files().list(
        q=f"'{folder_url}' in parents and mimeType contains 'image/'",
        fields="files(id, name, mimeType, size)"
    ).execute()

    files = results.get("files", [])




    url = META_SERVICE_API+"/api/image-processing/"

    payload = {
        "files": [
            {"id": f["id"], "name": f["name"], "mimeType": f["mimeType"]}
            for f in files
        ]
    }

    response = requests.post(url, json=payload)
    
    if response.status_code == 201:
        return {"status": "success", "uploaded_files": [f["name"] for f in files]}
    else:
        return {"status": "failed", "response": response.text}




    # for f in files:
    #     file_id, file_name, mime_type, size = (
    #         f["id"],
    #         f["name"],
    #         f["mimeType"],
    #         int(f.get("size", 0)),
    #     )

    #     # 2. Download image from Google Drive
    #     request_dl = drive_service.files().get_media(fileId=file_id)
    #     fh = io.BytesIO()
    #     downloader = MediaIoBaseDownload(fh, request_dl)
    #     done = False
    #     while not done:
    #         status_dl, done = downloader.next_chunk()

    #     fh.seek(0)  # Reset buffer pointer

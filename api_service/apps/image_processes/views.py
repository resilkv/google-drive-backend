import io
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .tasks import process_drive_folder
from urllib.parse import urlparse, parse_qs
from apps.image_processes.tasks import process_drive_folder
from config import settings
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from .serializers import GoogleImagePostSerializer
from drf_yasg.utils import swagger_auto_schema

SERVICE_ACCOUNT_FILE = 'service-account.json'


class GoogleDriveImportView(APIView):

    def extract_folder_id(self,folder_url: str) -> str:
        
        parsed = urlparse(folder_url)
        if "folders" in parsed.path:
            return parsed.path.split("/")[-1]
        return parse_qs(parsed.query).get("id", [None])[0]


    serializer_class = GoogleImagePostSerializer

    @swagger_auto_schema(tags=["Google Image"],request_body=serializer_class)
    def post(self, request):

        
        folder_url = request.data.get("folder_url")
        if not folder_url:
            return Response({"error": "Folder URL is required"}, status=status.HTTP_400_BAD_REQUEST)

      
        folder_id = self.extract_folder_id(folder_url)
        if not folder_id:
            return Response({"error": "Invalid Google Drive Folder URL"}, status=status.HTTP_400_BAD_REQUEST)
        
        process_drive_folder.delay(folder_id)
        
        # SCOPES = ['https://www.googleapis.com/auth/drive']
        # creds = service_account.Credentials.from_service_account_file(
        #     SERVICE_ACCOUNT_FILE, scopes=SCOPES
        # )
        # drive_service = build('drive', 'v3', credentials=creds)

       
        # # 1. List files in the folder
        # results = drive_service.files().list(
        #     q=f"'{folder_id}' in parents and mimeType contains 'image/'",
        #     fields="files(id, name, mimeType, size)"
        # ).execute()

        # files = results.get("files", [])




        # url = settings.META_SERVICE_API+"/api/image-processing/"

        # payload = {
        #     "files": files
        # }

        # response = requests.post(url, json=payload)
        
        # if response.status_code == 201:
        #     return {"status": "success", "uploaded_files": [f["name"] for f in files]}
        # else:
        #     return {"status": "failed", "response": response.text}



        # Load service account credentials
        
            # 3. Upload to S3
            # s3_key = f"images/{file_name}"
            # s3_client.upload_fileobj(img_resp.raw, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

            # s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"




        # Trigger async task
        # process_drive_folder.delay(folder_url)

        return Response({"message": "Import started. Check status later."}, status=status.HTTP_202_ACCEPTED)

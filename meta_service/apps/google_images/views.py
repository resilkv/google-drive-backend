from django.shortcuts import render
from rest_framework.views import APIView

from apps.google_images.models import GoogleImage
from apps.google_images.schemas import GetImageSchema
from .serializers import GoogleImagePostSerializer, GoogleImageSaveSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
import boto3
from config import settings
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2 import service_account
from io import BytesIO
from googleapiclient.discovery import build


SERVICE_ACCOUNT_FILE = 'service-account.json'


# Create your views here.
class GoogleImageListAPIView(APIView):

    serializer_class = GoogleImagePostSerializer
    image_save_serializer = GoogleImageSaveSerializer

    @swagger_auto_schema(tags=["Google Image"])
    def post(self,request):
        
        
        try:
            files = request.data.get("files", [])
            if not files:
                return Response({"status_code": 400, "error": "No files provided"}, status=status.HTTP_400_BAD_REQUEST)
            
            uploaded_files = []
         
            s3_client = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )

            # Initialize Google Drive service
            SCOPES = ['https://www.googleapis.com/auth/drive']
            creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
            drive_service = build('drive', 'v3', credentials=creds)

            for file in files:
               
                file_id = file.get("id")
                file_name = file.get("name")
                request_drive = drive_service.files().get_media(fileId=file_id)
                fh = BytesIO()
                downloader = MediaIoBaseDownload(fh, request_drive)
                done = False
                while not done:
                    download_status, done = downloader.next_chunk()
                fh.seek(0)

                # 2️⃣ Upload to S3
                s3_key = f"google_images/{file_name}"  # folder in your bucket
                s3_client.upload_fileobj(fh, settings.AWS_STORAGE_BUCKET_NAME, s3_key)

                s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"

                # 3️⃣ Save metadata to DB
                data = {
                    "name": file_name,
                    "google_drive_id": file_id,
                    "size": int(file.get("size", 0)),
                    "mime_type": file.get("mimeType"),
                    "storage_path": s3_url
                }
                serializer = self.image_save_serializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    uploaded_files.append(file.get("name"))
                else:
                 
                    print(f"Failed to save {file.get('name')}: {serializer.errors}")

            return Response({"status_code": 201, "uploaded_files": uploaded_files},status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"status_code": 500, "error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GoogleImageListing(APIView):

    serializer = GetImageSchema

    def get(self,request,*arg,**kwrg):

        try:

            queryset = GoogleImage.objects.all()
            serializer =  self.serializer(queryset,many=True)

            return Response({"status_code": 200,"data": serializer.data},status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"status_code": 500, "error": str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

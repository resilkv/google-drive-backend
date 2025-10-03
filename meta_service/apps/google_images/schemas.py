from rest_framework import serializers
from .models import GoogleImage

class GetImageSchema(serializers.ModelSerializer):

    class Meta:
        model = GoogleImage
        fields = ['id','name','google_drive_id','size','mime_type','storage_path','created_at']
    
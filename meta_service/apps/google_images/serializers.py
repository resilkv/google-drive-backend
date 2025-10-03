from rest_framework import serializers

from apps.google_images.models import GoogleImage


class GoogleImagePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleImage
        fields = ["name", "google_drive_id", "size", "mime_type"]


class GoogleImageSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoogleImage
        fields = ["name", "google_drive_id", "size", "mime_type",'storage_path']
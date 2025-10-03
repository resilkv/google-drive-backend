from rest_framework import serializers

class GoogleImagePostSerializer(serializers.Serializer):

    folder_url = serializers.URLField()
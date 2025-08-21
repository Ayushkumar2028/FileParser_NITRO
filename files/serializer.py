from rest_framework import serializers
from . models import FileUpload

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model=FileUpload
        fields=["id",
            "filename",
            "status",
            "progress",
            "created_at",]

from django.db import models
import uuid

# Create your models here.
class FileUpload(models.Model):
    Status_Choice=[
        ("uploading","Uploading"),
        ("processing","Processing"),
        ("ready","Ready"),
        ("failed","Failed")
    ]
    filename=models.CharField(max_length=200)
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    file=models.FileField(upload_to="uploads/")
    status=models.CharField(default="uploading",choices=Status_Choice,max_length=200)
    progress=models.IntegerField(default=0)
    parsed_data=models.JSONField(null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.filename


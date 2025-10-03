from django.db import models

# Create your models here.



class GoogleImage(models.Model):

    name = models.CharField(max_length=250,db_index=True,help_text="image name")
    google_drive_id  = models.CharField(max_length=250,help_text="google drive ID",null=True,blank=True)
    size = models.IntegerField(null=True,blank=True,help_text="file size(bytes)")
    mime_type = models.CharField(max_length=250)
    storage_path = models.URLField(help_text="S3 URL",db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.google_drive_id})"

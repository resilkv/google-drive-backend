from django.urls import path
from . import views

urlpatterns = [
    path('image-processing/', views.GoogleDriveImportView.as_view(), name='image-processing'),
]

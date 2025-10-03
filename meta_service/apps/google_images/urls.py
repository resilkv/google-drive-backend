from django.urls import path
from . import views

urlpatterns = [
    path('image-processing/', views.GoogleImageListAPIView.as_view(), name='image-processing'),
    path('image-listing/', views.GoogleImageListing.as_view(), name='image-listing'),
]


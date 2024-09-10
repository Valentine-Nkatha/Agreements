from django.urls import path
from .views import upload_image_page

urlpatterns = [
    path('upload/', upload_image_page, name='upload_image_page'),
]

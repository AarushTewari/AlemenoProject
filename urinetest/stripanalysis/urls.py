from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('upload/', ImageUploadView.as_view(), name='image-upload'),
]

from django.urls import path

from .views import (
    Directory,
    Download,
)

urlpatterns = [
    path('', Directory.as_view(), name='home'),
    path('download/', Download.as_view(), name='download'),
]
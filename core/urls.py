from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

from .views import (
    Directory,
    Download,
    NewFolder,
)

urlpatterns = [
    path('', login_required(Directory.as_view()), name='home'),
    #path('download/', login_required(Download.as_view()), name='download'),
    path('new-folder/', login_required(NewFolder.as_view()), name='new_folder'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
]
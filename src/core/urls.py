from django.urls import path
from .views import home, download_template

urlpatterns = [
    path('', home, name='home'),
    path('download-template/', download_template, name='download_template'),
]
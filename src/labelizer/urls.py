from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('core.urls')),
    path('staff/', include('staff.urls')),
    path('my-profile/', include('uprofile.urls')),
]
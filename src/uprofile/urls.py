from django.urls import path
from .views import profile, update_password, update_avatar

urlpatterns = [
    path('', profile, name='my_profile'),
    path('update-password/', update_password, name='update_password'),
    path('update-avatar/', update_avatar, name='update_avatar'),

]
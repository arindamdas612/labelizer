from django.urls import path
from .views import staff, change_status, change_role, delete_staff, reset_password

urlpatterns = [
    path('', staff, name='all_staff'),
    path('change-status/<int:staff_id>', change_status, name='change_status'),
    path('change-role/<int:staff_id>', change_role, name='change_role'),
    path('delete/<int:staff_id>', delete_staff, name='delete_staff'),
    path('reset_password/<int:staff_id>', reset_password, name='reset_password'),
]

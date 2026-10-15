
from django.urls import path, include
from .views import (
    employee_list,
    edit_employee,
    remove_employee,
    register_user,
    link_employee_account,
)

urlpatterns = [
    path('', employee_list, name='employee_list'),
    path(
        'edit/<int:employee_id>/',
        edit_employee,
        name='edit_employee',
    ),
    path(
        'remove/<int:employee_id>/',
        remove_employee,
        name='remove_employee',
    ),
    path(
        'link-account/<int:employee_id>/',
        link_employee_account,
        name='link_employee_account',
    ),
    path('register/', register_user, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
]

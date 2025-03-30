from django.urls import path
from .views import (
    role_list_create, user_list_create, user_detail, 
    patient_list_create, specialist_list_create, 
    disorder_list_create, report_list_create
)

urlpatterns = [
    path('roles/', role_list_create, name='role-list-create'),
    path('users/', user_list_create, name='user-list-create'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('patients/', patient_list_create, name='patient-list-create'),
    path('specialists/', specialist_list_create, name='specialist-list-create'),
    path('disorders/', disorder_list_create, name='disorder-list-create'),
    path('reports/', report_list_create, name='report-list-create'),
]

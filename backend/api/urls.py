from django.urls import path
from . import views

urlpatterns = [
    path('create_role/', views.list_create_role_view, name='roles'),
    path('role_info/<int:pk>/', views.retreive_update_destroy_role_view, name='role_info'),

    path('create_custom_user/', views.list_create_user_view, name='custom_user'),
    path('custom_user_info/<int:pk>/', views.retreive_update_destroy_user_view, name='custom_user'),
    path('user_login/', views.user_login, name='user_login'),

    path('create_patient/', views.list_create_patient_view, name='patients'),
    path('patient_info/<int:pk>/', views.retreive_update_destroy_patient_view, name='patient_info'),

    path('create_specialist/', views.list_create_specialist_view, name='specialists'),
    path('specialist_info/<int:pk>/', views.retreive_update_destroy_specialist_view, name='specialist_info'),

    path('create_disorder/', views.list_create_disorder_view, name='disorders'),
    path('disorder_info/<int:pk>/', views.retreive_update_destroy_disorder_view, name='disorder_info'),

    path('create_report/', views.list_create_report_view, name='reports'),
    path('report_info/<int:pk>/', views.retreive_update_destroy_report_view, name='report_info'),
]

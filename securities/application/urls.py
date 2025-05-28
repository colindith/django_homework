from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.apply_view, name='apply'),
    path('status/', views.application_status_view, name='application_status'),
    path('update/', views.update_application_view, name='update_application'),
]
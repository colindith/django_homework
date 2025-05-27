from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='/login', permanent=True)),
    path('login', views.user_login_view, name='user_login'),
    path('logout', views.user_logout_view, name='user_logout'),
]
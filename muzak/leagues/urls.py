from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.league_home, name='league_home'),
    # path('profile/', views.profile, name='profile'),
]

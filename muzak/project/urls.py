from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.cover_page, name='home'),
    path('profile/', views.profile, name='profile'),
]

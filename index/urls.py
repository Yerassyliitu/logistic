from django.urls import path
from rest_framework.routers import DefaultRouter

from index import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
]
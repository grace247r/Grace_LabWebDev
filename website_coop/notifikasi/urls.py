# di notifikasi/urls.py
from django.urls import path
from . import views

app_name = 'notifikasi'

urlpatterns = [
    path('', views.notifikasi_view, name='daftar_notifikasi'),
]
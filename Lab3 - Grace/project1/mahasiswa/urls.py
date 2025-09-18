from django.urls import path
from . import views

urlpatterns = [
    path('',views.mahasiswa, name='mahasiswa')
]
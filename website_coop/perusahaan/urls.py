from django.urls import path
from . import views

app_name = 'perusahaan'

urlpatterns = [
    path('dashboard/', views.perusahaan_dashboard_view, name='dashboard'),
    path('evaluasi/', views.daftar_evaluasi_view, name='daftar_evaluasi')
]
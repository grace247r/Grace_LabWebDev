# di mahasiswa/urls.py
from django.urls import path
from . import views

app_name = 'mahasiswa'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profil/', views.profil_view, name='profil'),
    path('sertifikat/', views.sertifikat_view, name='sertifikat'),
    path('unggah-berkas/', views.unggah_berkas_view, name='unggah_berkas'),
    path('lapor-pencarian/', views.LaporMingguanView.as_view(), name='form_lapor_mingguan'),
]
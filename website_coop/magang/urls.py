# magang/urls.py
from django.urls import path
from . import views
# Tidak perlu from .views import LaporanMagangCreateView lagi (sudah dikoreksi)

app_name = 'magang'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('konfirmasi/', views.konfirmasi_magang_view, name='konfirmasi_magang'),

    
    # URL SUBMIT: Form Laporan Magang (Bulanan atau Akhir)
    path('laporan/<str:jenis_laporan>/submit/', 
         views.LaporanMagangCreateView.as_view(), 
         name='submit_laporan_magang'),

    path('lowongan/', views.daftar_lowongan_view, name='daftar_lowongan'),

    path('lowongan/<int:pk>/', views.detail_lowongan_view, name='detail_lowongan'), 

    path('admin/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),

    path('admin/mahasiswa/', views.daftar_mahasiswa_admin_view, name='admin_daftar_mahasiswa'),

    path('redirect/', views.user_redirect_view, name='user_redirect'),

    path('admin/profil/', views.admin_profil_view, name='admin_profil'),
    
    path('admin/notifikasi/', views.admin_notifikasi_view, name='admin_notifikasi'),

    path('admin/berkas-mahasiswa/', views.admin_berkas_mahasiswa_view, name='admin_berkas_mahasiswa'),

    path('admin/pantau-evaluasi/', views.admin_pantau_evaluasi_view, name='admin_pantau_evaluasi'),

    path('admin/kelola-lowongan/', views.admin_kelola_lowongan_view, name='admin_kelola_lowongan'),

    
]
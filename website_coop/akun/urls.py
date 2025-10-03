from django.urls import path
from . import views

app_name = 'akun' 

urlpatterns = [
    path('', views.registrasi_view, name='registrasi'),
    path('login/', views.login_view, name='login'),  # ← Tambahkan ini
]
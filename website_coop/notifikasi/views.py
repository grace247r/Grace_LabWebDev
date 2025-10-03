# notifikasi/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notifikasi
from mahasiswa.models import Mahasiswa
from django.utils import timezone
from datetime import timedelta

@login_required
def notifikasi_view(request):
    # Ambil notifikasi untuk user yang login
    notifikasi_list = Notifikasi.objects.filter(user=request.user)
    
    # Jika belum ada notifikasi dan user adalah perusahaan, buat beberapa notifikasi dummy
    if not notifikasi_list.exists() and request.user.is_staff:
        # Contoh notifikasi untuk perusahaan
        notifications = [
            {
                'pesan': 'Ada 2 mahasiswa baru yang melamar untuk posisi Software Engineer Intern.',
                'waktu': timezone.now() - timedelta(hours=2)
            },
            {
                'pesan': 'Waktunya memberikan evaluasi untuk mahasiswa magang: John Doe',
                'waktu': timezone.now() - timedelta(days=1)
            },
            {
                'pesan': 'Laporan bulanan mahasiswa magang menunggu verifikasi Anda.',
                'waktu': timezone.now() - timedelta(days=2)
            }
        ]
        
        for notif in notifications:
            Notifikasi.objects.create(
                user=request.user,
                pesan=notif['pesan'],
                waktu_kirim=notif['waktu'],
                sudah_dibaca=False
            )
        
        # Ambil ulang notifikasi setelah membuat dummy data
        notifikasi_list = Notifikasi.objects.filter(user=request.user)

    context = {
        'notifikasi_list': notifikasi_list
    }
    
    return render(request, 'notifikasi/daftar_notifikasi.html', context)
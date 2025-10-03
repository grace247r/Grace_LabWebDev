from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lowongan, PerusahaanProfile
from .forms import LowonganForm
from magang.models import Magang

@login_required
def perusahaan_dashboard_view(request):
    # Hanya user staff (perusahaan) yang bisa akses
    if not request.user.is_staff or hasattr(request.user, 'mahasiswa'):
        return redirect('home')

    # Ambil atau buat profil perusahaan yang terhubung dengan user ini
    profile, created = PerusahaanProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = LowonganForm(request.POST)
        if form.is_valid():
            new_lowongan = form.save(commit=False)
            new_lowongan.perusahaan = profile # Tautkan ke profil perusahaan
            new_lowongan.save()
            messages.success(request, 'Lowongan baru berhasil diposting!')
            return redirect('perusahaan:dashboard')
    else:
        form = LowonganForm()

    # Ambil semua lowongan yang diposting oleh perusahaan ini
    lowongan_list = Lowongan.objects.filter(perusahaan=profile).order_by('-tanggal_posting')

    context = {
        'form': form,
        'lowongan_list': lowongan_list,
    }
    return render(request, 'perusahaan/dashboard.html', context)

@login_required
def perusahaan_dashboard_view(request):
    if not request.user.is_staff or hasattr(request.user, 'mahasiswa'):
        return redirect('home')

    profile, created = PerusahaanProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = LowonganForm(request.POST)
        if form.is_valid():
            new_lowongan = form.save(commit=False)
            new_lowongan.perusahaan = profile
            new_lowongan.save()
            messages.success(request, 'Lowongan baru berhasil diposting!')
            return redirect('perusahaan:dashboard')
    else:
        form = LowonganForm()

    lowongan_list = Lowongan.objects.filter(perusahaan=profile).order_by('-tanggal_posting')
        
    context = {
        'form': form,
        'lowongan_list': lowongan_list,
    }
    return render(request, 'perusahaan/dashboard.html', context)

@login_required
def daftar_evaluasi_view(request):
    if not request.user.is_staff:
        return redirect('home')

    # Ambil daftar mahasiswa yang magang di bawah supervisor ini
    # Kita asumsikan email supervisor unik dan sama dengan email user perusahaan
    mahasiswa_magang_list = Magang.objects.filter(email_supervisor=request.user.email)

    context = {
        'mahasiswa_magang_list': mahasiswa_magang_list
    }
    return render(request, 'perusahaan/daftar_evaluasi.html', context)
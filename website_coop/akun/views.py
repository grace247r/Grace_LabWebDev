from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegistrationForm, MahasiswaProfileForm
from .forms import LoginForm


def home(request):
    return render(request, 'home.html')

def registrasi_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = MahasiswaProfileForm(request.POST, request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Buat objek user baru tapi jangan simpan dulu
            new_user = user_form.save(commit=False)
            # Set password yang dipilih
            new_user.set_password(user_form.cleaned_data['password'])
            # Simpan objek User
            new_user.save()
            
            # Buat profil mahasiswa
            profile = profile_form.save(commit=False)
            # Hubungkan dengan objek User
            profile.user = new_user
            # Simpan objek Mahasiswa
            profile.save()
            
            messages.success(request, 'Registrasi berhasil! Silakan login.')
            return redirect('akun:login')  # ← Ganti dengan ini
    else:
        user_form = UserRegistrationForm()
        profile_form = MahasiswaProfileForm()
        
    return render(request, 'akun/daftar.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# Di dalam file akun/views.py

# Di dalam file akun/views.py

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            
            if user is not None:
                login(request, user)
                
                # ===== LOGIKA PENGALIHAN YANG DIPERBAIKI =====
                # 1. Cek Superuser (Admin) terlebih dahulu
                if user.is_superuser:
                    return redirect('magang:admin_dashboard')
                
                # 2. Jika bukan superuser, baru cek apakah dia Staff (Supervisor/Perusahaan)
                elif user.is_staff:
                    return redirect('perusahaan:dashboard')

                # 3. Jika bukan keduanya, maka dia adalah Mahasiswa
                else:
                    return redirect('mahasiswa:dashboard')
                # ============================================
                    
            else:
                messages.error(request, 'Username atau password salah!')
                # Tetap di halaman login jika salah
                return render(request, 'akun/login.html', {'form': form})
    else:
        form = LoginForm()
    
    return render(request, 'akun/login.html', {'form': form})
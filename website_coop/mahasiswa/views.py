from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from magang.models import Magang, Lowongan
from mahasiswa.models import Mahasiswa 
from .models import Mahasiswa, LaporanPencarianMagang # Tambahkan LaporanPencarianMagang
from django.contrib import messages 
from akun.forms import UserEditForm, MahasiswaProfileEditForm 
from .forms import BerkasForm, LaporanPencarianMagangForm # Tambahkan form baru

# IMPORTS UNTUK CLASS BASED VIEW BARU
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy 
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required # -- Ini memastikan hanya user yang sudah login bisa mengakses
def dashboard_view(request):
    # Mengambil profil mahasiswa yang sesuai dengan user yang sedang login
    try:
        profile = Mahasiswa.objects.get(user=request.user)
    except Mahasiswa.DoesNotExist:
        profile = None
        
    context = {
        'profile': profile
    }
    return render(request, 'mahasiswa/dashboard.html', context)

@login_required
def profil_view(request):
    profile = Mahasiswa.objects.get(user=request.user)

    if request.method == 'POST':
        # Jika form disubmit, isi form dengan data POST dan data user yang ada
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = MahasiswaProfileEditForm(instance=profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profil Anda berhasil diperbarui!')
            return redirect('mahasiswa:profil')
        else:
            messages.error(request, 'Terjadi kesalahan saat memperbarui profil.')
    else:
        # Jika hanya menampilkan halaman, isi form dengan data user yang ada
        user_form = UserEditForm(instance=request.user)
        profile_form = MahasiswaProfileEditForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'mahasiswa/profil.html', context)

@login_required
def sertifikat_view(request):
    try:
        # Cari data magang yang terhubung dengan profil mahasiswa yang sedang login
        magang = Magang.objects.get(mahasiswa__user=request.user)
    except Magang.DoesNotExist:
        magang = None
        
    context = {
        'magang': magang
    }
    return render(request, 'mahasiswa/sertifikat.html', context)

@login_required
def unggah_berkas_view(request):
    profile = Mahasiswa.objects.get(user=request.user)

    if request.method == 'POST':
        form = BerkasForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Berkas Anda berhasil diunggah/diperbarui!')
            return redirect('mahasiswa:unggah_berkas')
    else:
        form = BerkasForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }
    return render(request, 'mahasiswa/unggah_berkas.html', context)

class LaporMingguanView(LoginRequiredMixin, CreateView):
    model = LaporanPencarianMagang
    form_class = LaporanPencarianMagangForm
    template_name = 'mahasiswa/form_lapor_mingguan.html'
    success_url = reverse_lazy('mahasiswa:dashboard') 

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        
        # LOGIKA KONTROL AKSES: Cek apakah Mahasiswa sudah Konfirmasi Magang
        try:
            
            # Magang.objects.get(mahasiswa__user=user) atau Magang.objects.get(mahasiswa=user)
            # Karena Magang di magang/models.py menggunakan User langsung:
            Magang.objects.get(mahasiswa__user=user)
            
            # Jika objek Magang ditemukan, mahasiswa sudah magang, redirect ke dashboard
            messages.info(request, "Anda sudah mengonfirmasi tempat magang. Fitur Laporan Pencarian Magang tidak diperlukan lagi.")
            return redirect(self.success_url) 
            
        except Magang.DoesNotExist:
            # Objek Magang TIDAK ditemukan, mahasiswa BELUM magang, lanjutkan ke form
            return super().dispatch(request, *args, **kwargs)
        
        except Exception as e:
            # Tangani error lain, misal model Magang tidak ditemukan
            messages.error(request, "Terjadi kesalahan saat memeriksa status magang Anda.")
            return redirect(self.success_url)

    def form_valid(self, form):
        # Otomatis mengisi kolom 'mahasiswa'
        form.instance.mahasiswa = self.request.user
        messages.success(self.request, "Laporan mingguan berhasil disimpan!")
        return super().form_valid(form)

# magang/views.py (Pastikan Mahasiswa diimpor dari mahasiswa.models)
from mahasiswa.models import Mahasiswa 
# ... (imports lainnya)

@login_required
def user_redirect_view(request):
    """
    Mengalihkan pengguna ke dashboard yang sesuai berdasarkan hierarki peran:
    1. Admin/Staf (Prioritas Tertinggi)
    2. Mahasiswa (Memiliki profile Mahasiswa)
    3. Perusahaan/Supervisor (Sisanya)
    """
    user = request.user
    
    # 1. PRIORITAS TERTINGGI: Admin/Staf
    if user.is_superuser or user.is_staff:
        return redirect('magang:admin_dashboard')
    
    # 2. PRIORITAS KEDUA: Mahasiswa (Memiliki profile Mahasiswa)
    # Menggunakan try-except untuk memeriksa OneToOneField Mahasiswa dengan aman
    try:
        # Jika relasi Mahasiswa ditemukan, dia adalah Mahasiswa
        if hasattr(user, 'mahasiswa') and user.mahasiswa is not None:
            return redirect('mahasiswa:dashboard')
    except Mahasiswa.DoesNotExist:
        pass 
        
    # 3. PRIORITAS TERENDAH: Supervisor/Perusahaan
    # Jika lolos dari dua filter di atas (Bukan Admin DAN Bukan Mahasiswa), dia adalah Supervisor
    return redirect('perusahaan:dashboard')


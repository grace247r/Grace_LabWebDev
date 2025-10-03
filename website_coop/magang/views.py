# magang/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q 
from django.utils import timezone
from notifikasi.models import Notifikasi
from mahasiswa.models import Mahasiswa
from perusahaan.models import Lowongan 

# Import Forms dan Models
from .forms import KonfirmasiMagangForm
from .forms_laporan import LaporanMagangForm 
from .models import Magang, LaporanMagang, Lowongan 

# --- DATA DUMMY LOWONGAN (LENGKAP) ---
# Tambahkan field 'kualifikasi', 'lokasi', dan 'periode' agar sesuai dengan template detail
DUMMY_LOWONGAN = [
    {'pk': 1, 'posisi': 'UI/UX Designer Intern', 'nama_perusahaan': 'Tokopedia', 'bidang_studi': 'Desain/IT', 
     'deskripsi': 'Merancang antarmuka pengguna dan pengalaman pengguna yang menarik, berfokus pada pengalaman pengguna yang intuitif.', 
     'kualifikasi': 'Mahasiswa tingkat akhir DKV/Informatika. Menguasai Figma/Sketch. Memiliki portofolio yang relevan.', 
     'lokasi': 'Jakarta Selatan', 'periode': '6 Bulan', 'tanggal_posting': timezone.now()},
    {'pk': 2, 'posisi': 'Data Analyst Intern', 'nama_perusahaan': 'Bank Central Asia', 'bidang_studi': 'Data Science/Statistika', 
     'deskripsi': 'Menganalisis data transaksi volume besar untuk mendapatkan *insight* bisnis yang berharga dan mendukung pengambilan keputusan strategis.', 
     'kualifikasi': 'Mahasiswa S1 jurusan Statistika/Matematika. Mahir Python (Pandas) dan SQL. Memiliki pemahaman dasar visualisasi data.', 
     'lokasi': 'Jakarta Pusat', 'periode': '3 Bulan', 'tanggal_posting': timezone.now()},
    {'pk': 3, 'posisi': 'Software Engineer Intern', 'nama_perusahaan': 'Astra International', 'bidang_studi': 'IT/Teknik Informatika', 
     'deskripsi': 'Mengembangkan dan memelihara aplikasi perusahaan, serta berpartisipasi dalam *code review* dan *testing*.', 
     'kualifikasi': 'Mahasiswa tingkat akhir Teknik Informatika. Familiar dengan framework Django atau Flask. Mengerti Git.', 
     'lokasi': 'Tangerang', 'periode': '6 Bulan', 'tanggal_posting': timezone.now()},
    {'pk': 4, 'posisi': 'Marketing Specialist Intern', 'nama_perusahaan': 'Gojek', 'bidang_studi': 'Marketing/Bisnis', 
     'deskripsi': 'Membantu kampanye pemasaran digital, riset pasar, dan strategi branding.', 
     'kualifikasi': 'Mahasiswa S1 Marketing/Manajemen. Memiliki kemampuan komunikasi yang baik dan familiar dengan digital marketing.', 
     'lokasi': 'Jakarta Selatan', 'periode': '6 Bulan', 'tanggal_posting': timezone.now()},
]


# --- FUNGSI VIEW BIASA (MAHASISWA & ADMIN) ---

@login_required
def konfirmasi_magang_view(request):
    try:
        instance = Magang.objects.get(mahasiswa__user=request.user)
    except Magang.DoesNotExist:
        instance = None

    if request.method == 'POST':
        form = KonfirmasiMagangForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            konfirmasi = form.save(commit=False)
            konfirmasi.mahasiswa = request.user.mahasiswa 
            konfirmasi.save()
            messages.success(request, 'Data konfirmasi magang berhasil disimpan!')
            return redirect('magang:konfirmasi_magang')
    else:
        form = KonfirmasiMagangForm(instance=instance)

    return render(request, 'magang/konfirmasi_magang.html', {'form': form})

@login_required
def dashboard_view(request):
    try:
        magang = Magang.objects.get(mahasiswa__user=request.user)
    except Magang.DoesNotExist:
        magang = None
    
    # Lowongan logic for student dashboard (max 4)
    latest_lowongan = Lowongan.objects.filter(is_active=True).order_by('-tanggal_posting')[:4]
    
    if not latest_lowongan.exists():
        # Gunakan 4 data dummy teratas untuk tampilan
        latest_lowongan_display = DUMMY_LOWONGAN[:4]
    else:
        latest_lowongan_display = list(latest_lowongan) 

    return render(request, 'mahasiswa/dashboard.html', {'magang': magang, 'latest_lowongan': latest_lowongan_display})


@login_required
def admin_dashboard_view(request):
    # Hanya izinkan superuser/staf admin
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki akses ke halaman Administrasi COOP.")
        return redirect('mahasiswa:dashboard') 

    # Ambil Data Statistik
    total_mahasiswa = Mahasiswa.objects.all().count()
    mahasiswa_terkonfirmasi = Magang.objects.filter(status='Berjalan').count()
    mahasiswa_belum_konfirmasi = total_mahasiswa - mahasiswa_terkonfirmasi
    lowongan_aktif = Lowongan.objects.filter(is_active=True).count()

    context = {
        'total_mahasiswa': total_mahasiswa,
        'mahasiswa_terkonfirmasi': mahasiswa_terkonfirmasi,
        'mahasiswa_belum_konfirmasi': mahasiswa_belum_konfirmasi,
        'lowongan_aktif': lowongan_aktif,
    }
    return render(request, 'magang/admin_dashboard.html', context)


@login_required
def daftar_mahasiswa_admin_view(request):
    # Hanya izinkan superuser/staf admin
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "Anda tidak memiliki akses ke halaman Administrasi COOP.")
        return redirect('mahasiswa:dashboard') 

    status_filter = request.GET.get('status', 'semua')
    mahasiswa_qs = Mahasiswa.objects.all().select_related('user').prefetch_related('magang')
    
    if status_filter == 'sudah':
        mahasiswa_qs = mahasiswa_qs.filter(magang__status='Berjalan')
    elif status_filter == 'belum':
        # Exclude mahasiswa yang sudah terkonfirmasi
        mahasiswa_qs = mahasiswa_qs.exclude(magang__status='Berjalan')
        
    context = {
        'mahasiswa_list': mahasiswa_qs,
        'status_filter': status_filter,
    }
    return render(request, 'magang/daftar_mahasiswa_admin.html', context)


@login_required
def daftar_lowongan_view(request):
    query = request.GET.get('q')
    lowongan_db = Lowongan.objects.filter(is_active=True).order_by('-tanggal_posting')
    
    if query:
        lowongan_list = lowongan_db.filter(
            Q(posisi__icontains=query) |
            Q(nama_perusahaan__icontains=query) |
            Q(bidang_studi__icontains=query) |
            Q(deskripsi__icontains=query)
        ).distinct()
    else:
        lowongan_list = lowongan_db

    # Suntikkan Dummy Data jika DB kosong DAN TIDAK ada pencarian aktif
    if not query and not lowongan_list.exists():
        lowongan_list = DUMMY_LOWONGAN

    context = {
        'lowongan_list': lowongan_list,
        'query': query,
    }
    return render(request, 'magang/daftar_lowongan.html', context)


@login_required
def detail_lowongan_view(request, pk):
    lowongan = None
    
    # 1. Coba ambil dari database Lowongan
    try:
        lowongan = Lowongan.objects.get(pk=pk)
    except Lowongan.DoesNotExist:
        # 2. Jika tidak ditemukan di DB, cek apakah itu adalah data dummy
        pk_int = int(pk)
        for dummy in DUMMY_LOWONGAN:
            if dummy['pk'] == pk_int:
                lowongan = dummy
                break
    
    # 3. Jika tetap tidak ditemukan, raise 404
    if lowongan is None:
        raise Http404("Lowongan Magang tidak ditemukan.")
        
    return render(request, 'magang/detail_lowongan.html', {'lowongan': lowongan})


# --- CLASS BASED VIEWS (CBV) ---

class LaporanMagangCreateView(LoginRequiredMixin, CreateView):
    model = LaporanMagang
    form_class = LaporanMagangForm
    template_name = 'magang/laporan_magang_form.html'
    
    def get_success_url(self):
        return reverse_lazy('magang:dashboard') # Redirect ke dashboard mahasiswa

    def dispatch(self, request, jenis_laporan, *args, **kwargs):
        if jenis_laporan not in ['BULANAN', 'AKHIR']:
            raise Http404("Jenis laporan tidak valid.")
        
        try:
            magang_instance = Magang.objects.get(mahasiswa__user=request.user)
            self.magang_instance = magang_instance
            self.jenis_laporan = jenis_laporan
        except Magang.DoesNotExist:
            messages.error(request, "Anda harus mengonfirmasi tempat magang terlebih dahulu.")
            return redirect(reverse_lazy('magang:konfirmasi_magang'))

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jenis_laporan_display'] = "Bulanan (Kemajuan)" if self.jenis_laporan == 'BULANAN' else "Akhir (UAS)"
        context['is_bulanan'] = self.jenis_laporan == 'BULANAN'
        context['magang_instance'] = self.magang_instance

        if not context['is_bulanan']:
             context['form'].fields.pop('bulan_ke', None)
        else:
             if 'dokumen_laporan' in context['form'].fields:
                context['form'].fields['dokumen_laporan'].required = False
             
        return context

    def form_valid(self, form):
        laporan = form.save(commit=False)
        laporan.magang = self.magang_instance
        laporan.jenis_laporan = self.jenis_laporan

        if laporan.jenis_laporan == 'AKHIR':
            laporan.bulan_ke = None
        
        laporan.save()
        messages.success(self.request, f"Laporan {laporan.jenis_laporan} berhasil disimpan!")
        return redirect(self.get_success_url())
    
@login_required
def user_redirect_view(request):
    """
    Mengalihkan pengguna ke dashboard yang sesuai.
    """
    if request.user.is_superuser or request.user.is_staff:
        # ADMIN: Prioritas Tertinggi
        return redirect('magang:admin_dashboard')

    # Cek apakah user adalah Mahasiswa
    if hasattr(request.user, 'mahasiswa') and request.user.mahasiswa is not None:
        return redirect('mahasiswa:dashboard')

    # Cek apakah user adalah Perusahaan
    if hasattr(request.user, 'perusahaan') and request.user.perusahaan is not None:
        return redirect('perusahaan:dashboard')

    # Jika tidak termasuk ketiganya, redirect ke homepage atau tampilkan pesan error
    messages.error(request, "Akun Anda tidak dikenali dalam sistem.")
    return redirect('homepage')

@login_required
def admin_profil_view(request):
    # Hanya superuser yang bisa akses
    if not request.user.is_superuser:
        return redirect('home')

    # Data dummy untuk ditampilkan
    context = {
        'user': request.user
    }
    return render(request, 'magang/admin_profil.html', context)

@login_required
def admin_notifikasi_view(request):
    # Hanya superuser yang bisa akses
    if not request.user.is_superuser:
        return redirect('home')

    # Ambil semua notifikasi untuk ditampilkan (atau bisa difilter nanti)
    notifikasi_list = Notifikasi.objects.all()

    context = {
        'notifikasi_list': notifikasi_list
    }
    return render(request, 'magang/admin_notifikasi.html', context)

@login_required
def admin_berkas_mahasiswa_view(request):
    if not request.user.is_superuser:
        return redirect('home')

    # Ambil semua mahasiswa yang sudah konfirmasi magang
    mahasiswa_dengan_magang = Mahasiswa.objects.filter(magang__isnull=False)

    context = {
        'mahasiswa_list': mahasiswa_dengan_magang
    }
    return render(request, 'magang/admin_berkas_mahasiswa.html', context)

@login_required
def admin_pantau_evaluasi_view(request):
    if not request.user.is_superuser:
        return redirect('home')

    # Ambil semua data magang yang sedang berjalan
    magang_list = Magang.objects.filter(status='Berjalan')

    context = {
        'magang_list': magang_list
    }
    return render(request, 'magang/admin_pantau_evaluasi.html', context)

@login_required
def admin_kelola_lowongan_view(request):
    if not request.user.is_superuser:
        return redirect('home')

    lowongan_list = Lowongan.objects.all().order_by('-tanggal_posting')

    context = {
        'lowongan_list': lowongan_list
    }
    return render(request, 'magang/admin_kelola_lowongan.html', context)
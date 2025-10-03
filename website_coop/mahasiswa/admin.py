# mahasiswa/admin.py
from django.contrib import admin
from .models import Mahasiswa, LaporanPencarianMagang

# Pendaftaran Model Mahasiswa
class MahasiswaAdmin(admin.ModelAdmin):
    # Field yang ditampilkan di daftar
    list_display = ('user', 'nim', 'program_studi', 'angkatan', 'kontak_wa')
    # Field yang dapat dicari
    search_fields = ('nim', 'user__first_name', 'user__last_name', 'program_studi')
    # Filter samping
    list_filter = ('angkatan', 'program_studi', 'jenis_kelamin')

# Pendaftaran Model Laporan Pencarian Magang
class LaporanPencarianMagangAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'minggu_ke', 'tanggal_lapor')
    search_fields = ('mahasiswa__user__username',)
    list_filter = ('minggu_ke', 'tanggal_lapor')

admin.site.register(Mahasiswa, MahasiswaAdmin)
admin.site.register(LaporanPencarianMagang, LaporanPencarianMagangAdmin)
from django.contrib import admin
from .models import PerusahaanProfile, Lowongan, EvaluasiMagang

@admin.register(PerusahaanProfile)
class PerusahaanProfileAdmin(admin.ModelAdmin):
    list_display = ('nama_perusahaan', 'bidang_usaha', 'email', 'website')
    search_fields = ('nama_perusahaan', 'bidang_usaha', 'email')

@admin.register(Lowongan)
class LowonganAdmin(admin.ModelAdmin):
    list_display = ('posisi', 'perusahaan', 'tipe_magang', 'status', 'tanggal_posting', 'tanggal_deadline')
    list_filter = ('status', 'tipe_magang')
    search_fields = ('posisi', 'perusahaan__nama_perusahaan')
    ordering = ('-tanggal_posting',)

@admin.register(EvaluasiMagang)
class EvaluasiMagangAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'perusahaan', 'periode', 'tanggal_evaluasi')
    list_filter = ('periode',)
    search_fields = ('mahasiswa__user__username', 'perusahaan__nama_perusahaan')

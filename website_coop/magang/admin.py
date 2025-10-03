# magang/admin.py
from django.contrib import admin
from .models import Magang, LaporanMagang, Lowongan

# Pendaftaran Model Magang (Konfirmasi)
class MagangAdmin(admin.ModelAdmin):
    list_display = ('mahasiswa', 'nama_perusahaan', 'posisi', 'periode_magang', 'status')
    search_fields = ('mahasiswa__user__username', 'nama_perusahaan', 'posisi')
    list_filter = ('status', 'periode_magang', 'bidang_usaha')

# Pendaftaran Model Laporan Magang (Bulanan/Akhir)
class LaporanMagangAdmin(admin.ModelAdmin):
    list_display = ('magang', 'jenis_laporan', 'bulan_ke', 'tanggal_submit')
    search_fields = ('magang__nama_perusahaan', 'magang__mahasiswa__user__username')
    list_filter = ('jenis_laporan', 'bulan_ke')

# Pendaftaran Model Lowongan
class LowonganAdmin(admin.ModelAdmin):
    list_display = ('posisi', 'nama_perusahaan', 'bidang_studi', 'tanggal_posting', 'is_active')
    search_fields = ('posisi', 'nama_perusahaan', 'bidang_studi')
    list_filter = ('is_active', 'bidang_studi')
    actions = ['make_inactive']

    @admin.action(description='Tandai lowongan sebagai tidak aktif')
    def make_inactive(modeladmin, request, queryset):
        queryset.update(is_active=False)

admin.site.register(Magang, MagangAdmin)
admin.site.register(LaporanMagang, LaporanMagangAdmin)
admin.site.register(Lowongan, LowonganAdmin)
# magang/models.py

from django.db import models
from django.contrib.auth.models import User # <-- HARUS DITAMBAHKAN
# Hapus: from mahasiswa.models import Mahasiswa 
# Menggunakan string reference untuk menghindari circular import

class Magang(models.Model):
    STATUS_CHOICES = [
        ('Berjalan', 'Berjalan'),
        ('Selesai', 'Selesai'),
    ]
    
    PERIODE_CHOICES = [
        ('2025/2026 Ganjil', 'Semester Ganjil 2025/2026'),
        ('2025/2026 Genap', 'Semester Genap 2025/2026'),
        ('2026/2027 Ganjil', 'Semester Ganjil 2026/2027'),
        ('2026/2027 Genap', 'Semester Genap 2026/2027'),
    ]
    
    # KOREKSI SINTAKS: Menggunakan string reference
    mahasiswa = models.OneToOneField('mahasiswa.Mahasiswa', on_delete=models.CASCADE)
    
    # Field Konfirmasi Magang
    periode_magang = models.CharField(max_length=100, choices=PERIODE_CHOICES, blank=True, null=True)
    lowongan = models.ForeignKey('perusahaan.Lowongan', on_delete=models.SET_NULL, null=True, blank=True)
    posisi = models.CharField(max_length=200, blank=True, null=True)
    nama_perusahaan = models.CharField(max_length=200, blank=True, null=True)
    alamat_perusahaan = models.TextField(blank=True, null=True)
    bidang_usaha = models.CharField(max_length=200, blank=True, null=True)
    nama_supervisor = models.CharField(max_length=100, blank=True, null=True)
    email_supervisor = models.EmailField(blank=True, null=True)
    kontak_wa_supervisor = models.CharField(max_length=20, blank=True)
    surat_penerimaan = models.FileField(upload_to='surat_penerimaan/', blank=True, null=True)
    
    # Field Status Program
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Berjalan')
    nilai_akhir = models.CharField(max_length=5, blank=True, null=True)
    
    def __str__(self):
        return f"{self.mahasiswa.user.username} di {self.nama_perusahaan or 'Belum dikonfirmasi'}"


# Model Laporan Magang (Bulanan/Akhir)
class LaporanMagang(models.Model):
    JENIS_LAPORAN_CHOICES = [
        ('BULANAN', 'Laporan Bulanan/Kemajuan (UTS)'),
        ('AKHIR', 'Laporan Akhir (UAS)'),
    ]
    # ... (Field LaporanMagang lainnya)
    magang = models.ForeignKey(Magang, on_delete=models.CASCADE, related_name='laporan_magang')
    jenis_laporan = models.CharField(max_length=10, choices=JENIS_LAPORAN_CHOICES)
    bulan_ke = models.PositiveSmallIntegerField(null=True, blank=True, help_text='Bulan ke berapa laporan ini dibuat.')
    tanggal_submit = models.DateTimeField(auto_now_add=True)
    profil_perusahaan = models.TextField(verbose_name="Profil Singkat Perusahaan")
    jobdesk = models.TextField(verbose_name="Jobdesk / Tugas yang Dikerjakan")
    suasana_kerja = models.TextField(verbose_name="Suasana Lingkungan Pekerjaan")
    pengetahuan_bermanfaat = models.TextField(verbose_name="Pengetahuan dari Kampus yang Bermanfaat", help_text="Apa yang didapatkan dari perkuliahan yang berguna untuk pekerjaan.")
    pengetahuan_kurang = models.TextField(verbose_name="Pengetahuan yang Perlu Ditambahkan", help_text="Apa yang berguna pada perusahaan tapi belum didapatkan dalam pembelajaran.")
    dokumen_laporan = models.FileField(upload_to='dokumen_laporan/', null=True, blank=True, verbose_name="Dokumen Laporan Akhir", help_text="Upload file PDF laporan akhir magang (hanya untuk laporan UAS)")

    class Meta:
        verbose_name = "Laporan Magang"
        verbose_name_plural = "Laporan Magang"
        unique_together = [('magang', 'jenis_laporan', 'bulan_ke')] 
        ordering = ['-tanggal_submit']

    def __str__(self):
        return f"{self.jenis_laporan} - Bulan {self.bulan_ke or 'Akhir'} oleh {self.magang.mahasiswa.user.username}"


# MODEL BARU: Lowongan (Fitur 2)
class Lowongan(models.Model):
    user_perusahaan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lowongan_diposting')
    
    nama_perusahaan = models.CharField(max_length=200)
    posisi = models.CharField(max_length=200)
    bidang_studi = models.CharField(max_length=100, help_text="Contoh: IT, Desain, Akuntansi")
    deskripsi = models.TextField()
    kualifikasi = models.TextField()
    tanggal_posting = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.posisi} di {self.nama_perusahaan}"
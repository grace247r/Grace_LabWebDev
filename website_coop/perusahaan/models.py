from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PerusahaanProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama_perusahaan = models.CharField(max_length=200, blank=True)
    bidang_usaha = models.CharField(max_length=100, blank=True)
    alamat = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telepon = models.CharField(max_length=20, blank=True)
    deskripsi = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='foto_profil/', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Lowongan(models.Model):
    TIPE_MAGANG_CHOICES = [
        ('WFO', 'Work From Office'),
        ('WFH', 'Work From Home'),
        ('HYBRID', 'Hybrid'),
    ]
    STATUS_CHOICES = [
        ('OPEN', 'Dibuka'),
        ('CLOSED', 'Ditutup'),
    ]
    
    perusahaan = models.ForeignKey(PerusahaanProfile, on_delete=models.CASCADE)
    posisi = models.CharField(max_length=200)
    deskripsi = models.TextField()
    kualifikasi = models.TextField()
    lokasi = models.CharField(max_length=200)
    tipe_magang = models.CharField(max_length=6, choices=TIPE_MAGANG_CHOICES, default='WFO')
    durasi = models.CharField(max_length=50)  # Contoh: "3 bulan", "6 bulan"
    status = models.CharField(max_length=6, choices=STATUS_CHOICES, default='OPEN')
    tanggal_posting = models.DateTimeField(default=timezone.now)
    tanggal_deadline = models.DateField()

    def __str__(self):
        return f"{self.posisi} di {self.perusahaan.nama_perusahaan}"


class EvaluasiMagang(models.Model):
    PERIODE_CHOICES = [
        ('UTS', 'Evaluasi Tengah Semester'),
        ('UAS', 'Evaluasi Akhir Semester'),
    ]
    
    # Menggunakan referensi string untuk menghindari circular import
    mahasiswa = models.ForeignKey('mahasiswa.Mahasiswa', on_delete=models.CASCADE)
    perusahaan = models.ForeignKey(PerusahaanProfile, on_delete=models.CASCADE)
    periode = models.CharField(max_length=3, choices=PERIODE_CHOICES)
    tanggal_evaluasi = models.DateField(default=timezone.now)
    
    # Kriteria Evaluasi (skala 1-5)
    kehadiran = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    kedisiplinan = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    inisiatif = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    kerjasama = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    kemampuan_teknis = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    
    # Feedback kualitatif
    kelebihan = models.TextField()
    kekurangan = models.TextField()
    saran = models.TextField()
    
    def __str__(self):
        return f"Evaluasi {self.periode} - {self.mahasiswa.user.get_full_name()}"
    
    def get_average_score(self):
        """Menghitung rata-rata nilai dari semua kriteria evaluasi"""
        scores = [
            self.kehadiran,
            self.kedisiplinan,
            self.inisiatif,
            self.kerjasama,
            self.kemampuan_teknis
        ]
        return round(sum(scores) / len(scores), 1)

    class Meta:
        unique_together = ['mahasiswa', 'perusahaan', 'periode']
        ordering = ['-tanggal_evaluasi']
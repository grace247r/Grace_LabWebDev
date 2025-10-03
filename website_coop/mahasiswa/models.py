from django.db import models
from django.contrib.auth.models import User

class Mahasiswa(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto_profil = models.ImageField(upload_to='foto_profil/', null=True, blank=True, default='foto_profil/default.jpg') 
   
    nim = models.CharField(max_length=20, unique=True)
    program_studi = models.CharField(max_length=100)
    angkatan = models.IntegerField()
    jenis_kelamin = models.CharField(max_length=20)
    kontak_wa = models.CharField(max_length=20)
    email_outlook = models.EmailField(max_length=254) 
    bukti_konsultasi = models.FileField(upload_to='dokumen/konsultasi/')
    sptjm = models.FileField(upload_to='dokumen/sptjm/')
    cv = models.FileField(upload_to='dokumen/cv/', null=True, blank=True)
    portofolio = models.FileField(upload_to='dokumen/portofolio/', null=True, blank=True)

    

    def __str__(self):
        return self.user.username

class LaporanPencarianMagang(models.Model):
    mahasiswa = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='laporan_pencarian',
        verbose_name='Mahasiswa Pelapor'
    )
    
    minggu_ke = models.PositiveSmallIntegerField(
        verbose_name='Minggu Ke-',
        help_text='Nomor urut laporan mingguan Anda.'
    )
    tanggal_lapor = models.DateField(
        auto_now_add=True,
        verbose_name='Tanggal Lapor'
    )
    
    perusahaan_dihubungi = models.TextField(
        verbose_name='Perusahaan yang Dihubungi Minggu Ini',
        help_text='Sebutkan nama perusahaan, posisi yang dilamar, dan hasilnya.'
    )
    kendala = models.TextField(
        verbose_name='Kendala atau Tantangan',
        blank=True,
        null=True
    )
    rencana_minggu_depan = models.TextField(
        verbose_name='Rencana Aksi Minggu Depan'
    )

    class Meta:
        verbose_name = "Laporan Pencarian Magang"
        verbose_name_plural = "Laporan Pencarian Magang"
        ordering = ['-tanggal_lapor']

    def __str__(self):
        return f"Laporan Pencarian Minggu Ke-{self.minggu_ke} oleh {self.mahasiswa.username}"
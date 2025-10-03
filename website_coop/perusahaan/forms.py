from django import forms
from .models import PerusahaanProfile, Lowongan, EvaluasiMagang

class PerusahaanProfileForm(forms.ModelForm):
    class Meta:
        model = PerusahaanProfile
        # Gunakan 'telepon' dan 'alamat', sesuai dengan nama field di models.py
        fields = [
            'nama_perusahaan', 'bidang_usaha', 'alamat', 'email', 
            'telepon', 'deskripsi', 'website', 'logo'
        ]

class LowonganForm(forms.ModelForm):
    class Meta:
        model = Lowongan
        fields = [
            'posisi', 'deskripsi', 'kualifikasi', 'lokasi', 
            'tipe_magang', 'durasi', 'status', 'tanggal_deadline'
        ]
        widgets = {
            'tanggal_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

class EvaluasiMagangForm(forms.ModelForm):
    class Meta:
        model = EvaluasiMagang
        fields = [
            'periode', 'kehadiran', 'kedisiplinan', 'inisiatif', 
            'kerjasama', 'kemampuan_teknis', 'kelebihan', 
            'kekurangan', 'saran'
        ]
        widgets = {
            'kelebihan': forms.Textarea(attrs={'rows': 3}),
            'kekurangan': forms.Textarea(attrs={'rows': 3}),
            'saran': forms.Textarea(attrs={'rows': 3}),
        }
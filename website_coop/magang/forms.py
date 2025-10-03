# di magang/forms.py
from django import forms
from .models import Magang

class KonfirmasiMagangForm(forms.ModelForm):
    PERIODE_CHOICES = [
        ('', '-- Pilih Periode Magang --'),
        ('2025/2026 Ganjil', 'Semester Ganjil 2025/2026'),
        ('2025/2026 Genap', 'Semester Genap 2025/2026'),
        ('2026/2027 Ganjil', 'Semester Ganjil 2026/2027'),
        ('2026/2027 Genap', 'Semester Genap 2026/2027'),
    ]

    periode_magang = forms.ChoiceField(
        choices=PERIODE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    alamat_perusahaan = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3})
    )

    class Meta:
        model = Magang
        fields = [
            'periode_magang', 'posisi', 'nama_perusahaan', 'alamat_perusahaan',
            'bidang_usaha', 'nama_supervisor', 'email_supervisor',
            'kontak_wa_supervisor', 'surat_penerimaan'
        ]


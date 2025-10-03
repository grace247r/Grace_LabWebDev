# magang/forms_laporan.py

from django import forms
from .models import LaporanMagang

class LaporanMagangForm(forms.ModelForm):
    
    class Meta:
        model = LaporanMagang
        fields = [
            'bulan_ke',
            'profil_perusahaan',
            'jobdesk',
            'suasana_kerja',
            'pengetahuan_bermanfaat',
            'pengetahuan_kurang',
            'dokumen_laporan'
        ]
        
        widgets = {
            'bulan_ke': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Isi nomor bulan (misal: 1, 2, 3)'}),
            'profil_perusahaan': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Deskripsikan profil singkat perusahaan tempat magang...'}),
            'jobdesk': forms.Textarea(attrs={'rows': 6, 'class': 'form-control', 'placeholder': 'Uraikan tugas-tugas yang dikerjakan secara rinci...'}),
            'suasana_kerja': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Bagaimana suasana lingkungan pekerjaan dan budaya di sana...'}),
            'pengetahuan_bermanfaat': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Sebutkan mata kuliah atau konsep yang paling berguna...'}),
            'pengetahuan_kurang': forms.Textarea(attrs={'rows': 4, 'class': 'form-control', 'placeholder': 'Sebutkan keahlian atau pengetahuan yang Anda butuhkan tapi belum didapat dari kampus...'}),
            'dokumen_laporan': forms.FileInput(attrs={'class': 'form-control-file', 'accept': '.pdf,.doc,.docx'}),
        }
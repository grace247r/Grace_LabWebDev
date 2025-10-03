# di mahasiswa/forms.py
from django import forms
from .models import LaporanPencarianMagang, Mahasiswa

class BerkasForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ['cv', 'portofolio']

class LaporanPencarianMagangForm(forms.ModelForm):
    class Meta:
        model = LaporanPencarianMagang
        fields = [
            'minggu_ke',
            'perusahaan_dihubungi',
            'kendala',
            'rencana_minggu_depan'
        ]
        widgets = {
            'minggu_ke': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'perusahaan_dihubungi': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'kendala': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'rencana_minggu_depan': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
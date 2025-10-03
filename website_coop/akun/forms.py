from django import forms
from django.contrib.auth.models import User
from mahasiswa.models import Mahasiswa

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Konfirmasi password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords tidak cocok.')
        return cd['password2']

class MahasiswaProfileForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ('email_outlook', 'nim', 'program_studi', 'angkatan', 'jenis_kelamin', 'kontak_wa', 'bukti_konsultasi', 'sptjm')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

# Di dalam akun/forms.py
# ... (kode form lainnya sudah ada di atas)

# --- TAMBAHKAN DUA CLASS DI BAWAH INI ---

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class MahasiswaProfileEditForm(forms.ModelForm):
    class Meta:
        model = Mahasiswa
        fields = ('foto_profil', 'email_outlook', 'kontak_wa')
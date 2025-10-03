from django.db import models
from django.contrib.auth.models import User

class Notifikasi(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pesan = models.TextField()
    waktu_kirim = models.DateTimeField(auto_now_add=True)
    sudah_dibaca = models.BooleanField(default=False)

    def __str__(self):
        return f'Notifikasi untuk {self.user.username}: {self.pesan[:30]}'

    class Meta:
        ordering = ['-waktu_kirim'] # Urutkan dari yang paling baru
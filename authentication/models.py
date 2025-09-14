from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Özel kullanıcı modeli - Django'nun varsayılan User modelini genişletir
    """
    email = models.EmailField(unique=True, verbose_name="E-posta")
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefon Numarası")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Doğum Tarihi")
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True, verbose_name="Profil Resmi")
    bio = models.TextField(max_length=500, blank=True, verbose_name="Biyografi")
    is_verified = models.BooleanField(default=False, verbose_name="E-posta Doğrulandı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"
        db_table = 'custom_users'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

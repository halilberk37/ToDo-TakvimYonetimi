from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Calendar(models.Model):
    """
    Kullanıcıya özel takvim modeli
    """
    name = models.CharField(max_length=100, verbose_name="Takvim Adı")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="Renk Kodu")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendars', verbose_name="Kullanıcı")
    is_default = models.BooleanField(default=False, verbose_name="Varsayılan Takvim")
    is_public = models.BooleanField(default=False, verbose_name="Herkese Açık")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Takvim"
        verbose_name_plural = "Takvimler"
        unique_together = ['name', 'user']  # Her kullanıcı için benzersiz takvim adı

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    def save(self, *args, **kwargs):
        """
        Eğer bu takvim varsayılan olarak işaretlenirse, kullanıcının diğer takvimlerini varsayılan olmaktan çıkar
        """
        if self.is_default:
            Calendar.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)


class EventType(models.TextChoices):
    """
    Etkinlik türleri
    """
    MEETING = 'meeting', 'Toplantı'
    APPOINTMENT = 'appointment', 'Randevu'
    TASK = 'task', 'Görev'
    REMINDER = 'reminder', 'Hatırlatıcı'
    HOLIDAY = 'holiday', 'Tatil'
    PERSONAL = 'personal', 'Kişisel'
    WORK = 'work', 'İş'
    OTHER = 'other', 'Diğer'


class Event(models.Model):
    """
    Ana etkinlik modeli
    """
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='events', verbose_name="Takvim")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events', verbose_name="Kullanıcı")
    
    # Tarih ve saat bilgileri - Serializer ile uyumlu field isimleri
    start_time = models.DateTimeField(verbose_name="Başlangıç Tarihi")
    end_time = models.DateTimeField(verbose_name="Bitiş Tarihi")
    is_all_day = models.BooleanField(default=False, verbose_name="Tüm Gün")
    
    # Tekrarlama bilgileri
    is_recurring = models.BooleanField(default=False, verbose_name="Tekrarlayan")
    recurrence_pattern = models.CharField(max_length=50, blank=True, null=True, verbose_name="Tekrarlama Deseni")
    recurrence_end_date = models.DateTimeField(blank=True, null=True, verbose_name="Tekrarlama Bitiş Tarihi")
    
    # Etkinlik özellikleri
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.OTHER, verbose_name="Etkinlik Türü")
    location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Konum")
    is_important = models.BooleanField(default=False, verbose_name="Önemli")
    is_private = models.BooleanField(default=False, verbose_name="Özel")
    
    # Bildirim ayarları
    reminder_minutes = models.PositiveIntegerField(
        default=15, 
        validators=[MinValueValidator(1), MaxValueValidator(10080)],  # 1 dakika - 1 hafta
        verbose_name="Hatırlatıcı (Dakika)"
    )
    
    # Zaman damgaları
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Etkinlik"
        verbose_name_plural = "Etkinlikler"
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} - {self.start_time.strftime('%d.%m.%Y %H:%M')}"

    @property
    def duration(self):
        """
        Etkinliğin süresini hesapla
        """
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return None

    @property
    def is_past(self):
        """
        Etkinlik geçmişte mi?
        """
        return self.end_time < timezone.now()

    @property
    def is_current(self):
        """
        Etkinlik şu anda devam ediyor mu?
        """
        now = timezone.now()
        return self.start_time <= now <= self.end_time

    @property
    def is_upcoming(self):
        """
        Etkinlik gelecekte mi?
        """
        return self.start_time > timezone.now()

    def save(self, *args, **kwargs):
        """
        Etkinlik kaydedilirken tarih kontrolü yap
        """
        if self.end_time <= self.start_time:
            raise ValueError("Bitiş tarihi başlangıç tarihinden sonra olmalıdır")
        super().save(*args, **kwargs)


class EventParticipant(models.Model):
    """
    Etkinlik katılımcıları
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants', verbose_name="Etkinlik")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    is_organizer = models.BooleanField(default=False, verbose_name="Organizatör")
    response_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Beklemede'),
            ('accepted', 'Kabul Edildi'),
            ('declined', 'Reddedildi'),
            ('tentative', 'Belirsiz'),
        ],
        default='pending',
        verbose_name="Yanıt Durumu"
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Katılım Tarihi")

    class Meta:
        verbose_name = "Etkinlik Katılımcısı"
        verbose_name_plural = "Etkinlik Katılımcıları"
        unique_together = ['event', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class EventAttachment(models.Model):
    """
    Etkinlik ekleri
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attachments', verbose_name="Etkinlik")
    filename = models.CharField(max_length=255, verbose_name="Dosya Adı")
    file = models.FileField(upload_to='event_attachments/', verbose_name="Dosya")
    file_size = models.PositiveIntegerField(verbose_name="Dosya Boyutu (Byte)")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")

    class Meta:
        verbose_name = "Etkinlik Eki"
        verbose_name_plural = "Etkinlik Ekleri"

    def __str__(self):
        return f"{self.filename} - {self.event.title}"

    def save(self, *args, **kwargs):
        """
        Dosya boyutunu otomatik hesapla
        """
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class EventReminder(models.Model):
    """
    Etkinlik hatırlatıcıları
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reminders', verbose_name="Etkinlik")
    reminder_type = models.CharField(
        max_length=20,
        choices=[
            ('email', 'E-posta'),
            ('push', 'Push Bildirimi'),
            ('sms', 'SMS'),
        ],
        default='email',
        verbose_name="Hatırlatıcı Türü"
    )
    reminder_time = models.DateTimeField(verbose_name="Hatırlatma Zamanı")
    is_sent = models.BooleanField(default=False, verbose_name="Gönderildi")
    sent_at = models.DateTimeField(blank=True, null=True, verbose_name="Gönderilme Tarihi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        verbose_name = "Etkinlik Hatırlatıcısı"
        verbose_name_plural = "Etkinlik Hatırlatıcıları"

    def __str__(self):
        return f"{self.event.title} - {self.reminder_time.strftime('%d.%m.%Y %H:%M')}"

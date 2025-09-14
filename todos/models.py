from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Category(models.Model):
    """
    Todo kategorileri için model
    """
    name = models.CharField(max_length=100, verbose_name="Kategori Adı")
    color = models.CharField(max_length=7, default="#007bff", verbose_name="Renk Kodu")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories', verbose_name="Kullanıcı")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        unique_together = ['name', 'user']  # Her kullanıcı için benzersiz kategori adı

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Priority(models.TextChoices):
    """
    Öncelik seviyeleri
    """
    LOW = 'low', 'Düşük'
    MEDIUM = 'medium', 'Orta'
    HIGH = 'high', 'Yüksek'
    URGENT = 'urgent', 'Acil'


class Todo(models.Model):
    """
    Ana Todo modeli
    """
    title = models.CharField(max_length=200, verbose_name="Başlık")
    description = models.TextField(blank=True, null=True, verbose_name="Açıklama")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', verbose_name="Kullanıcı")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='todos', verbose_name="Kategori")
    
    # Durum ve öncelik
    is_completed = models.BooleanField(default=False, verbose_name="Tamamlandı")
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM, verbose_name="Öncelik")
    
    # Tarihler
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Bitiş Tarihi")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Tamamlanma Tarihi")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")
    
    # Ek özellikler
    is_important = models.BooleanField(default=False, verbose_name="Önemli")
    is_starred = models.BooleanField(default=False, verbose_name="Yıldızlı")
    estimated_duration = models.DurationField(null=True, blank=True, verbose_name="Tahmini Süre")
    actual_duration = models.DurationField(null=True, blank=True, verbose_name="Gerçek Süre")

    class Meta:
        verbose_name = "Todo"
        verbose_name_plural = "Todos"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def save(self, *args, **kwargs):
        """
        Todo tamamlandığında completed_at tarihini otomatik ayarla
        """
        if self.is_completed and not self.completed_at:
            self.completed_at = timezone.now()
        elif not self.is_completed and self.completed_at:
            self.completed_at = None
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """
        Todo'nun süresi geçmiş mi kontrol et
        """
        if self.due_date and not self.is_completed:
            return timezone.now() > self.due_date
        return False

    @property
    def days_until_due(self):
        """
        Bitiş tarihine kaç gün kaldığını hesapla
        """
        if self.due_date and not self.is_completed:
            delta = self.due_date - timezone.now()
            return delta.days
        return None


class TodoAttachment(models.Model):
    """
    Todo'ya eklenen dosyalar için model
    """
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='attachments', verbose_name="Todo")
    file = models.FileField(upload_to='todo_attachments/', verbose_name="Dosya")
    filename = models.CharField(max_length=255, verbose_name="Dosya Adı")
    file_size = models.PositiveIntegerField(verbose_name="Dosya Boyutu")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Yüklenme Tarihi")

    class Meta:
        verbose_name = "Todo Eki"
        verbose_name_plural = "Todo Ekleri"

    def __str__(self):
        return f"{self.filename} - {self.todo.title}"


class TodoComment(models.Model):
    """
    Todo'ya yapılan yorumlar için model
    """
    todo = models.ForeignKey(Todo, on_delete=models.CASCADE, related_name='comments', verbose_name="Todo")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Kullanıcı")
    comment = models.TextField(verbose_name="Yorum")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Todo Yorumu"
        verbose_name_plural = "Todo Yorumları"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.todo.title}"

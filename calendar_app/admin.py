from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Calendar, Event, EventParticipant, EventAttachment, EventReminder


@admin.register(Calendar)
class CalendarAdmin(admin.ModelAdmin):
    """
    Takvim admin paneli
    """
    list_display = ('name', 'user', 'color_display', 'is_default', 'is_public', 'created_at')
    list_filter = ('is_default', 'is_public', 'user', 'created_at')
    search_fields = ('name', 'description', 'user__username', 'user__email')
    ordering = ('-created_at',)
    
    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Renk'


class EventParticipantInline(admin.TabularInline):
    """
    Etkinlik katılımcıları için inline admin
    """
    model = EventParticipant
    extra = 0


class EventAttachmentInline(admin.TabularInline):
    """
    Etkinlik ekleri için inline admin
    """
    model = EventAttachment
    extra = 0


class EventReminderInline(admin.TabularInline):
    """
    Etkinlik hatırlatıcıları için inline admin
    """
    model = EventReminder
    extra = 0


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """
    Etkinlik admin paneli
    """
    list_display = ('title', 'calendar', 'user', 'start_time', 'end_time', 'event_type', 'is_important')
    list_filter = ('event_type', 'is_important', 'is_private', 'is_all_day', 'is_recurring', 'calendar', 'user', 'start_time')
    search_fields = ('title', 'description', 'location', 'user__username', 'user__email')
    ordering = ('start_time',)
    inlines = [EventParticipantInline, EventAttachmentInline, EventReminderInline]
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'description', 'calendar', 'user', 'event_type')
        }),
        ('Tarih ve Saat', {
            'fields': ('start_time', 'end_time', 'is_all_day')
        }),
        ('Tekrarlama', {
            'fields': ('is_recurring', 'recurrence_pattern', 'recurrence_end_date'),
            'classes': ('collapse',)
        }),
        ('Konum ve Özellikler', {
            'fields': ('location', 'is_important', 'is_private')
        }),
        ('Bildirimler', {
            'fields': ('reminder_minutes',),
            'classes': ('collapse',)
        }),
        ('Meta Bilgiler', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def get_queryset(self, request):
        """
        Admin kullanıcısına sadece kendi etkinliklerini göster
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    """
    Etkinlik katılımcıları admin paneli
    """
    list_display = ('event', 'user', 'is_organizer', 'response_status', 'joined_at')
    list_filter = ('is_organizer', 'response_status', 'joined_at')
    search_fields = ('event__title', 'user__username', 'user__email')
    ordering = ('-joined_at',)


@admin.register(EventAttachment)
class EventAttachmentAdmin(admin.ModelAdmin):
    """
    Etkinlik ekleri admin paneli
    """
    list_display = ('filename', 'event', 'file_size', 'uploaded_at')
    list_filter = ('uploaded_at', 'event__user')
    search_fields = ('filename', 'event__title')
    ordering = ('-uploaded_at',)


@admin.register(EventReminder)
class EventReminderAdmin(admin.ModelAdmin):
    """
    Etkinlik hatırlatıcıları admin paneli
    """
    list_display = ('event', 'reminder_time', 'is_sent', 'sent_at')
    list_filter = ('is_sent', 'reminder_time', 'event__user')
    search_fields = ('event__title',)
    ordering = ('reminder_time',)

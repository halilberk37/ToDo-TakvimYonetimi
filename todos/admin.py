from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Todo, TodoAttachment, TodoComment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Kategori admin paneli
    """
    list_display = ('name', 'user', 'color_display', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username', 'user__email')
    ordering = ('-created_at',)
    
    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 3px;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Renk'


class TodoAttachmentInline(admin.TabularInline):
    """
    Todo ekleri için inline admin
    """
    model = TodoAttachment
    extra = 0


class TodoCommentInline(admin.TabularInline):
    """
    Todo yorumları için inline admin
    """
    model = TodoComment
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    """
    Todo admin paneli
    """
    list_display = ('title', 'user', 'category', 'priority', 'is_completed', 'due_date', 'created_at')
    list_filter = ('is_completed', 'priority', 'is_important', 'is_starred', 'category', 'user', 'created_at')
    search_fields = ('title', 'description', 'user__username', 'user__email')
    ordering = ('-created_at',)
    inlines = [TodoAttachmentInline, TodoCommentInline]
    
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('title', 'description', 'user', 'category')
        }),
        ('Durum ve Öncelik', {
            'fields': ('is_completed', 'priority', 'is_important', 'is_starred')
        }),
        ('Tarihler', {
            'fields': ('due_date', 'completed_at', 'estimated_duration', 'actual_duration')
        }),
        ('Meta Bilgiler', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'completed_at')
    
    def get_queryset(self, request):
        """
        Admin kullanıcısına sadece kendi todo'larını göster
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)


@admin.register(TodoAttachment)
class TodoAttachmentAdmin(admin.ModelAdmin):
    """
    Todo ekleri admin paneli
    """
    list_display = ('filename', 'todo', 'file_size', 'uploaded_at')
    list_filter = ('uploaded_at', 'todo__user')
    search_fields = ('filename', 'todo__title')
    ordering = ('-uploaded_at',)


@admin.register(TodoComment)
class TodoCommentAdmin(admin.ModelAdmin):
    """
    Todo yorumları admin paneli
    """
    list_display = ('todo', 'user', 'comment_preview', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('comment', 'todo__title', 'user__username')
    ordering = ('-created_at',)
    
    def comment_preview(self, obj):
        return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
    comment_preview.short_description = 'Yorum Önizleme'

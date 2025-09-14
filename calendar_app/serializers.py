from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Calendar, Event, EventParticipant, EventAttachment, EventReminder

User = get_user_model()


class CalendarSerializer(serializers.ModelSerializer):
    """
    Takvim serializer'ı
    """
    event_count = serializers.SerializerMethodField()

    class Meta:
        model = Calendar
        fields = (
            'id', 'name', 'description', 'color', 'is_default', 'is_public',
            'event_count', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_event_count(self, obj):
        """
        Takvime ait etkinlik sayısını getir
        """
        return obj.events.count()


class EventCreateSerializer(serializers.ModelSerializer):
    """
    Etkinlik oluşturma için basit serializer
    """
    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'start_time', 'end_time',
            'location', 'is_all_day', 'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        """
        Etkinlik oluştururken kullanıcıyı ve varsayılan takvimi ata
        """
        validated_data['user'] = self.context['request'].user
        
        # Varsayılan takvimi bul veya oluştur
        calendar, created = Calendar.objects.get_or_create(
            user=self.context['request'].user,
            is_default=True,
            defaults={
                'name': 'Kişisel Takvim',
                'description': 'Varsayılan kişisel takvim',
                'color': '#007bff'
            }
        )
        validated_data['calendar'] = calendar
        
        return super().create(validated_data)


class EventParticipantSerializer(serializers.ModelSerializer):
    """
    Etkinlik katılımcısı serializer'ı
    """
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = EventParticipant
        fields = (
            'id', 'user', 'user_name', 'user_email', 'is_organizer',
            'response_status', 'joined_at'
        )
        read_only_fields = ('id', 'joined_at')


class EventAttachmentSerializer(serializers.ModelSerializer):
    """
    Etkinlik eki serializer'ı
    """
    class Meta:
        model = EventAttachment
        fields = ('id', 'filename', 'file', 'file_size', 'uploaded_at')
        read_only_fields = ('id', 'filename', 'file_size', 'uploaded_at')


class EventReminderSerializer(serializers.ModelSerializer):
    """
    Etkinlik hatırlatıcısı serializer'ı
    """
    class Meta:
        model = EventReminder
        fields = (
            'id', 'reminder_type', 'reminder_time', 'is_sent',
            'sent_at', 'created_at'
        )
        read_only_fields = ('id', 'is_sent', 'sent_at', 'created_at')


class EventListSerializer(serializers.ModelSerializer):
    """
    Etkinlik listesi için basit serializer
    """
    calendar_name = serializers.CharField(source='calendar.name', read_only=True)
    calendar_color = serializers.CharField(source='calendar.color', read_only=True)
    duration = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    is_current = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'calendar', 'calendar_name', 'calendar_color',
            'start_time', 'end_time', 'location', 'is_all_day',
            'duration', 'is_past', 'is_current', 'is_upcoming',
            'created_at', 'updated_at'
        )


class EventDetailSerializer(serializers.ModelSerializer):
    """
    Etkinlik detayı için kapsamlı serializer
    """
    calendar = CalendarSerializer(read_only=True)
    calendar_id = serializers.IntegerField(write_only=True, required=False)
    participants = EventParticipantSerializer(many=True, read_only=True)
    attachments = EventAttachmentSerializer(many=True, read_only=True)
    reminders = EventReminderSerializer(many=True, read_only=True)
    duration = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    is_current = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = (
            'id', 'title', 'description', 'calendar', 'calendar_id',
            'start_time', 'end_time', 'location', 'is_all_day',
            'duration', 'is_past', 'is_current', 'is_upcoming',
            'participants', 'attachments', 'reminders',
            'created_at', 'updated_at'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

    def create(self, validated_data):
        """
        Etkinlik oluştururken kullanıcıyı ve varsayılan takvimi ata
        """
        validated_data['user'] = self.context['request'].user
        
        # Varsayılan takvimi bul veya oluştur
        calendar, created = Calendar.objects.get_or_create(
            user=self.context['request'].user,
            is_default=True,
            defaults={
                'name': 'Kişisel Takvim',
                'description': 'Varsayılan kişisel takvim',
                'color': '#007bff'
            }
        )
        validated_data['calendar'] = calendar
        
        return super().create(validated_data)


class EventParticipantCreateSerializer(serializers.ModelSerializer):
    """
    Etkinlik katılımcısı oluşturma serializer'ı
    """
    class Meta:
        model = EventParticipant
        fields = ('id', 'user', 'is_organizer', 'response_status')
        read_only_fields = ('id',)

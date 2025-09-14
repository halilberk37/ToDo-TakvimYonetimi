from django.shortcuts import render
from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta, datetime
from .models import Calendar, Event, EventParticipant
from .serializers import (
    CalendarSerializer, EventListSerializer, EventDetailSerializer,
    EventCreateSerializer, EventParticipantCreateSerializer
)
from .permissions import IsOwnerOrReadOnly, IsOwner, IsEventOwnerOrParticipant


class CalendarListCreateView(generics.ListCreateAPIView):
    """
    Takvim listesi ve oluşturma
    """
    serializer_class = CalendarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        return Calendar.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CalendarDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Takvim detayı, güncelleme ve silme
    """
    serializer_class = CalendarSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Calendar.objects.filter(user=self.request.user)


class EventListCreateView(generics.ListCreateAPIView):
    """
    Etkinlik listesi ve oluşturma
    """
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['calendar', 'is_all_day']
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['title', 'start_time', 'created_at']
    ordering = ['-start_time']

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return EventCreateSerializer
        return EventListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Etkinlik detayı, güncelleme ve silme
    """
    serializer_class = EventDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Event.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_event_participant(request, pk):
    """
    Etkinliğe katılımcı ekle
    """
    try:
        event = Event.objects.get(pk=pk, user=request.user)
        serializer = EventParticipantCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Event.DoesNotExist:
        return Response(
            {'error': 'Etkinlik bulunamadı'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def today_events(request):
    """
    Bugünkü etkinlikler
    """
    today = timezone.now().date()
    events = Event.objects.filter(
        user=request.user,
        start_time__date=today
    ).order_by('start_time')
    
    serializer = EventListSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def upcoming_events(request):
    """
    Yaklaşan etkinlikler
    """
    now = timezone.now()
    upcoming_date = now + timedelta(days=7)
    
    events = Event.objects.filter(
        user=request.user,
        start_time__range=[now, upcoming_date]
    ).order_by('start_time')
    
    serializer = EventListSerializer(events, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def calendar_statistics(request):
    """
    Takvim istatistikleri
    """
    user_events = Event.objects.filter(user=request.user)
    today = timezone.now().date()
    
    stats = {
        'total_events': user_events.count(),
        'today_events': user_events.filter(start_time__date=today).count(),
        'upcoming_events': user_events.filter(
            start_time__date__gt=today
        ).count(),
        'past_events': user_events.filter(
            start_time__date__lt=today
        ).count(),
    }
    
    return Response(stats)

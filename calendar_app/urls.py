from django.urls import path
from .views import (
    CalendarListCreateView, CalendarDetailView,
    EventListCreateView, EventDetailView,
    today_events, upcoming_events,
    add_event_participant, calendar_statistics
)

app_name = 'calendar_app'

urlpatterns = [
    # Takvim endpoints
    path('calendars/', CalendarListCreateView.as_view(), name='calendar-list-create'),
    path('calendars/<int:pk>/', CalendarDetailView.as_view(), name='calendar-detail'),
    
    # Etkinlik endpoints
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/<int:pk>/participants/', add_event_participant, name='event-add-participant'),
    
    # Özel endpoints
    path('events/today/', today_events, name='today-events'),
    path('events/upcoming/', upcoming_events, name='upcoming-events'),
    path('statistics/', calendar_statistics, name='calendar-statistics'),
]

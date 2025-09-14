from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Calendar, Event, EventParticipant

User = get_user_model()


class CalendarModelTest(TestCase):
    """
    Calendar model testleri
    """
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_create_calendar(self):
        """
        Takvim oluşturma testi
        """
        calendar = Calendar.objects.create(
            name='Kişisel Takvim',
            description='Kişisel etkinliklerim',
            color='#28a745',
            user=self.user,
            is_default=True
        )
        self.assertEqual(calendar.name, 'Kişisel Takvim')
        self.assertEqual(calendar.user, self.user)
        self.assertTrue(calendar.is_default)

    def test_calendar_default_unique(self):
        """
        Varsayılan takvim tekliği testi
        """
        Calendar.objects.create(
            name='Takvim 1',
            user=self.user,
            is_default=True
        )
        
        calendar2 = Calendar.objects.create(
            name='Takvim 2',
            user=self.user,
            is_default=True
        )
        
        # İkinci takvim varsayılan olarak işaretlendiğinde, ilki varsayılan olmaktan çıkmalı
        calendars = Calendar.objects.filter(user=self.user, is_default=True)
        self.assertEqual(calendars.count(), 1)
        self.assertEqual(calendars.first(), calendar2)


class EventModelTest(TestCase):
    """
    Event model testleri
    """
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.calendar = Calendar.objects.create(
            name='Test Takvim',
            user=self.user
        )

    def test_create_event(self):
        """
        Etkinlik oluşturma testi
        """
        start_time = timezone.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        event = Event.objects.create(
            title='Test Etkinliği',
            description='Test açıklama',
            calendar=self.calendar,
            user=self.user,
            start_datetime=start_time,
            end_datetime=end_time,
            event_type='meeting'
        )
        
        self.assertEqual(event.title, 'Test Etkinliği')
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.calendar, self.calendar)

    def test_event_duration_property(self):
        """
        Etkinlik süresi property testi
        """
        start_time = timezone.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        event = Event.objects.create(
            title='Test Etkinliği',
            calendar=self.calendar,
            user=self.user,
            start_datetime=start_time,
            end_datetime=end_time
        )
        
        self.assertEqual(event.duration, timedelta(hours=2))

    def test_event_is_past_property(self):
        """
        Etkinlik geçmişte mi property testi
        """
        past_start = timezone.now() - timedelta(hours=2)
        past_end = timezone.now() - timedelta(hours=1)
        
        event = Event.objects.create(
            title='Geçmiş Etkinlik',
            calendar=self.calendar,
            user=self.user,
            start_datetime=past_start,
            end_datetime=past_end
        )
        
        self.assertTrue(event.is_past)

    def test_event_is_upcoming_property(self):
        """
        Etkinlik gelecekte mi property testi
        """
        future_start = timezone.now() + timedelta(hours=1)
        future_end = timezone.now() + timedelta(hours=2)
        
        event = Event.objects.create(
            title='Gelecek Etkinlik',
            calendar=self.calendar,
            user=self.user,
            start_datetime=future_start,
            end_datetime=future_end
        )
        
        self.assertTrue(event.is_upcoming)


class CalendarAPITest(APITestCase):
    """
    Calendar API testleri
    """
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')
        
        self.calendar = Calendar.objects.create(
            name='Test Takvim',
            user=self.user
        )

    def test_create_calendar(self):
        """
        Takvim oluşturma API testi
        """
        url = reverse('calendar_app:calendar-list-create')
        data = {
            'name': 'Yeni Takvim',
            'description': 'Yeni takvim açıklaması',
            'color': '#ff0000',
            'is_default': False
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Yeni Takvim')

    def test_list_calendars(self):
        """
        Takvim listesi API testi
        """
        url = reverse('calendar_app:calendar-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Takvim')

    def test_create_event(self):
        """
        Etkinlik oluşturma API testi
        """
        url = reverse('calendar_app:event-list-create')
        start_time = timezone.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        data = {
            'title': 'API Test Etkinliği',
            'description': 'API ile oluşturulan etkinlik',
            'calendar': self.calendar.id,
            'start_datetime': start_time.isoformat(),
            'end_datetime': end_time.isoformat(),
            'event_type': 'meeting'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'API Test Etkinliği')

    def test_list_events(self):
        """
        Etkinlik listesi API testi
        """
        # Önce bir etkinlik oluştur
        start_time = timezone.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        
        Event.objects.create(
            title='Test Etkinliği',
            calendar=self.calendar,
            user=self.user,
            start_datetime=start_time,
            end_datetime=end_time
        )
        
        url = reverse('calendar_app:event-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_today_events(self):
        """
        Bugünkü etkinlikler API testi
        """
        today = timezone.now().date()
        start_time = datetime.combine(today, datetime.min.time())
        end_time = start_time + timedelta(hours=1)
        
        Event.objects.create(
            title='Bugünkü Etkinlik',
            calendar=self.calendar,
            user=self.user,
            start_datetime=start_time,
            end_datetime=end_time
        )
        
        url = reverse('calendar_app:today-events')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_upcoming_events(self):
        """
        Yaklaşan etkinlikler API testi
        """
        start_time = timezone.now() + timedelta(days=1)
        end_time = start_time + timedelta(hours=1)
        
        Event.objects.create(
            title='Yaklaşan Etkinlik',
            calendar=self.calendar,
            user=self.user,
            start_datetime=start_time,
            end_datetime=end_time
        )
        
        url = reverse('calendar_app:upcoming-events')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_event_statistics(self):
        """
        Etkinlik istatistikleri API testi
        """
        # Birkaç etkinlik oluştur
        start_time = timezone.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)
        
        Event.objects.create(
            title='Etkinlik 1',
            calendar=self.calendar,
            user=self.user,
            start_datetime=start_time,
            end_datetime=end_time,
            is_important=True
        )
        
        Event.objects.create(
            title='Etkinlik 2',
            calendar=self.calendar,
            user=self.user,
            start_datetime=start_time + timedelta(days=1),
            end_datetime=end_time + timedelta(days=1)
        )
        
        url = reverse('calendar_app:event-statistics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_events'], 2)
        self.assertEqual(response.data['important_events'], 1)

    def test_add_event_participant(self):
        """
        Etkinlik katılımcısı ekleme API testi
        """
        start_time = timezone.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=1)
        
        event = Event.objects.create(
            title='Test Etkinliği',
            calendar=self.calendar,
            user=self.user,
            start_datetime=start_time,
            end_datetime=end_time
        )
        
        url = reverse('calendar_app:event-add-participant', kwargs={'pk': event.pk})
        data = {
            'user': self.user.id,
            'is_organizer': False,
            'response_status': 'accepted'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['response_status'], 'accepted')

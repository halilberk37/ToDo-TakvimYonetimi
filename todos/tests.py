from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Todo, TodoComment

User = get_user_model()


class CategoryModelTest(TestCase):
    """
    Category model testleri
    """
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )

    def test_create_category(self):
        """
        Kategori oluşturma testi
        """
        category = Category.objects.create(
            name='İş',
            color='#007bff',
            user=self.user
        )
        self.assertEqual(category.name, 'İş')
        self.assertEqual(category.user, self.user)

    def test_category_str_representation(self):
        """
        Kategori string temsili testi
        """
        category = Category.objects.create(
            name='İş',
            color='#007bff',
            user=self.user
        )
        expected = f"{category.name} ({category.user.username})"
        self.assertEqual(str(category), expected)


class TodoModelTest(TestCase):
    """
    Todo model testleri
    """
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='İş',
            color='#007bff',
            user=self.user
        )

    def test_create_todo(self):
        """
        Todo oluşturma testi
        """
        todo = Todo.objects.create(
            title='Test Todo',
            description='Test açıklama',
            user=self.user,
            category=self.category,
            priority='high'
        )
        self.assertEqual(todo.title, 'Test Todo')
        self.assertEqual(todo.user, self.user)
        self.assertEqual(todo.category, self.category)

    def test_todo_completion(self):
        """
        Todo tamamlama testi
        """
        todo = Todo.objects.create(
            title='Test Todo',
            user=self.user,
            category=self.category
        )
        
        # Başlangıçta tamamlanmamış
        self.assertFalse(todo.is_completed)
        self.assertIsNone(todo.completed_at)
        
        # Tamamla
        todo.is_completed = True
        todo.save()
        
        self.assertTrue(todo.is_completed)
        self.assertIsNotNone(todo.completed_at)

    def test_todo_overdue_property(self):
        """
        Todo süresi geçmiş mi testi
        """
        past_date = timezone.now() - timedelta(days=1)
        todo = Todo.objects.create(
            title='Test Todo',
            user=self.user,
            category=self.category,
            due_date=past_date,
            is_completed=False
        )
        
        self.assertTrue(todo.is_overdue)

    def test_todo_days_until_due_property(self):
        """
        Todo bitiş tarihine kaç gün kaldığı testi
        """
        future_date = timezone.now() + timedelta(days=3)
        todo = Todo.objects.create(
            title='Test Todo',
            user=self.user,
            category=self.category,
            due_date=future_date,
            is_completed=False
        )
        
        self.assertEqual(todo.days_until_due, 3)


class TodoAPITest(APITestCase):
    """
    Todo API testleri
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
        
        self.category = Category.objects.create(
            name='İş',
            color='#007bff',
            user=self.user
        )

    def test_create_category(self):
        """
        Kategori oluşturma API testi
        """
        url = reverse('todos:category-list-create')
        data = {
            'name': 'Kişisel',
            'color': '#28a745'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'Kişisel')

    def test_list_categories(self):
        """
        Kategori listesi API testi
        """
        url = reverse('todos:category-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'İş')

    def test_create_todo(self):
        """
        Todo oluşturma API testi
        """
        url = reverse('todos:todo-list-create')
        data = {
            'title': 'API Test Todo',
            'description': 'API ile oluşturulan todo',
            'priority': 'medium',
            'is_important': True
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'API Test Todo')

    def test_list_todos(self):
        """
        Todo listesi API testi
        """
        # Önce bir todo oluştur
        Todo.objects.create(
            title='Test Todo',
            user=self.user,
            category=self.category
        )
        
        url = reverse('todos:todo-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_todo_detail(self):
        """
        Todo detay API testi
        """
        todo = Todo.objects.create(
            title='Test Todo',
            user=self.user,
            category=self.category
        )
        
        url = reverse('todos:todo-detail', kwargs={'pk': todo.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Todo')

    def test_toggle_todo_completion(self):
        """
        Todo tamamlama durumu değiştirme API testi
        """
        todo = Todo.objects.create(
            title='Test Todo',
            user=self.user,
            category=self.category
        )
        
        url = reverse('todos:todo-toggle', kwargs={'pk': todo.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_completed'])

    def test_todo_statistics(self):
        """
        Todo istatistikleri API testi
        """
        # Birkaç todo oluştur
        Todo.objects.create(
            title='Todo 1',
            user=self.user,
            category=self.category,
            is_completed=True
        )
        Todo.objects.create(
            title='Todo 2',
            user=self.user,
            category=self.category,
            is_completed=False,
            is_important=True
        )
        
        url = reverse('todos:todo-statistics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_todos'], 2)
        self.assertEqual(response.data['completed_todos'], 1)
        self.assertEqual(response.data['important_todos'], 1)

    def test_add_todo_comment(self):
        """
        Todo yorumu ekleme API testi
        """
        todo = Todo.objects.create(
            title='Test Todo',
            user=self.user,
            category=self.category
        )
        
        url = reverse('todos:todo-add-comment', kwargs={'pk': todo.pk})
        data = {'comment': 'Bu bir test yorumudur'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['comment'], 'Bu bir test yorumudur')

    def test_user_isolation(self):
        """
        Kullanıcı izolasyonu testi
        """
        # Başka bir kullanıcı oluştur
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='otherpass123'
        )
        
        # Başka kullanıcının todo'su
        Todo.objects.create(
            title='Other User Todo',
            user=other_user
        )
        
        # Mevcut kullanıcının todo'su
        Todo.objects.create(
            title='My Todo',
            user=self.user
        )
        
        url = reverse('todos:todo-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'My Todo')

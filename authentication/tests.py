from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

User = get_user_model()


class CustomUserModelTest(TestCase):
    """
    CustomUser model testleri
    """
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        }

    def test_create_user(self):
        """
        Kullanıcı oluşturma testi
        """
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.full_name, 'Test User')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_superuser(self):
        """
        Superuser oluşturma testi
        """
        user = User.objects.create_superuser(**self.user_data)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_user_str_representation(self):
        """
        Kullanıcı string temsili testi
        """
        user = User.objects.create_user(**self.user_data)
        expected = f"{user.first_name} {user.last_name} ({user.email})"
        self.assertEqual(str(user), expected)


class AuthenticationAPITest(APITestCase):
    """
    Authentication API testleri
    """
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123',
            'password_confirm': 'testpass123'
        }
        self.user_create_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': 'testpass123'
        }
        self.login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }

    def test_user_registration(self):
        """
        Kullanıcı kayıt testi
        """
        url = reverse('authentication:register')
        response = self.client.post(url, self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], 'test@example.com')

    def test_user_registration_invalid_data(self):
        """
        Geçersiz veri ile kayıt testi
        """
        url = reverse('authentication:register')
        invalid_data = self.user_data.copy()
        invalid_data['password_confirm'] = 'different_password'
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_login(self):
        """
        Kullanıcı giriş testi
        """
        # Önce kullanıcı oluştur
        User.objects.create_user(**self.user_create_data)
        
        url = reverse('authentication:login')
        response = self.client.post(url, self.login_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIn('user', response.data)

    def test_user_login_invalid_credentials(self):
        """
        Geçersiz kimlik bilgileri ile giriş testi
        """
        url = reverse('authentication:login')
        invalid_data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_profile_access(self):
        """
        Kullanıcı profil erişim testi
        """
        user = User.objects.create_user(**self.user_create_data)
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
        
        url = reverse('authentication:profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_user_profile_update(self):
        """
        Kullanıcı profil güncelleme testi
        """
        user = User.objects.create_user(**self.user_create_data)
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
        
        url = reverse('authentication:profile')
        update_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'bio': 'Updated bio'
        }
        
        response = self.client.put(url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['bio'], 'Updated bio')

    def test_change_password(self):
        """
        Şifre değiştirme testi
        """
        user = User.objects.create_user(**self.user_create_data)
        token = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
        
        url = reverse('authentication:change_password')
        password_data = {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123'
        }
        
        response = self.client.post(url, password_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_logout(self):
        """
        Çıkış testi
        """
        user = User.objects.create_user(**self.user_create_data)
        token = RefreshToken.for_user(user)
        
        url = reverse('authentication:logout')
        logout_data = {'refresh': str(token)}
        
        response = self.client.post(url, logout_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT) 
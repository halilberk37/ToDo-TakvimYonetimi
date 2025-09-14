# 📚 TodoCalendar API Dokümantasyonu

## �� Genel Bilgiler

**Base URL:** `http://127.0.0.1:8000/api/`

**Authentication:** JWT (JSON Web Token) tabanlı kimlik doğrulama

**Content-Type:** `application/json`

---

## 🔐 Authentication Endpoints

### 1. Kullanıcı Kaydı
```http
POST /api/auth/register/
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "username": "username",
    "first_name": "Ad",
    "last_name": "Soyad",
    "password": "password123",
    "password_confirm": "password123"
}
```

**Response (201 Created):**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "Ad",
        "last_name": "Soyad",
        "full_name": "Ad Soyad",
        "phone_number": null,
        "birth_date": null,
        "profile_picture": null,
        "bio": "",
        "is_verified": false,
        "created_at": "2025-09-14T16:29:43.505281Z",
        "updated_at": "2025-09-14T16:29:43.505288Z"
    }
}
```

### 2. Kullanıcı Girişi
```http
POST /api/auth/login/
```

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Response (200 OK):**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
        "id": 1,
        "email": "user@example.com",
        "username": "username",
        "first_name": "Ad",
        "last_name": "Soyad",
        "full_name": "Ad Soyad"
    }
}
```

### 3. Token Yenileme
```http
POST /api/auth/token/refresh/
```

**Request Body:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 4. Kullanıcı Çıkışı
```http
POST /api/auth/logout/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (205 Reset Content):**
```json
{
    "message": "Başarıyla çıkış yapıldı."
}
```

### 5. Profil Görüntüleme
```http
GET /api/auth/profile/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
{
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "Ad",
    "last_name": "Soyad",
    "full_name": "Ad Soyad",
    "phone_number": "+905551234567",
    "birth_date": "1990-01-01",
    "profile_picture": "http://127.0.0.1:8000/media/profile_pictures/profile.jpg",
    "bio": "Kullanıcı hakkında bilgi",
    "is_verified": true,
    "created_at": "2025-09-14T16:29:43.505281Z",
    "updated_at": "2025-09-14T16:29:43.505288Z"
}
```

### 6. Profil Güncelleme
```http
PUT /api/auth/profile/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "first_name": "Yeni Ad",
    "last_name": "Yeni Soyad",
    "phone_number": "+905559876543",
    "bio": "Güncellenmiş biyografi"
}
```

### 7. Şifre Değiştirme
```http
POST /api/auth/change-password/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "old_password": "eski_sifre",
    "new_password": "yeni_sifre",
    "new_password_confirm": "yeni_sifre"
}
```

---

## 📝 Todo Endpoints

### 1. Kategori Listesi
```http
GET /api/todos/categories/
```

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `search`: Kategori adında arama
- `ordering`: Sıralama (`name`, `created_at`)

**Response (200 OK):**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "İş",
            "color": "#007bff",
            "todo_count": 5,
            "created_at": "2025-09-14T16:29:43.505281Z",
            "updated_at": "2025-09-14T16:29:43.505288Z"
        }
    ]
}
```

### 2. Kategori Oluşturma
```http
POST /api/todos/categories/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "name": "Kişisel",
    "color": "#28a745"
}
```

### 3. Kategori Detayı
```http
GET /api/todos/categories/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 4. Kategori Güncelleme
```http
PUT /api/todos/categories/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 5. Kategori Silme
```http
DELETE /api/todos/categories/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 6. Todo Listesi
```http
GET /api/todos/
```

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `is_completed`: Tamamlanma durumu (`true`/`false`)
- `priority`: Öncelik (`low`, `medium`, `high`)
- `is_important`: Önemli mi (`true`/`false`)
- `is_starred`: Yıldızlı mı (`true`/`false`)
- `category`: Kategori ID
- `is_overdue`: Süresi geçmiş mi (`true`/`false`)
- `search`: Başlık ve açıklamada arama
- `ordering`: Sıralama (`title`, `created_at`, `due_date`, `priority`)

**Response (200 OK):**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Test Todo",
            "description": "Test açıklama",
            "category": 1,
            "category_name": "İş",
            "category_color": "#007bff",
            "is_completed": false,
            "priority": "high",
            "due_date": "2025-09-20T10:00:00Z",
            "is_important": true,
            "is_starred": false,
            "days_until_due": 5,
            "is_overdue": false,
            "created_at": "2025-09-14T16:29:43.505281Z",
            "updated_at": "2025-09-14T16:29:43.505288Z"
        }
    ]
}
```

### 7. Todo Oluşturma
```http
POST /api/todos/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "title": "Yeni Todo",
    "description": "Todo açıklaması",
    "category": 1,
    "priority": "medium",
    "due_date": "2025-09-20T10:00:00Z",
    "is_important": true,
    "is_starred": false,
    "estimated_duration": "02:00:00"
}
```

### 8. Todo Detayı
```http
GET /api/todos/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Test Todo",
    "description": "Test açıklama",
    "category": {
        "id": 1,
        "name": "İş",
        "color": "#007bff",
        "todo_count": 5,
        "created_at": "2025-09-14T16:29:43.505281Z",
        "updated_at": "2025-09-14T16:29:43.505288Z"
    },
    "is_completed": false,
    "priority": "high",
    "due_date": "2025-09-20T10:00:00Z",
    "completed_at": null,
    "is_important": true,
    "is_starred": false,
    "estimated_duration": "02:00:00",
    "actual_duration": null,
    "days_until_due": 5,
    "is_overdue": false,
    "duration": "2:00:00",
    "attachments": [],
    "comments": [],
    "created_at": "2025-09-14T16:29:43.505281Z",
    "updated_at": "2025-09-14T16:29:43.505288Z"
}
```

### 9. Todo Güncelleme
```http
PUT /api/todos/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 10. Todo Silme
```http
DELETE /api/todos/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 11. Todo Tamamlama Durumu Değiştirme
```http
POST /api/todos/{id}/toggle/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Test Todo",
    "is_completed": true,
    "completed_at": "2025-09-14T16:30:00Z"
}
```

### 12. Todo Yorumu Ekleme
```http
POST /api/todos/{id}/comments/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "comment": "Bu bir yorumdur"
}
```

### 13. Todo İstatistikleri
```http
GET /api/todos/statistics/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
{
    "total_todos": 10,
    "completed_todos": 6,
    "pending_todos": 4,
    "overdue_todos": 1,
    "important_todos": 3,
    "starred_todos": 2,
    "completion_rate": 60.0
}
```

### 14. Yaklaşan Todo'lar
```http
GET /api/todos/upcoming/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "title": "Yaklaşan Todo",
        "due_date": "2025-09-16T10:00:00Z",
        "days_until_due": 2,
        "priority": "high"
    }
]
```

---

## 📅 Calendar Endpoints

### 1. Takvim Listesi
```http
GET /api/calendar/calendars/
```

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `search`: Takvim adı ve açıklamasında arama
- `ordering`: Sıralama (`name`, `created_at`)

**Response (200 OK):**
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Kişisel Takvim",
            "description": "Kişisel etkinliklerim",
            "color": "#28a745",
            "is_default": true,
            "is_public": false,
            "event_count": 5,
            "created_at": "2025-09-14T16:29:43.505281Z",
            "updated_at": "2025-09-14T16:29:43.505288Z"
        }
    ]
}
```

### 2. Takvim Oluşturma
```http
POST /api/calendar/calendars/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "name": "İş Takvimi",
    "description": "İş etkinlikleri",
    "color": "#007bff",
    "is_default": false,
    "is_public": false
}
```

### 3. Takvim Detayı
```http
GET /api/calendar/calendars/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 4. Takvim Güncelleme
```http
PUT /api/calendar/calendars/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 5. Takvim Silme
```http
DELETE /api/calendar/calendars/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 6. Etkinlik Listesi
```http
GET /api/calendar/events/
```

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**
- `event_type`: Etkinlik türü (`meeting`, `appointment`, `reminder`, `other`)
- `is_important`: Önemli mi (`true`/`false`)
- `is_private`: Özel mi (`true`/`false`)
- `calendar`: Takvim ID
- `start_date`: Başlangıç tarihi (ISO format)
- `end_date`: Bitiş tarihi (ISO format)
- `search`: Başlık, açıklama ve konumda arama
- `ordering`: Sıralama (`title`, `start_datetime`, `created_at`)

**Response (200 OK):**
```json
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Toplantı",
            "description": "Haftalık toplantı",
            "calendar": 1,
            "calendar_name": "İş Takvimi",
            "calendar_color": "#007bff",
            "start_datetime": "2025-09-16T10:00:00Z",
            "end_datetime": "2025-09-16T11:00:00Z",
            "is_all_day": false,
            "event_type": "meeting",
            "location": "Konferans Salonu",
            "is_important": true,
            "is_private": false,
            "duration": "1:00:00",
            "is_past": false,
            "is_current": false,
            "is_upcoming": true,
            "created_at": "2025-09-14T16:29:43.505281Z"
        }
    ]
}
```

### 7. Etkinlik Oluşturma
```http
POST /api/calendar/events/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "title": "Yeni Etkinlik",
    "description": "Etkinlik açıklaması",
    "calendar": 1,
    "start_datetime": "2025-09-20T10:00:00Z",
    "end_datetime": "2025-09-20T11:00:00Z",
    "is_all_day": false,
    "event_type": "meeting",
    "location": "Ofis",
    "is_important": true,
    "is_private": false,
    "reminder_minutes": 15,
    "send_notification": true
}
```

### 8. Etkinlik Detayı
```http
GET /api/calendar/events/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
{
    "id": 1,
    "title": "Toplantı",
    "description": "Haftalık toplantı",
    "calendar": {
        "id": 1,
        "name": "İş Takvimi",
        "color": "#007bff",
        "event_count": 5
    },
    "start_datetime": "2025-09-16T10:00:00Z",
    "end_datetime": "2025-09-16T11:00:00Z",
    "is_all_day": false,
    "is_recurring": false,
    "recurrence_pattern": null,
    "recurrence_end_date": null,
    "event_type": "meeting",
    "location": "Konferans Salonu",
    "is_important": true,
    "is_private": false,
    "reminder_minutes": 15,
    "send_notification": true,
    "duration": "1:00:00",
    "is_past": false,
    "is_current": false,
    "is_upcoming": true,
    "participants": [],
    "attachments": [],
    "reminders": [],
    "created_at": "2025-09-14T16:29:43.505281Z",
    "updated_at": "2025-09-14T16:29:43.505288Z"
}
```

### 9. Etkinlik Güncelleme
```http
PUT /api/calendar/events/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 10. Etkinlik Silme
```http
DELETE /api/calendar/events/{id}/
```

**Headers:** `Authorization: Bearer <access_token>`

### 11. Etkinlik Katılımcısı Ekleme
```http
POST /api/calendar/events/{id}/participants/
```

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
    "user": 2,
    "is_organizer": false,
    "response_status": "accepted"
}
```

### 12. Bugünkü Etkinlikler
```http
GET /api/calendar/events/today/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "title": "Bugünkü Etkinlik",
        "start_datetime": "2025-09-14T10:00:00Z",
        "end_datetime": "2025-09-14T11:00:00Z",
        "event_type": "meeting"
    }
]
```

### 13. Yaklaşan Etkinlikler
```http
GET /api/calendar/events/upcoming/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
[
    {
        "id": 1,
        "title": "Yaklaşan Etkinlik",
        "start_datetime": "2025-09-16T10:00:00Z",
        "end_datetime": "2025-09-16T11:0000Z",
        "event_type": "meeting"
    }
]
```

### 14. Aylık Etkinlikler
```http
GET /api/calendar/events/month/{year}/{month}/
```

**Headers:** `Authorization: Bearer <access_token>`

**Example:** `GET /api/calendar/events/month/2025/9/`

### 15. Etkinlik İstatistikleri
```http
GET /api/calendar/statistics/
```

**Headers:** `Authorization: Bearer <access_token>`

**Response (200 OK):**
```json
{
    "total_events": 15,
    "upcoming_events": 8,
    "past_events": 7,
    "today_events": 2,
    "this_week_events": 5,
    "important_events": 3,
    "private_events": 2
}
```

---

## 🔒 Güvenlik ve İzinler

### Authentication
- Tüm API endpoint'leri JWT token ile korunmaktadır
- Token süresi: 60 dakika
- Refresh token süresi: 7 gün
- Token format: `Bearer <access_token>`

### İzinler
- Kullanıcılar sadece kendi verilerine erişebilir
- Admin kullanıcıları tüm verilere erişebilir
- Etkinlik katılımcıları sadece okuma yapabilir

### Hata Kodları
- `400 Bad Request`: Geçersiz veri
- `401 Unauthorized`: Kimlik doğrulama hatası
- `403 Forbidden`: İzin hatası
- `404 Not Found`: Kaynak bulunamadı
- `500 Internal Server Error`: Sunucu hatası

---

## 📊 Rate Limiting

- API rate limiting aktif değil
- Production ortamında rate limiting eklenmesi önerilir

---

## 🧪 Test Endpoints

Test için örnek veriler:

### Test Kullanıcısı
```json
{
    "email": "test@example.com",
    "password": "testpass123"
}
```

### Test Todo
```json
{
    "title": "Test Todo",
    "description": "Test açıklama",
    "priority": "high",
    "is_important": true
}
```

### Test Etkinlik
```json
{
    "title": "Test Etkinlik",
    "description": "Test açıklama",
    "start_datetime": "2025-09-20T10:00:00Z",
    "end_datetime": "2025-09-20T11:00:00Z",
    "event_type": "meeting"
}
```

---

## 📝 Notlar

- Tüm tarih/saat değerleri ISO 8601 formatında (UTC)
- Dosya yüklemeleri için multipart/form-data kullanın
- Pagination: Sayfa başına 20 kayıt
- Search: Case-insensitive arama
- Filtering: Query parameter'lar ile filtreleme

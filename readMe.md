# 📅 TodoCalendar - To-Do ve Takvim Yönetim Sistemi

Cursor ile birlikte geliştirmeye çalıştığım bir deneme uygulaması. Uygulama nihai halinde değil eksik bırakıldı. Teme anlamda öğrenmek istediğim kısımları görüp geliştirmeyi bıraktım. İncelemek isteyenler için yüklendi.
## ✨ Özellikler

### 🔐 Kimlik Doğrulama
- JWT (JSON Web Token) tabanlı güvenli giriş sistemi
- Kullanıcı kaydı ve profil yönetimi
- Şifre değiştirme ve çıkış işlemleri
- Token yenileme mekanizması

### 📝 Todo Yönetimi
- Kategorilere göre todo organizasyonu
- Öncelik seviyeleri (Düşük, Orta, Yüksek)
- Bitiş tarihi ve hatırlatıcılar
- Önemli ve yıldızlı todo işaretleme
- Todo'ya yorum ve ek dosya ekleme
- İstatistikler ve raporlar

### 📅 Takvim Yönetimi
- Çoklu takvim desteği
- Etkinlik türleri (Toplantı, Randevu, Hatırlatıcı, Diğer)
- Tekrarlayan etkinlikler
- Katılımcı yönetimi
- Konum ve açıklama bilgileri
- Hatırlatıcı sistemi

### 🎨 Kullanıcı Deneyimi
- Responsive tasarım
- Kategori ve takvim renklendirme
- Arama ve filtreleme
- Sayfalama (Pagination)
- Gerçek zamanlı güncellemeler

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- PostgreSQL 12+
- pip (Python paket yöneticisi)

### Adım 1: Projeyi Klonlayın
```bash
git clone <repository-url>
cd proje2
```

### Adım 2: Virtual Environment Oluşturun
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate     # Windows
```

### Adım 3: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 4: Ortam Değişkenlerini Ayarlayın
`.env` dosyasını oluşturun:
```env
SECRET_KEY=your-super-secret-key-here-change-this-in-production
DEBUG=True
DB_NAME=todocalendar_db
DB_USER=your-postgres-username
DB_PASSWORD=your-postgres-password
DB_HOST=localhost
DB_PORT=5432
```

### Adım 5: Veritabanını Oluşturun
```bash
# PostgreSQL'de veritabanı oluşturun
createdb todocalendar_db

# Django migration'larını çalıştırın
python3 manage.py makemigrations
python3 manage.py migrate
```

### Adım 6: Süper Kullanıcı Oluşturun
```bash
python3 manage.py createsuperuser
```

### Adım 7: Sunucuyu Başlatın
```bash
python3 manage.py runserver
```

Sunucu `http://127.0.0.1:8000` adresinde çalışacaktır.

## 📚 API Dokümantasyonu

Detaylı API dokümantasyonu için [API_DOCUMENTATION.md](API_DOCUMENTATION.md) dosyasına bakın.

### Hızlı Başlangıç

#### 1. Kullanıcı Kaydı
```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "first_name": "Ad",
    "last_name": "Soyad",
    "password": "password123",
    "password_confirm": "password123"
  }'
```

#### 2. Giriş Yapma
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

#### 3. Todo Oluşturma
```bash
curl -X POST http://127.0.0.1:8000/api/todos/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Yeni Todo",
    "description": "Todo açıklaması",
    "priority": "medium",
    "is_important": true
  }'
```

#### 4. Etkinlik Oluşturma
```bash
curl -X POST http://127.0.0.1:8000/api/calendar/events/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Toplantı",
    "description": "Haftalık toplantı",
    "calendar": 1,
    "start_datetime": "2025-09-20T10:00:00Z",
    "end_datetime": "2025-09-20T11:00:00Z",
    "event_type": "meeting"
  }'
```

## 🧪 Testler

Projeyi test etmek için:

```bash
# Tüm testleri çalıştır
python3 manage.py test

# Belirli bir uygulamanın testlerini çalıştır
python3 manage.py test authentication
python3 manage.py test todos
python3 manage.py test calendar_app

# Detaylı test çıktısı
python3 manage.py test -v 2
```

## 📁 Proje Yapısı

```
proje2/
├── todocalendar_project/     # Ana Django projesi
│   ├── settings.py           # Proje ayarları
│   ├── urls.py              # Ana URL yapılandırması
│   └── wsgi.py              # WSGI yapılandırması
├── authentication/           # Kimlik doğrulama uygulaması
│   ├── models.py            # CustomUser modeli
│   ├── views.py             # Auth API view'ları
│   ├── serializers.py       # Auth serializer'ları
│   ├── urls.py              # Auth URL'leri
│   └── admin.py             # Admin yapılandırması
├── todos/                   # Todo uygulaması
│   ├── models.py            # Todo modelleri
│   ├── views.py             # Todo API view'ları
│   ├── serializers.py       # Todo serializer'ları
│   ├── urls.py              # Todo URL'leri
│   └── admin.py             # Admin yapılandırması
├── calendar_app/            # Takvim uygulaması
│   ├── models.py            # Calendar modelleri
│   ├── views.py             # Calendar API view'ları
│   ├── serializers.py       # Calendar serializer'ları
│   ├── urls.py              # Calendar URL'leri
│   └── admin.py             # Admin yapılandırması
├── requirements.txt         # Python bağımlılıkları
├── .env                     # Ortam değişkenleri
├── API_DOCUMENTATION.md     # API dokümantasyonu
└── readMe.md               # Bu dosya
```

## 🔧 Teknolojiler

- **Backend**: Django 5.1, Django Rest Framework 3.14
- **Veritabanı**: PostgreSQL
- **Kimlik Doğrulama**: JWT (djangorestframework-simplejwt)
- **CORS**: django-cors-headers
- **Filtreleme**: django-filter
- **Konfigürasyon**: python-decouple

## 🛡️ Güvenlik

- JWT tabanlı kimlik doğrulama
- Kullanıcı veri izolasyonu
- CORS yapılandırması
- Güvenli şifre hash'leme
- SQL injection koruması

## 📄 Veritabanı Modelleri

### CustomUser
- Email tabanlı giriş
- Profil bilgileri (ad, soyad, telefon, doğum tarihi)
- Profil resmi ve biyografi
- E-posta doğrulama durumu

### Category
- Kategori adı ve rengi
- Kullanıcıya özel kategoriler

### Todo
- Başlık, açıklama ve öncelik
- Bitiş tarihi ve tamamlama durumu
- Önemli ve yıldızlı işaretleme
- Tahmini ve gerçek süre

### Calendar
- Takvim adı, açıklama ve rengi
- Varsayılan ve genel takvim ayarları

### Event
- Etkinlik başlığı ve açıklaması
- Başlangıç ve bitiş tarihleri
- Etkinlik türü ve konumu
- Tekrarlama ayarları

## 🚀 Deployment

### Production Ayarları

1. **DEBUG** değişkenini `False` yapın
2. **SECRET_KEY**'i güvenli bir değerle değiştirin
3. **ALLOWED_HOSTS**'a domain adresinizi ekleyin
4. **DATABASE** ayarlarını production veritabanı için güncelleyin
5. **STATIC** ve **MEDIA** dosyaları için CDN kullanın
6. **HTTPS** sertifikası ekleyin

### Docker ile Deployment

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Katkıda Bulunma

1. Projeyi fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.


## 🙏 Teşekkürler

- Django ve Django Rest Framework ekibine
- PostgreSQL topluluğuna
- Tüm açık kaynak katkıda bulunanlara

---

**Not**: Bu proje eğitim amaçlı geliştirilmiştir. Production ortamında kullanmadan önce güvenlik ve performans testlerini yapın.

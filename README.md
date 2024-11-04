# Database Systems CRUD Application

Bu proje, Flask kullanarak basit bir CRUD (Create, Read, Update, Delete) işlemleri gerçekleştirmek amacıyla geliştirilmiştir. Database Systems dersi kapsamında üç kişilik bir grup çalışması olarak yapılmıştır. Bu uygulama, veritabanı işlemlerini temel seviyede anlamak ve kullanmak için geliştirilmiştir.

## Gereksinimler

- Python 3
- Git

## Kurulum Adımları

### 1. Gerekli Paketleri Yükleme

pip install Flask Flask-SQLAlchemy Flask-Migrate

Bu komut, Flask framework'ünü ve veritabanı yönetimi için gerekli olan ek kütüphaneleri kurar.

Proje Mimarisi genel hatları ile bu şekilde 
project_root/
├── backend/                   # Backend dosyaları
│   ├── app.py                 # Flask uygulamasını başlatan ana dosya
│   ├── mysql_connector.py     # Veritabanı bağlantısı ve SQL dosyası çalıştırma
│   ├── models.py              # Veritabanı ORM sınıfları
│   ├── routes.py              # CRUD işlemleri için API endpointleri
│   └── database/              # Veritabanı ile ilgili SQL dosyaları
│       └── create_tables.sql  #Tablolarun oluşturulduğu SQL sorguları
│
├── frontend/                # Frontend dosyaları
│   ├── index.html           # Ana HTML dosyası
│   ├── styles.css           # CSS dosyası
│   ├── script.js            # JavaScript dosyası
│   └── assets/              # Statik dosyalar
│
├── .gitignore               # Git tarafından izlenmemesi gereken dosyalar
├── README.md                # Proje açıklamaları
└── requirements.txt         # Python bağımlılıkları



# Database Systems CRUD Application

Bu proje, Flask kullanarak basit bir CRUD (Create, Read, Update, Delete) işlemleri gerçekleştirmek amacıyla geliştirilmiştir. Database Systems dersi kapsamında üç kişilik bir grup çalışması olarak yapılmıştır. Bu uygulama, veritabanı işlemlerini temel seviyede anlamak ve kullanmak için geliştirilmiştir.

## Gereksinimler

- Python 3
- Git

### Gerekli Paketleri Yükleme

pip install -r requirements.txt

Bu komut, Flask framework'ünü ve veritabanı yönetimi için gerekli olan ek kütüphaneleri kurar. Eğer eklemek istediğiniz ya da kullandığınız başka bir paket varsa 'requirements.txt" dosyasına yazın ki güncel kalalım.

# Proje Dosya Yapısı

Bu bölümde proje dosya yapısındaki klasörlerin ve dosyaların işlevleri açıklanmıştır. Bu yapıyı takip ederek proje içerisindeki dosyaların sorumluluklarını ve kullanım amacını kolayca anlayabilirsiniz.

## backend/
Backend ile ilgili tüm dosyaları içerir. Veritabanı işlemleri, API rotaları ve modeller bu klasörde yer alır.

- **database/**: Veritabanı ile ilgili dosyaların bulunduğu klasör. Migration sorguları vs'de burada olacak.
  - **create_tables.sql**: Veritabanı tablolarını oluşturan SQL komutlarını içerir.
- **mysql_connector.py**: Veritabanı bağlantısını kurar ve SQL dosyalarını çalıştırır. Gerekli kontrolleri yapar ve database'i hazır konuma getirir.
- **models.py**: Veritabanı tablolarının ORM modellerini tanımlar. SQLAlchemy gibi bir ORM kullanılıyorsa, burada her tabloya karşılık gelen Python sınıfları tanımlanır. Şimdilik kullanmayacağız. Lazım olursa diye duruyor.
- **routes.py**: CRUD işlemleri ve diğer API endpoint'lerinin tanımlandığı dosya. Tüm rotalar burada tanımlanarak uygulamanın işlevselliği sağlanır.
- **__init__.py**: `backend` klasörünün bir Python paketi olarak tanımlanmasını sağlar. Ayrıca Flask uygulamasını burada başlatabilirsiniz.

## frontend/
Frontend ile ilgili tüm dosyaların yer aldığı klasördür. Kullanıcı arayüzü ve statik dosyalar burada bulunur.

- **assets/**: Projede kullanılan görseller, fontlar veya diğer varlık dosyalarını içerir.
- **index.html**: Frontend’in ana HTML dosyasıdır. Kullanıcının giriş yaptığı ana sayfa olarak kullanılır.
- **script.js**: JavaScript dosyasıdır. Kullanıcı etkileşimleri ve dinamik içerik güncellemeleri için kullanılır.
- **styles.css**: CSS dosyasıdır. Sayfanın görünümünü ve stilini belirler. Daha 'statics' adı altında bir klasörde bir araya toplanabilirler.
- **base.html**: Diğer şablon dosyalarının miras aldığı temel yapı. Genelde başlık, menü, alt bilgi gibi ortak bölümleri içerir.
- **home.html**: Öylesine koydum, görevine göre html dosyası eklicez buraya.

## Ana Dosyalar

- **.gitignore**: Git tarafından izlenmemesi gereken dosyaları belirtir. Örneğin, `__pycache__` klasörlerini ve gizli veritabanı ayarlarını buraya ekleyebilirsiniz.
- **README.md**: Proje hakkında genel bilgiler, kullanım talimatları ve kurulum adımlarını içeren dökümantasyon dosyasıdır.
- **requirements.txt**: Projede kullanılan Python bağımlılıklarını listeler. Başka bir ortamda projeyi kurarken gerekli kütüphaneleri yüklemek için bu dosya kullanılır.
- **app.py**: Projenin ana dosyasıdır. Flask uygulamasını başlatır ve temel yapılandırmaları yapar. `backend` ve `frontend` bölümlerini bir araya getirir.
- **MySQL.md**: MySQL ile ilgili bilgiler ve kurulum talimatlarını içerir.




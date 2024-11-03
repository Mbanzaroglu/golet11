## MySQL Server ve MySQL Workbench Kurulumu

Bu projede veritabanı işlemlerini gerçekleştirmek için MySQL Server ve MySQL Workbench gereklidir. Aşağıdaki adımları izleyerek bilgisayarınıza MySQL Server ve MySQL Workbench’i kurabilirsiniz.

### Adım 1: MySQL Installer'ı İndirin

1. [MySQL'in resmi web sitesine](https://dev.mysql.com/downloads/installer/) gidin.
2. **Select Version** bölümünde en güncel MySQL Installer sürümünü seçin (örneğin, 8.0.40).
3. **Select Operating System** bölümünde işletim sisteminizi (Windows) seçin.
4. **Windows (x86, 32-bit), MSI Installer** seçeneklerinden birini indirin:
   - **Web Installer (2.1 MB)**: Küçük boyutludur ve kurulumu başlattığınızda MySQL bileşenlerini internetten indirir.
   - **Full Installer (306.4 MB)**: Tüm bileşenleri içerir, internet bağlantısına ihtiyaç duymaz.

### Adım 2: MySQL Installer ile Kurulum Yapın

1. İndirdiğiniz **MySQL Installer** dosyasını çalıştırın.
2. Kurulum türü olarak **Custom** veya **Server only** seçebilirsiniz. **Custom** seçeneği ile hem **MySQL Server** hem de **MySQL Workbench** bileşenlerini seçerek kurulum yapabilirsiniz.
3. **MySQL Server** ve **MySQL Workbench** bileşenlerini seçin ve devam edin.
4. Kurulum sırasında **root** kullanıcı şifresi belirlemeniz istenecektir. Bu şifreyi unutmayın; MySQL Workbench ile bağlanırken bu şifreyi kullanacaksınız.

### Adım 3: MySQL Server’ı Yapılandırma

1. Kurulum tamamlandıktan sonra **MySQL Server Configuration** sihirbazı açılacaktır. Burada sunucu ayarlarını yapın.
2. **Standart port** olarak **3306** kullanılacaktır. Bu ayarı varsayılan bırakabilirsiniz.
3. **Authentication Method** olarak **Use Strong Password Encryption for Authentication** seçeneğini seçin.
4. **root** şifrenizi tekrar onaylayın.

### Adım 4: MySQL Workbench ile Bağlantı Kurma

1. MySQL Workbench’i açın.
2. **MySQL Connections** bölümünde **+** simgesine tıklayarak yeni bir bağlantı oluşturun.
3. **Connection Name** kısmına bir isim verin (örneğin, "Local MySQL").
4. **Hostname** kısmına `localhost` yazın ve **Port** alanını `3306` olarak bırakın.
5. **Username** alanına `root` yazın.
6. **Password** kısmında **Store in Vault...** seçeneğine tıklayarak root şifrenizi girin.
7. **Test Connection** butonuna tıklayarak bağlantıyı test edin. Bağlantı başarılıysa, ayarları kaydedin ve MySQL Server’a bağlanabilirsiniz.

### Notlar

- MySQL Server yüklendikten sonra otomatik olarak arka planda çalışır.
- Veritabanı işlemlerini yapmak için MySQL Workbench’i kullanarak MySQL Server’a bağlanabilirsiniz.
- Kurulum sırasında belirlediğiniz **root** şifresini güvenli bir yerde saklayın.

---

Bu adımları takip ederek MySQL Server ve MySQL Workbench kurulumunu tamamlayabilir ve veritabanı işlemlerine başlayabilirsiniz.

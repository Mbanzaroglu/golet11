// "Create Song" butonuna tıklanınca bu fonksiyon çalışır
function createSong() {
    // Formdaki verileri al
    const title = document.getElementById("title").value;
    const duration = document.getElementById("duration").value;
    const genre = document.getElementById("genre").value;
    const artist = document.getElementById("artist").value;

    // API'ye gönderilecek veri yapısını JSON formatında hazırla
    const data = {
        title: title,
        duration: duration,
        genre: genre,
        artist: artist
    };

    // API'ye POST isteği gönder
    fetch('/create_song', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)  // Veriyi JSON formatına çevirerek gönder
    })
    .then(response => response.json())  // Yanıtı JSON formatında işle
    .then(result => {
        // API'den gelen mesajı sayfada göster
        document.getElementById("message").innerText = result.message || result.error;
    })
    .catch(error => console.error('Error:', error));  // Hata varsa konsola yazdır
}

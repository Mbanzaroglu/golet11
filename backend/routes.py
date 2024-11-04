from flask import Blueprint, request, jsonify
from backend.mysql_connector import conn  # MySQL bağlantısını import edin

main = Blueprint('main', __name__)

@main.route('/create_song', methods=['POST'])
def create_song():
    data = request.json  # Gelen JSON veriyi al
    title = data.get("title")  # Şarkı başlığı
    duration = data.get("duration")  # Şarkının süresi
    genre = data.get("genre")  # Şarkının türü
    artist = data.get("artist")  # Şarkının sanatçısı

    # SQL sorgusu
    query = """
    INSERT INTO bp_release (release_title, release_date, release_url, label_id, updated_on)
    VALUES (%s, %s, %s, %s, NOW())
    """

    # Bağlantıyı kullanarak SQL sorgusunu çalıştır
    cursor = conn.cursor()
    try:
        cursor.execute(query, (title, duration, genre, artist))
        conn.commit()  # Değişiklikleri veritabanına kaydet
        response = {"message": "Song created successfully"}
    except Exception as e:
        conn.rollback()  # Hata durumunda değişiklikleri geri al
        response = {"error": str(e)}
    finally:
        cursor.close()  # Cursor'u kapat

    return jsonify(response)  # Yanıtı JSON formatında döndür

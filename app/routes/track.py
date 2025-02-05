from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.db_connection import get_db_connection_and_cursor
from flask_login import login_required, current_user
import json
import datetime

track_bp = Blueprint('track_bp', __name__, url_prefix='/track')

@track_bp.route('/details/<int:track_id>/<int:artist_id>')
def track_detail(track_id, artist_id):
    index = request.args.get('index', default=0, type=int)
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            bp_track.track_id,
            bp_track.title,
            bp_track.mix,
            bp_track.release_date,
            bp_track.bpm,
            bp_track.duration,
            bp_release.release_title,
            bp_genre.genre_name,
            bp_artist.artist_name
        FROM
            bp_track
        LEFT JOIN
            artist_track ON bp_track.track_id = artist_track.track_id
        LEFT JOIN
            bp_artist ON artist_track.artist_id = bp_artist.artist_id
        LEFT JOIN
            bp_release ON bp_track.release_id = bp_release.release_id
        LEFT JOIN
            bp_genre ON bp_track.genre_id = bp_genre.genre_id
        WHERE
            bp_track.track_id = %(track_id)s AND
            bp_artist.artist_id = %(artist_id)s
        """
        cursor.execute(query, {'track_id': track_id, 'artist_id': artist_id})
        track_rows = cursor.fetchall()  # Tüm sonuçları al
        if current_user.is_authenticated:
            # Kullanıcının favorilerinde bu şarkının olup olmadığını kontrol et
            cursor.execute("""
                SELECT * FROM favorite_tracks WHERE user_id = %s AND track_id = %s
            """, (current_user.id, track_id))
            is_favorite = cursor.fetchone() is not None
        else:
            is_favorite = False

    if not track_rows:
        # Eğer sonuç yoksa, kullanıcıya 404 dönebilirsiniz
        return "Track not found", 404

    # İlk satırdaki genel verileri al
    track_data = track_rows[0]

    artists = [track_data['artist_name']] if track_data['artist_name'] else []
    # Sorgudaki LEFT JOINler ile tüm verileri olan datalara erişiyoruz ama yine de tedbir olarak aşağıdaki gibi
    # koşullar koyarak verinin olmadığı durumda hata almamak için null atıyoruz. 
    track_dict = {
        "id": track_data['track_id'],
        "title": track_data['title'],
        "mix": track_data['mix'] if track_data['mix'] else "Original Mix",
        "artists": artists,
        "release_date": track_data['release_date'].strftime('%Y-%m-%d') if track_data['release_date'] else "",
        "genre_name": track_data['genre_name'] if track_data['genre_name'] else "Unknown",
        "bpm": track_data['bpm'] if track_data['bpm'] else "",
        # Duration TIME tipinde geliyor. String olarak dönüşütürüp salise kısmını çıkarıyoruz.
        "duration": str(track_data['duration']).rsplit(':', 1)[0] if track_data['duration'] else "00:00",
        "release_title": track_data['release_title'] if track_data['release_title'] else "Unknown"
    }

    return render_template('track.html', track=track_dict, is_favorite=is_favorite, index=index)

@track_bp.route('/add_favorite', methods=['POST'])
@login_required
def add_favorite():
    # Kullanıcıdan gelen track_id verisini al
    track_id = request.form.get('track_id')
    
    if not track_id:
        flash('Geçerli bir şarkı seçilmedi.', 'danger')
        return redirect(url_for('main_bp.home'))  # Kullanıcıyı ana sayfaya yönlendir

    try:
        with get_db_connection_and_cursor() as (conn, cursor):
            # Kullanıcının aynı şarkıyı daha önce ekleyip eklemediğini kontrol et
            cursor.execute("""
                SELECT * FROM favorite_tracks WHERE user_id = %s AND track_id = %s
            """, (current_user.id, track_id))
            
            existing_favorite = cursor.fetchone()
            if existing_favorite:
                flash('Bu şarkı zaten favorilerde.', 'info')
                return redirect(request.referrer or url_for('main_bp.home'))  # Kullanıcıyı önceki sayfaya döndür

            # Şarkıyı favorilere ekle
            cursor.execute("""
                INSERT INTO favorite_tracks (user_id, track_id) VALUES (%s, %s)
            """, (current_user.id, track_id))
            conn.commit()
            flash('Şarkı favorilere eklendi!', 'success')
            return redirect(request.referrer or url_for('main_bp.home'))  # Kullanıcıyı önceki sayfaya döndür


    except Exception as e:
        flash(f'Favorilere eklerken bir hata oluştu: {str(e)}', 'danger')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@track_bp.route('/remove_favorite', methods=['POST'])
@login_required
def remove_favorite():
    track_id = request.form.get('track_id')
    
    if not track_id:
        flash('Geçerli bir şarkı seçilmedi.', 'danger')
        return redirect(url_for('main_bp.home'))

    try:
        with get_db_connection_and_cursor() as (conn, cursor):
            cursor.execute("""
                SELECT * FROM favorite_tracks WHERE user_id = %s AND track_id = %s
            """, (current_user.id, track_id))
            
            existing_favorite = cursor.fetchone()
            if not existing_favorite:
                flash('Bu şarkı favorilerde bulunamadı.', 'info')
                return redirect(request.referrer or url_for('main_bp.home'))

            cursor.execute("""
                DELETE FROM favorite_tracks WHERE user_id = %s AND track_id = %s
            """, (current_user.id, track_id))
            conn.commit()
            flash('Şarkı favorilerden kaldırıldı!', 'success')
            return redirect(request.referrer or url_for('main_bp.home'))

    except Exception as e:
        flash(f'Favorilerden kaldırırken bir hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('main_bp.home'))
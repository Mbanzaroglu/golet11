from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.db_connection import get_db_connection_and_cursor
from flask_login import login_required, current_user
import datetime

album_bp = Blueprint('album_bp', __name__, url_prefix='/albums')


@album_bp.route('/details/<int:release_id>/<int:artist_id>')
def album_detail(release_id, artist_id):
    with get_db_connection_and_cursor() as (conn, cursor):
        # Albüm detaylarını ve şarkıları çeken sorgu
        query = """
        SELECT
            br.release_id,
            br.release_title,
            br.release_date,
            br.release_title,
            ba.artist_name,
            bt.title,
            bt.track_id
        FROM
            bp_release br
        LEFT JOIN
            artist_release ar ON br.release_id = ar.release_id
        LEFT JOIN
            bp_artist ba ON ar.artist_id = ba.artist_id
        LEFT JOIN
            bp_track bt ON br.release_id = bt.release_id
        WHERE
            br.release_id = %(release_id)s AND
            ba.artist_id = %(artist_id)s
        ORDER BY
            bt.track_id
        """
        cursor.execute(query, {'release_id': release_id, 'artist_id': artist_id})
        album_rows = cursor.fetchall()

        if not album_rows:
            return "Release not found", 404

        # Albüm detaylarını ve şarkıları düzenleyin
        release_data = album_rows[0]
        tracks = [
            {
                "title": row['title'],
                "number": row['track_id']
            }
            for row in album_rows if row['title']
        ]

        release_dict = {
            "id": release_data['release_id'],
            "title": release_data['release_title'],
            "artists": [release_data['artist_name']],
            "release_date": release_data['release_date'].strftime('%Y-%m-%d') if release_data['release_date'] else "",
            "release_title": release_data['release_title'] if release_data['release_title'] else "Unknown",
            "tracks": tracks
        }

        cursor.execute("""
            SELECT * FROM favorite_albums 
            WHERE user_id = %s AND album_id = %s
        """, (current_user.id, release_id))
        is_favorite = cursor.fetchone() is not None

        return render_template('album.html', album=release_dict, is_favorite=is_favorite)

@album_bp.route('/add_favorite_album', methods=['POST'])
@login_required
def add_favorite_album():
    # Kullanıcıdan gelen release_id verisini al
    release_id = request.form.get('release_id')

    print(f"Gönderilen album_id: {release_id}")

    if not release_id:
        flash('Geçerli bir albüm seçilmedi.', 'danger')
        return redirect(url_for('main_bp.home'))  # Kullanıcıyı ana sayfaya yönlendir

    try:
        with get_db_connection_and_cursor() as (conn, cursor):
            # Kullanıcının aynı albümü daha önce ekleyip eklemediğini kontrol et
            cursor.execute("""
                SELECT * FROM favorite_albums WHERE user_id = %s AND album_id = %s
            """, (current_user.id, release_id))
            
            existing_favorite = cursor.fetchone()
            if existing_favorite:
                flash('Bu albüm zaten favorilerde.', 'info')
                return redirect(request.referrer or url_for('main_bp.home'))  # Kullanıcıyı önceki sayfaya döndür

            # Şarkıyı favorilere ekle
            cursor.execute("""
                INSERT INTO favorite_albums (user_id, album_id) VALUES (%s, %s)
            """, (current_user.id, release_id))
            conn.commit()
            flash('Albüm favorilere eklendi!', 'success')
            return redirect(request.referrer or url_for('main_bp.home'))  # Kullanıcıyı önceki sayfaya döndür


    except Exception as e:
        flash(f'Favorilere eklerken bir hata oluştu: {str(e)}', 'danger')

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@album_bp.route('/remove_favorite_album', methods=['POST'])
@login_required
def remove_favorite():
    release_id = request.form.get('release_id')
    
    if not release_id:
        flash('Geçerli bir albüm seçilmedi.', 'danger')
        return redirect(url_for('main_bp.home'))

    try:
        with get_db_connection_and_cursor() as (conn, cursor):
            cursor.execute("""
                SELECT * FROM favorite_albums WHERE user_id = %s AND album_id = %s
            """, (current_user.id, release_id))
            
            existing_favorite = cursor.fetchone()
            if not existing_favorite:
                flash('Bu albüm favorilerde bulunamadı.', 'info')
                return redirect(request.referrer or url_for('main_bp.home'))

            cursor.execute("""
                DELETE FROM favorite_albums WHERE user_id = %s AND album_id = %s
            """, (current_user.id, release_id))
            conn.commit()
            flash('Albüm favorilerden kaldırıldı!', 'success')
            return redirect(request.referrer or url_for('main_bp.home'))

    except Exception as e:
        flash(f'Favorilerden kaldırırken bir hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('main_bp.home'))
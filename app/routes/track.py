from flask import Blueprint, render_template, request
from app.utils.db_connection import get_db_connection_and_cursor
import json
import datetime

track__bp = Blueprint('track_bp', __name__, url_prefix='/track')

@track__bp.route('/details/<int:track_id>')
def track_detail(track_id):
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
            bp_track.track_id = %s
        """
        cursor.execute(query, (track_id,))
        track_data = cursor.fetchone()

    artists = [track_data['artist_name']] if track_data['artist_name'] else []

    track_dict = {
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

    return render_template('track.html', track=track_dict)

from flask import Blueprint, render_template, request
from app.utils.db_connection import get_db_connection_and_cursor
import json
import datetime

track__bp = Blueprint('track_bp', __name__, url_prefix='/track')

@track__bp.route('/details') #/<int:track_id> ekle sonuna.
def track_detail():
    # selected_page = 'track_detail'
    # with get_db_connection_and_cursor() as (conn, cursor):
    #     query = """
    #     SELECT
    #         bp_track.track_id,
    #         bp_track.title,
    #         bp_artist.artist_name
    #     FROM
    #         bp_track
    #     LEFT JOIN
    #         artist_track ON bp_track.track_id = artist_track.track_id
    #     LEFT JOIN
    #         bp_artist ON artist_track.artist_id = bp_artist.artist_id
    #     WHERE
    #         bp_track.track_id = %s
    #     """
    #     cursor.execute(query, (track_id,))
    #     track_data = cursor.fetchone()
    track_data = {
    "title": "Summer Vibes",
    "mix": "Original Mix",
    "artists": ["DJ Example", "Producer Name"],
    "release_date": datetime.datetime(2024, 12, 8).strftime('%Y-%m-%d'),  # String formatına dönüştür
    "genre_name": "House",
    "bpm": "128",
    "duration": 405,
    "remixers": ["Remixer 1", "Remixer 2"],
    "release_title": "Marshall Matters"
}
    return render_template('track.html',track=track_data)
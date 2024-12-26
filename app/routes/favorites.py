from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.db_connection import get_db_connection_and_cursor

fav_bp = Blueprint('fav_bp', __name__, url_prefix='/favorites')

@fav_bp.route('/songs')
@login_required
def favorite_songs():
    selected_page = 'songs'
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            bp_track.track_id,
            bp_track.title AS song_title,
            MIN(bp_artist.artist_name) AS artist_name,  -- İlk sanatçıyı seçiyoruz
            MIN(artist_track.artist_id) AS artist_id   -- İlgili artist_id'yi seçiyoruz
        FROM
            favorite_tracks as ft
        INNER JOIN
            bp_track ON ft.track_id = bp_track.track_id
        INNER JOIN
            artist_track ON bp_track.track_id = artist_track.track_id
        INNER JOIN
            bp_artist ON artist_track.artist_id = bp_artist.artist_id
        WHERE
            ft.user_id = %(user_id)s
        GROUP BY
            bp_track.track_id, bp_track.title;
        """
        cursor.execute(query, {'user_id': current_user.id})
        track_rows = cursor.fetchall()

    if not track_rows:
        return "No tracks found for this user.", 404

    tracks = []
    for row in track_rows:
        tracks.append({
            "track_id": row['track_id'],
            "title": row['song_title'],
            "artist_name": row['artist_name'],
            "artist_id": row['artist_id']
        })

    return render_template('fav.html', tracks=tracks, selected_page=selected_page)



@fav_bp.route('/albums')
@login_required
def favorite_albums():
    selected_page = 'releases'
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            br.release_id,
            br.release_title,
            ba.artist_name,
            ar.artist_id
        FROM
            favorite_albums fa
        INNER JOIN
            bp_release br ON fa.album_id = br.release_id
        INNER JOIN
            artist_release ar ON br.release_id = ar.release_id
        INNER JOIN
            bp_artist ba ON ar.artist_id = ba.artist_id
        WHERE
            fa.user_id = %s
        """
        cursor.execute(query, (current_user.id,))
        favorite_albums_list = cursor.fetchall()
        
    return render_template('fav.html', selected_page=selected_page, albums=favorite_albums_list)


@fav_bp.route('/artists')
@login_required
def favorite_artists():
    selected_page = 'artists'
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            bp_artist.artist_id,
            bp_artist.artist_name,
            bp_artist.artist_url
        FROM
            favorite_artists
        INNER JOIN
            bp_artist ON favorite_artists.artist_id = bp_artist.artist_id
        WHERE
            favorite_artists.user_id = %s
        """
        cursor.execute(query, (current_user.id,))
        favorite_artists_list = cursor.fetchall()
    if not favorite_artists_list:
        return "No Favorite artists found",404 

    artists=[]
    for row in favorite_artists_list:
        artists.append({
            "artist_id": row['artist_id'],
            "artist_name": row['artist_name']
        })

        
    return render_template('fav.html', selected_page=selected_page, artists=favorite_artists_list)

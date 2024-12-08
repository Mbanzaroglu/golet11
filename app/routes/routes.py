from flask import Blueprint, render_template, request
from app.utils.db_connection import get_db_connection_and_cursor

# Define a Blueprint for routes
main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    selected_page = "home"
    return render_template('home.html', selected_page=selected_page)

@main_bp.route('/songs')
def songs():
    selected_page = "songs"
    # SQL query to get songs with their artists
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            bp_track.track_id,
            bp_track.title,
            bp_artist.artist_name
        FROM
            bp_track
        LEFT JOIN
            artist_track ON bp_track.track_id = artist_track.track_id
        LEFT JOIN
            bp_artist ON artist_track.artist_id = bp_artist.artist_id
        """
        cursor.execute(query)
        songs_list = cursor.fetchall()
    return render_template('home.html', selected_page=selected_page, songs=songs_list)

@main_bp.route('/albums')
def albums():
    selected_page = 'albums'
    # SQL query to get albums with their artists
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            bp_release.release_id,
            bp_release.release_title,
            bp_artist.artist_name
        FROM
            bp_release
        LEFT JOIN
            artist_release ON bp_release.release_id = artist_release.release_id
        LEFT JOIN
            bp_artist ON artist_release.artist_id = bp_artist.artist_id
        """
        cursor.execute(query)
        albums_list = cursor.fetchall()
    return render_template('home.html', selected_page=selected_page, albums=albums_list)

@main_bp.route('/artists')
def artists():
    selected_page = 'artists'
    # SQL query to get artist information
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            artist_id,
            artist_name,
            artist_url
        FROM
            bp_artist
        """
        cursor.execute(query)
        artist_list = cursor.fetchall()

    return render_template('home.html', selected_page=selected_page, artists=artist_list)

@main_bp.route('/search')
def search():
    selected_page = 'search'
    query_param = request.args.get('q', '')
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            bp_track.track_id,
            bp_track.title,
            bp_artist.artist_name
        FROM
            bp_track
        LEFT JOIN
            artist_track ON bp_track.track_id = artist_track.track_id
        LEFT JOIN
            bp_artist ON artist_track.artist_id = bp_artist.artist_id
        WHERE
            bp_track.title LIKE %s OR bp_artist.artist_name LIKE %s
        """
        search_term = f"%{query_param}%"
        cursor.execute(query, (search_term, search_term))
        search_results = cursor.fetchall()

    return render_template('home.html', selected_page=selected_page, search_results=search_results, query=query_param)
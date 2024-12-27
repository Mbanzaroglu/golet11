from flask import Blueprint, render_template, request
from app.utils.db_connection import get_db_connection_and_cursor

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    selected_page = "home"
    return render_template('home.html', selected_page=selected_page, hide_navigation=True)

@main_bp.route('/songs')
def songs():
    selected_page = "songs"
    page = request.args.get('page', 1, type=int)
    per_page = 24
    offset = (page - 1) * per_page

    songs_list = []
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            bp_track.track_id,
            bp_track.title AS song_title,
            GROUP_CONCAT(DISTINCT bp_artist.artist_name ORDER BY bp_artist.artist_name SEPARATOR ', ') AS artist_names,
            GROUP_CONCAT(DISTINCT bp_artist.artist_id SEPARATOR ', ') AS artist_ids
        FROM
            bp_track
        INNER JOIN
            artist_track ON bp_track.track_id = artist_track.track_id
        INNER JOIN
            bp_artist ON artist_track.artist_id = bp_artist.artist_id
        GROUP BY
            bp_track.track_id, bp_track.title
        ORDER BY
            bp_track.track_id ASC
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (per_page, offset))
        songs_list = cursor.fetchall()

        query_count = "SELECT COUNT(*) as total_songs FROM bp_track"
        cursor.execute(query_count)
        res = cursor.fetchone()
        total_songs=res['total_songs']


    total_pages = (total_songs // per_page) + (1 if total_songs % per_page > 0 else 0)
    return render_template('home.html', selected_page=selected_page, songs=songs_list, page=page, total_pages=total_pages)

@main_bp.route('/albums')
def albums():
    selected_page = "albums"
    page = request.args.get('page', 1, type=int)
    per_page = 21
    offset = (page - 1) * per_page

    albums_list = []
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            bp_release.release_id,
            bp_release.release_title AS release_title,
            GROUP_CONCAT(DISTINCT bp_artist.artist_name ORDER BY bp_artist.artist_name SEPARATOR ', ') AS artist_name,
            GROUP_CONCAT(DISTINCT bp_artist.artist_id SEPARATOR ', ') AS artist_ids,
            GROUP_CONCAT(DISTINCT bp_genre.genre_name ORDER BY bp_genre.genre_name SEPARATOR ', ') AS genre_names
        FROM
            bp_release
        INNER JOIN
            artist_release ON bp_release.release_id = artist_release.release_id
        INNER JOIN
            bp_artist ON artist_release.artist_id = bp_artist.artist_id
        INNER JOIN
            bp_track ON bp_release.release_id = bp_track.release_id
        INNER JOIN
            bp_genre ON bp_track.genre_id = bp_genre.genre_id
        GROUP BY
            bp_release.release_id, bp_release.release_title
        ORDER BY
            bp_release.release_id ASC
        LIMIT %s OFFSET %s;
        """
        cursor.execute(query, (per_page, offset))
        albums_list = cursor.fetchall()

        query_count = "SELECT COUNT(*) as total_albums FROM bp_release"
        cursor.execute(query_count)
        res = cursor.fetchone()
        total_albums=res['total_albums']

    total_pages = (total_albums // per_page) + (1 if total_albums % per_page > 0 else 0)
    return render_template('home.html', selected_page=selected_page, albums=albums_list, page=page, total_pages=total_pages)

@main_bp.route('/artists')
def artists():
    selected_page = "artists"
    page = request.args.get('page', 1, type=int)
    per_page = 24
    offset = (page - 1) * per_page

    artist_list = []
    with get_db_connection_and_cursor() as (conn, cursor):
        query = """
        SELECT
            artist_id,
            artist_name,
            artist_url
        FROM
            bp_artist
        LIMIT %s OFFSET %s
        """
        cursor.execute(query, (per_page, offset))
        artist_list = cursor.fetchall()

        query_count = "SELECT COUNT(*) as total_artist FROM bp_artist"
        cursor.execute(query_count)
        res = cursor.fetchone()
        total_artists=res['total_artist']

    total_pages = (total_artists // per_page) + (1 if total_artists % per_page > 0 else 0)
    return render_template('home.html', selected_page=selected_page, artists=artist_list, page=page, total_pages=total_pages)


@main_bp.route('/search', methods=['GET'])
def search():
    """
    Bir arama sayfası oluşturuyoruz. Formdan hem 'q' (arama terimi) hem de
    'selected_page' parametresini alıp, gelen değere göre farklı sorgular yapacağız.
    """
    # Arama kutusundan gelen metni alıyoruz (örn. şarkı veya sanatçı adı)
    query_param = request.args.get('q', '')
    # Kullanıcının hangi sayfadayken arama yaptığına göre sorgu seçeceğiz
    selected_page = request.args.get('selected_page', 'songs')
    
    # Burada sonuçları tutacak bir liste değişkeni oluşturuyoruz
    search_results = []

    # Veritabanı bağlantısı açıyoruz
    with get_db_connection_and_cursor() as (conn, cursor):
        # Hangi sayfada arama yapılacağına göre farklı sorgular döndürüyoruz
        if selected_page == 'songs':
            """
            'songs' seçeneği için, tıpkı yukarıdaki 'songs' fonksiyonunda olduğu gibi
            şarkı ve sanatçıları bir arada çeken sorguyu, 'WHERE' koşuluna
            LIKE ekleyerek kullanıyoruz.
            """
            # Bu sorgu main_bp.songs ile aynı kolonları çekiyor çünkü ikisi de home.html select_page='songs' olduğunda çalışıyor.
            query = """
            SELECT
                bp_track.track_id,
                bp_track.title AS song_title,
                GROUP_CONCAT(DISTINCT bp_artist.artist_name ORDER BY bp_artist.artist_name SEPARATOR ', ') AS artist_names,
                GROUP_CONCAT(DISTINCT bp_artist.artist_id SEPARATOR ', ') AS artist_ids
            FROM
                bp_track
            INNER JOIN
                artist_track ON bp_track.track_id = artist_track.track_id
            INNER JOIN
                bp_artist ON artist_track.artist_id = bp_artist.artist_id
            WHERE
                bp_track.title LIKE %s OR bp_artist.artist_name LIKE %s
            GROUP BY
                bp_track.track_id, bp_track.title
            ORDER BY
                bp_track.track_id ASC
            LIMIT 50
            """
            # Aranacak stringin başına ve sonuna '%' ekleyerek LIKE kullanıyoruz
            search_term = f"%{query_param}%"
            cursor.execute(query, (search_term, search_term))
            search_results = cursor.fetchall()

        elif selected_page == 'artists':
            """
            'artists' sayfası için sanatçı bilgilerini getiriyoruz.
            """
            query = """
            SELECT
                artist_id,
                artist_name,
                artist_url
            FROM
                bp_artist
            WHERE
                artist_name LIKE %s
            """
            search_term = f"%{query_param}%"
            cursor.execute(query, (search_term,))
            search_results = cursor.fetchall()

        elif selected_page == 'albums':
            """
            'albums' sayfası için albüm ve şarkı bilgilerini getiriyoruz.
            """
            query = """
            SELECT
                bp_release.release_id,
                bp_release.release_title AS release_title,
                GROUP_CONCAT(DISTINCT bp_artist.artist_name ORDER BY bp_artist.artist_name SEPARATOR ', ') AS artist_name,
                GROUP_CONCAT(DISTINCT bp_artist.artist_id SEPARATOR ', ') AS artist_ids
            FROM
                bp_release
            LEFT JOIN
                artist_release ON bp_release.release_id = artist_release.release_id
            LEFT JOIN
                bp_artist ON artist_release.artist_id = bp_artist.artist_id
            WHERE
                bp_release.release_title LIKE %s
                OR bp_artist.artist_name LIKE %s
            GROUP BY
                bp_release.release_id, bp_release.release_title
            ORDER BY
                bp_release.release_id ASC
            """
            search_term = f"%{query_param}%"
            cursor.execute(query, (search_term, search_term))
            search_results = cursor.fetchall()

        else:
            """
            Herhangi bir değer gelmediyse varsayılan olarak albüm arıyoruz.
            """
            query = """
            SELECT
                bp_track.track_id,
                bp_track.title,
                bp_artist.artist_name
            FROM
                bp_track
            INNER JOIN
                artist_track ON bp_track.track_id = artist_track.track_id
            INNER JOIN
                bp_artist ON artist_track.artist_id = bp_artist.artist_id
            WHERE
                bp_track.title LIKE %s OR bp_artist.artist_name LIKE %s
            """
            search_term = f"%{query_param}%"
            cursor.execute(query, (search_term, search_term))
            search_results = cursor.fetchall()

    # Seçilen sayfanın türünü (songs/artists/albums) ve arama sonuçlarını gönderiyoruz
    # 'query' ile de formdan gelen metni tekrar döndürüyoruz ki arama kutusunda görünsün.
    return render_template(
        'home.html',
        selected_page=selected_page,
        search_results=search_results,
        query=query_param
    )

from flask import Blueprint, render_template, request ,redirect, url_for
from app.utils.db_connection import get_db_connection_and_cursor
from flask_login import login_required, current_user

main_bp = Blueprint('main_bp', __name__)

@main_bp.route('/')
def home():
    selected_page = "home"
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.auth_home'))
    return render_template('home.html', selected_page=selected_page, hide_navigation=True)

@main_bp.route('/home')
@login_required
def auth_home():
    selected_page="home"
    user_name='User'
    recommendations = {
        'tracks': [],
        'albums': [],
        'artists': []
    }

    with get_db_connection_and_cursor() as (conn, cursor):
        cursor.execute("SELECT username FROM users WHERE id = %s", (current_user.id,))
        result = cursor.fetchone()
        if result:
            user_name = result['username']  


        cursor.execute("SELECT track_id FROM favorite_tracks WHERE user_id = %s", (current_user.id,))
        favorite_tracks = [row['track_id'] for row in cursor.fetchall()]

        if favorite_tracks:
            # Dynamically construct the IN clause
            placeholders = ', '.join(['%s'] * len(favorite_tracks))
            query = f"""
                SELECT DISTINCT genre_id
                FROM bp_track
                WHERE track_id IN ({placeholders})
            """
            cursor.execute(query, favorite_tracks)
            genre_ids = [row['genre_id'] for row in cursor.fetchall()]

            if genre_ids:
                placeholders = ', '.join(['%s'] * len(genre_ids))
                query = f"""
                    SELECT bp_track.track_id, bp_track.title, artist_track.artist_id
                    FROM bp_track
                    INNER JOIN artist_track ON bp_track.track_id = artist_track.track_id
                    INNER JOIN bp_release ON bp_track.release_id = bp_release.release_id
                    WHERE bp_track.genre_id IN ({placeholders})
                    ORDER BY RAND() LIMIT 4
                """
                cursor.execute(query, genre_ids)
                recommendations['tracks'] = cursor.fetchall()
        else:
            # No favorite tracks, provide random track recommendations
            cursor.execute("""
                SELECT bp_track.track_id, bp_track.title, bp_track.genre_id, artist_track.artist_id
                FROM bp_track
                INNER JOIN artist_track ON bp_track.track_id = artist_track.track_id
                INNER JOIN bp_release ON bp_track.release_id = bp_release.release_id
                ORDER BY RAND() LIMIT 4
            """)
            recommendations['tracks'] = cursor.fetchall()



        # Get favorite albums
        cursor.execute("SELECT album_id FROM favorite_albums WHERE user_id = %s", (current_user.id,))
        favorite_albums = [row['album_id'] for row in cursor.fetchall()]

        if favorite_albums:
            placeholders = ', '.join(['%s'] * len(favorite_albums))
            query = f"""
                SELECT FLOOR(AVG(bpt.genre_id)) AS avg_genre
                FROM bp_release
                inner join
                bp_track bpt on bpt.release_id=bp_release.release_id
                WHERE bp_release.release_id IN ({placeholders})
            """
            cursor.execute(query, favorite_albums)
            avg_genre = cursor.fetchone()['avg_genre']

            if avg_genre:
                query = """
                    SELECT bp_release.release_id, bp_release.release_title, artist_release.artist_id
                    FROM bp_release
                    INNER JOIN artist_release ON bp_release.release_id = artist_release.release_id
                    INNER JOIN bp_track bpt on bpt.release_id=bp_release.release_id
                    WHERE genre_id = %s
                    ORDER BY RAND() LIMIT 4
                """
                cursor.execute(query, (avg_genre,))
                recommendations['albums'] = cursor.fetchall()
        else:
            # No favorite albums, provide random album recommendations
            cursor.execute("""
                SELECT bpr.release_id, bpr.release_title, bpt.genre_id, artist_release.artist_id
                FROM bp_release bpr
                INNER JOIN artist_release ON bpr.release_id = artist_release.release_id
                INNER JOIN bp_track bpt ON bpr.release_id=bpt.release_id 
                ORDER BY RAND() LIMIT 4
            """)
            recommendations['albums'] = cursor.fetchall()




        # Get favorite artists
        cursor.execute("SELECT artist_id FROM favorite_artists WHERE user_id = %s", (current_user.id,))
        favorite_artists = [row['artist_id'] for row in cursor.fetchall()]

        if favorite_artists:
            placeholders = ', '.join(['%s'] * len(favorite_artists))
            query = f"""
                SELECT DISTINCT genre_id
                FROM bp_track
                WHERE track_id IN (
                    SELECT track_id
                    FROM artist_track
                    WHERE artist_id IN ({placeholders})
                )
            """
            cursor.execute(query, favorite_artists)
            genre_ids = [row['genre_id'] for row in cursor.fetchall()]

            if genre_ids:
                placeholders = ', '.join(['%s'] * len(genre_ids))
                query = f"""
                    SELECT artist_id, artist_name
                    FROM bp_artist
                    WHERE artist_id IN (
                        SELECT artist_id
                        FROM artist_track
                        WHERE track_id IN (
                            SELECT track_id
                            FROM bp_track
                            WHERE genre_id IN ({placeholders})
                        )
                    )
                    ORDER BY RAND() LIMIT 4
                """
                cursor.execute(query, genre_ids)
                recommendations['artists'] = cursor.fetchall()
        else:
            # No favorite artists, provide random artist recommendations
            cursor.execute("""
                SELECT artist_id, artist_name FROM bp_artist ORDER BY RAND() LIMIT 4
            """)
            recommendations['artists'] = cursor.fetchall()

    return render_template('home.html',user_name=user_name, selected_page=selected_page, recommendations=recommendations)



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
        query=query_param,
        total_pages=1
    )

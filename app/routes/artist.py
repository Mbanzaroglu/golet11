from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.db_connection import get_db_connection_and_cursor
from flask_login import login_required, current_user
import json
import datetime

artist_bp=Blueprint('artist_bp',__name__,url_prefix='/artist')


@artist_bp.route('/details/<int:artist_id>')
def artist_detail(artist_id):
    with get_db_connection_and_cursor() as (conn,cursor):
        query="""
        SELECT
            ar.artist_id,
            bpa.artist_name,
            ar.release_id,
            br.release_title,
            br.release_date
        FROM
            artist_release ar
        INNER JOIN
            bp_release br ON ar.release_id = br.release_id
        inner join
            bp_artist bpa on ar.artist_id = bpa.artist_id
        WHERE
            ar.artist_id = %(artist_id)s
        ORDER BY
            br.release_date DESC
        """

        cursor.execute(query,{'artist_id':artist_id})
        artist_rows=cursor.fetchall()
        if current_user.is_authenticated:
            cursor.execute("""
                SELECT * from favorite_artists where user_id=%s and artist_id=%s
            """, (current_user.id,artist_id))
            is_favorite=cursor.fetchone() is not None
        else:
            is_favorite=False
    if not artist_rows:
        return "Artist not found", 404
    
    artist_data=artist_rows[0]


    releases = [
        {"title": row["release_title"],"release_id":row["release_id"], "date": row["release_date"].strftime("%Y-%m-%d")}
        for row in artist_rows
        if row["release_id"]
    ]

    artist_dict={

        "id": artist_data['artist_id'],
        "name": artist_data['artist_name'],
        "releases":releases
    }
    return render_template("artist.html", artist=artist_dict,is_favorite=is_favorite)



@artist_bp.route('/add_favorite',methods=['POST'])
@login_required
def add_favorite():
    artist_id=request.form.get('artist_id')

    if not artist_id:
        flash('Geçerli bir sanatçı seçilmedi.','danger')
        return redirect(url_for('main_bp.home'))
    
    try:
        with get_db_connection_and_cursor() as (conn, cursor):
            cursor.execute("""
                SELECT * from favorite_artists WHERE user_id= %s AND artist_id= %s
            """, (current_user.id,artist_id))
        
            existing_favorite=cursor.fetchone()
            if existing_favorite:
                flash('Bu sanatçı zaten favorilerinde','info')
                return redirect(request.referrer or url_for('main_bp.home'))

            
            cursor.execute("""
                INSERT INTO favorite_artists (user_id,artist_id) VALUES (%s,%s)
            """,(current_user.id,artist_id))
            conn.commit()
            flash('Sanatçı favorilere eklendi','success')
            return redirect(request.referrer or url_for('main_bp.home'))

    
    except Exception as e:
        flash(f'Favorilere eklerken bir hata oluştu: {str(e)}','danger')

    return json.dumps({'success': True}),200 ,{'ContentType': 'application/json'}

@artist_bp.route('/remove_favorite', methods=['POST'])
@login_required
def remove_favorite():
    artist_id = request.form.get('artist_id')
    
    if not artist_id:
        flash('Geçerli bir sanatçı seçilmedi.', 'danger')
        return redirect(url_for('main_bp.home'))

    try:
        with get_db_connection_and_cursor() as (conn, cursor):
            cursor.execute("""
                SELECT * FROM favorite_artists WHERE user_id = %s AND artist_id = %s
            """, (current_user.id, artist_id))
            
            existing_favorite = cursor.fetchone()
            if not existing_favorite:
                flash('Bu sanatçı favorilerde bulunamadı.', 'info')
                return redirect(request.referrer or url_for('main_bp.home'))

            cursor.execute("""
                DELETE FROM favorite_artists WHERE user_id = %s AND artist_id = %s
            """, (current_user.id, artist_id))
            conn.commit()
            flash('Sanatçı favorilerden kaldırıldı!', 'success')
            return redirect(request.referrer or url_for('main_bp.home'))

    except Exception as e:
        flash(f'Favorilerden kaldırırken bir hata oluştu: {str(e)}', 'danger')
        return redirect(url_for('main_bp.home'))
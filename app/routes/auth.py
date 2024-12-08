from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from app.utils.db_connection import get_db_connection_and_cursor
from app.models.models import User  # User modelini tanımlayacağız
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with get_db_connection_and_cursor() as (conn, cursor):
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                user_data = cursor.fetchone()
        except Exception as e:
            flash('Veritabanı hatası: ' + str(e), 'danger')
            return render_template('login.html')
        if user_data and check_password_hash(user_data['password'], password):
            user = User(user_data)
            login_user(user)
            flash('Giriş başarılı!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main_bp.home'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('main_bp.home'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.home'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Şifreyi hashleyelim
        hashed_password = generate_password_hash(password, method='sha256')
        try:
            with get_db_connection_and_cursor() as (conn, cursor):
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
                conn.commit()
                flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
                return redirect(url_for('auth_bp.login'))
        except Exception as e:
            conn.rollback()
            flash('Kayıt sırasında bir hata oluştu.', 'danger')
    return render_template('register.html')

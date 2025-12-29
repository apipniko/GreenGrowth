from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from greengrowth_project.models.user import get_account_user, add_account_user
from greengrowth_project.models.admin import get_account_admin, get_program_by_admin

# Membuat Blueprint untuk auth
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Logic login
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Validasi data
        akun_user = get_account_user(email)
        akun_admin = get_account_admin(email)
        
        # Cek akun user
        if akun_user is not None and check_password_hash(akun_user[4], password):
            session['logged_in'] = True
            session['user_id'] = akun_user[0]
            session['user_name'] = akun_user[1]
            session['user_role'] = akun_user[3]
            session['profile_image'] = akun_user[5]
            session['role'] = 'user'
            flash(f'Selamat datang {akun_user[1]}!👋', 'success')
            return redirect(url_for('user.dashboard'))
        # Cek akun admin
        elif akun_admin is not None and check_password_hash(akun_admin[4], password):
            session['logged_in'] = True
            session['admin_id'] = akun_admin[0]
            session['admin_role'] = akun_admin[3]
            session['role'] = 'admin'
            # Ambil program_id yang terhubung dengan admin
            program = get_program_by_admin(akun_admin[0])
            if program:
                session['program_id'] = program[0]
            flash(f"Halo Admin {akun_admin[1]}, selamat bekerja!", "success")
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Login gagal, email atau password anda salah!','error')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Logic register
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        password = request.form['password']
        conf_password = request.form['conf_password']
        # Kondisi konfirmasi password
        if password != conf_password:
            flash('Password yang anda masukan tidak sesuai, silahkan coba lagi!','error')
            return redirect(url_for('auth.register'))
        # Mengecek apakah email sudah digunakan?
        user = get_account_user(email)
        if user:
            flash("Email sudah digunakan!", "error")
            return render_template('auth/register.html')
        # Proses menambahkan akun baru
        add_account_user(nama,email,password)
        flash("Berhasil untuk mendaftar akun!", "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sampai jumpa lagi! 👋', 'info')
    return redirect(url_for('home'))

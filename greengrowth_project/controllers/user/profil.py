from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import os

profil_bp = Blueprint('profil', __name__, url_prefix='/profil')

# ================= CONFIG UPLOAD =================
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = os.path.join('static', 'uploads')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ================= ROUTES =================

@profil_bp.route('/')
def profile():
    """Tampilkan halaman profil user"""
    if 'user_id' not in session:
        flash("Silakan login dulu", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    
    # Ambil data user dari DB
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE user_id=%s", (user_id,))
    user = cur.fetchone()
    cur.close()

    # Ubah tuple menjadi dict agar mudah di template
    user_dict = {}
    if user:
        user_dict = {
            'user_id': user[0],
            'nama_user': user[1],
            'email_user': user[2],
            'user_role': user[3],
            'password_user': user[4],
            'foto_user': user[5],
            'gender': user[6],
            'tanggal_lahir': user[7],
            'pendidikan_tertinggi': user[8],
            'softskill': user[9],
            'hardskill': user[10],
            'pengalaman': user[11],
            'no_hp': user[12],
            'alamat': user[13],
            'created_at': user[14]
        }

    return render_template('user/profil.html', user=user_dict)


@profil_bp.route('/update', methods=['POST'])
def update_profile():
    """Update profil user"""
    if 'user_id' not in session:
        flash("User tidak login", "error")
        return redirect(url_for('auth.login'))

    user_id = session['user_id']

    # Ambil data dari form
    nama_user = request.form.get('nama_user')
    gender = request.form.get('gender')
    tanggal_lahir = request.form.get('tanggal_lahir')
    pendidikan_tertinggi = request.form.get('pendidikan_tertinggi')
    softskill = request.form.get('softskill')
    hardskill = request.form.get('hardskill')
    pengalaman = request.form.get('pengalaman')
    no_hp = request.form.get('no_hp')
    alamat = request.form.get('alamat')
    foto_file = request.files.get('foto_user')

    # Upload foto jika ada
    foto_filename = None
    if foto_file and allowed_file(foto_file.filename):
        filename = secure_filename(foto_file.filename)
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        foto_path = os.path.join(UPLOAD_FOLDER, filename)
        foto_file.save(foto_path)
        foto_filename = foto_path.replace("\\", "/")  # agar path valid di HTML

    # Update database
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        if foto_filename:
            cur.execute("""
                UPDATE users
                SET nama_user=%s, gender=%s, tanggal_lahir=%s, pendidikan_tertinggi=%s,
                    softskill=%s, hardskill=%s, pengalaman=%s, no_hp=%s, alamat=%s, foto_user=%s
                WHERE user_id=%s
            """, (nama_user, gender, tanggal_lahir, pendidikan_tertinggi,
                  softskill, hardskill, pengalaman, no_hp, alamat, foto_filename, user_id))
        else:
            cur.execute("""
                UPDATE users
                SET nama_user=%s, gender=%s, tanggal_lahir=%s, pendidikan_tertinggi=%s,
                    softskill=%s, hardskill=%s, pengalaman=%s, no_hp=%s, alamat=%s
                WHERE user_id=%s
            """, (nama_user, gender, tanggal_lahir, pendidikan_tertinggi,
                  softskill, hardskill, pengalaman, no_hp, alamat, user_id))

        mysql.connection.commit()
        cur.close()
        flash("Data berhasil disimpan!", "success")
        return redirect(url_for('profil.profile'))

    except Exception as e:
        flash(f"Tolong isikan {str(e)} terlebih dahulu", "error")
        return redirect(url_for('profil.profile'))

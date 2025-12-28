from flask import Blueprint, render_template, request, redirect, url_for, Response, flash, session, abort, current_app
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.utils import secure_filename
from greengrowth_project.models.laporan import createLaporan_db, readLaporan_db, readLaporan_by_id,updateLaporan_db, deleteLaporan_db
from greengrowth_project.models.program_admin import readProgram_by_admin, get_program_by_id
laporan_bp = Blueprint('laporan', __name__, url_prefix='/laporan')

def allowed_file(filename):
    if not filename:
        return False
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png','jpg','jpeg','gif'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed

def save_upload(file_storage):
    """Save uploaded file and return relative static path like 'uploads/xxx.jpg'"""
    if not file_storage or file_storage.filename == '':
        return None
    if not allowed_file(file_storage.filename):
        return None
    filename = secure_filename(file_storage.filename)
    unique = f"{uuid.uuid4().hex}_{filename}"
    upload_folder = os.path.join(current_app.root_path, current_app.config.get('UPLOAD_FOLDER', 'static/uploads'))
    os.makedirs(upload_folder, exist_ok=True)
    dest = os.path.join(upload_folder, unique)
    file_storage.save(dest)
    # Return relative path under static
    rel = os.path.join('uploads', unique).replace('\\', '/')
    return rel

@laporan_bp.route('/create_laporan', methods=['GET', 'POST'])
def create_laporan():
    # Memriksa apakah request sama dengan POST
    if request.method == 'POST':
        if 'logged_in' not in session:
            flash("Anda harus login sebagai admin terlebih dahulu")
            return redirect(url_for('auth.login'))
        # Mengambil program_id dari form dropdown program
        try:
            program_id = request.form.get('program_id')
        except:
            flash("Program tidak valid!")
            return redirect(url_for('auth.login'))
        # Handle Upload
        foto_laporan = request.files.get('foto_laporan')
        foto_rel = None
        if not foto_laporan or foto_laporan.filename == '':
            flash('Foto laporan harus diunggah!', 'error')
            admin_id = session.get('admin_id')
            programs = readProgram_by_admin(admin_id)
            return render_template('admin/laporan/create.html', programs=programs, selected_program_id=program_id)
        foto_rel = save_upload(foto_laporan)
        if foto_rel is None:
            flash('Format file tidak diizinkan.', 'error')
            admin_id = session.get('admin_id')
            programs = readProgram_by_admin(admin_id)
            return render_template('admin/laporan/create.html', programs=programs, selected_program_id=program_id)
        laporan_tanggal = request.form.get('tanggal_laporan')
        laporan_persentase_progres = request.form.get('laporan_persentase_progres')
        laporan_output_ekonomi = request.form.get('laporan_output_ekonomi')
        # Memanggil model createLaporan_db
        result = createLaporan_db(program_id,foto_rel,laporan_tanggal,laporan_persentase_progres,laporan_output_ekonomi)
        if result:
            flash('Laporan berhasil ditambahkan!', 'success')
            return redirect(url_for('laporan.create_laporan'))
        else:
            flash('Gagal menambahkan laporan!', 'error')
            admin_id = session.get('admin_id')
            programs = readProgram_by_admin(admin_id)
            return render_template('admin/laporan/create.html', programs=programs, selected_program_id=program_id)
    # GET request untuk menampilkan data program pada dropdown
    admin_id = session.get('admin_id')
    program_id = request.args.get('program_id','')
    programs = readProgram_by_admin(admin_id)
    return render_template('admin/laporan/create.html',programs=programs,selected_program_id=program_id)

@laporan_bp.route('/read_laporan', methods=['GET', 'POST'])
def read_laporan():
    # Memeriksa apakah session ada
    if 'logged_in' not in session:
        flash("Anda harus login!")
        return redirect(url_for('auth.login'))
    admin_id = session.get('admin_id')
    # Memanggil query untuk menampilkan seluruh laporan
    laporan_list = readLaporan_db()
    return render_template('admin/laporan/list.html', laporan=laporan_list )

@laporan_bp.route('/update_laporan/<int:laporan_id>', methods=['GET', 'POST'])
def update_laporan(laporan_id):
    # Periksa session
    if 'logged_in' not in session:
        flash("Anda harus login terlebih dahulu!")
        return redirect(url_for('auth.login'))
    # GET: render form
    if request.method == 'GET':
        admin_id = session.get('admin_id')
        programs = readProgram_by_admin(admin_id)
        laporan = readLaporan_by_id(laporan_id)
        return render_template('admin/laporan/update.html', programs=programs, laporan_id=laporan_id, laporan=laporan)
    # POST: process update
    program_id = request.form.get('program_id')
    foto_file = request.files.get('foto_laporan')
    laporan_tanggal = request.form.get('tanggal_laporan')
    laporan_persentase_progres = request.form.get('laporan_persentase_progres')
    laporan_output_ekonomi = request.form.get('laporan_output_ekonomi')
    # get existing laporan to preserve foto if not replaced
    existing = readLaporan_by_id(laporan_id)
    # Ambil path file foto jika data laporan ada dan field foto tersedia
    foto_rel = None
    if existing and len(existing) >= 3:
        foto_rel = existing[2]
    # If new file uploaded, save and replace
    if foto_file and foto_file.filename:
        new_rel = save_upload(foto_file)
        if new_rel is None:
            flash('Format file tidak diizinkan.', 'error')
            admin_id = session.get('admin_id')
            programs = readProgram_by_admin(admin_id)
            laporan = readLaporan_by_id(laporan_id)
            return render_template('admin/laporan/update.html', programs=programs, laporan_id=laporan_id, laporan=laporan)
        foto_rel = new_rel
    # Call model update
    ok = updateLaporan_db(program_id, foto_rel, laporan_tanggal, laporan_persentase_progres, laporan_output_ekonomi, laporan_id)
    if ok:
        flash('Laporan berhasil diperbarui!', 'success')
    else:
        flash('Gagal memperbarui laporan.', 'error')

    return redirect(url_for('laporan.read_laporan'))


@laporan_bp.route('/delete_laporan/<int:laporan_id>', methods=['POST'])
def delete_laporan(laporan_id):
    # Periksa session
    if 'logged_in' not in session:
        flash("Anda harus login terlebih dahulu!")
        return redirect(url_for('auth.login'))
    # Ambil data laporan untuk menghapus file jika ada
    laporan = readLaporan_by_id(laporan_id)
    # Ambil path file foto jika data laporan ada dan field foto tersedia
    foto_rel = None
    if laporan and len(laporan) >= 3:
        foto_rel = laporan[2]
    # Hapus record dari database
    ok = deleteLaporan_db(laporan_id)
    # Jika ada file yang diupload, coba hapus dari disk
    if ok and foto_rel:
        try:
            static_path = os.path.join(current_app.root_path, 'static', foto_rel.replace('/', os.path.sep))
            if os.path.exists(static_path):
                os.remove(static_path)
        except Exception:
            pass
    if ok:
        flash('Laporan berhasil dihapus.', 'success')
    else:
        flash('Gagal menghapus laporan.', 'error')
    return redirect(url_for('laporan.read_laporan'))



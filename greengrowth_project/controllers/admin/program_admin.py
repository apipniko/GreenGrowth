from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from greengrowth_project.models.program_admin import createProgram_db, readProgram_by_admin, readProgram_by_id, updateProgram_db, deleteProgram_db

program_bp = Blueprint('program', __name__, url_prefix='/program')

ALLOWED_STATUS = {'perencanaan', 'berjalan', 'selesai'}


@program_bp.route('/list', methods=['GET'])
def list_program():
    # List semua program milik admin
    if 'logged_in' not in session or 'admin_id' not in session:
        flash("Anda harus login sebagai admin!")
        return redirect(url_for('auth.login'))
    admin_id = session['admin_id']
    programs = readProgram_by_admin(admin_id)
    return render_template('admin/program/list.html', programs=programs)


@program_bp.route('/create', methods=['GET', 'POST'])
def create_program():
    # Form dan submit buat program
    if 'logged_in' not in session or 'admin_id' not in session:
        flash("Anda harus login sebagai admin!")
        return redirect(url_for('auth.login'))
    if request.method == "POST":
        admin_id = session['admin_id']
        # Ambil data dari form
        nama_program = request.form.get('nama_program', '').strip()
        if not nama_program:
            flash("Nama program harus diisi!")
            return redirect(url_for('program.create_program'))
        sektor_program = request.form.get('sektor_program', '')
        tujuan_program = request.form.get('tujuan_program', '')
        lokasi_program = request.form.get('lokasi_program', '')
        status_program = request.form.get('status_program', 'perencanaan')
        deskripsi_program = request.form.get('deskripsi_program', '')
        # Validasi status
        if status_program not in ALLOWED_STATUS:
            status_program = 'perencanaan'
        # Insert ke database
        result = createProgram_db(admin_id, nama_program, sektor_program, tujuan_program, 
                                 lokasi_program, status_program, deskripsi_program)
        # Validasi untuk memeriksa query dalam veriabel result apakah berhasil atau tidak?
        return redirect(url_for('program.create_program'))
    return render_template('admin/program/create.html')


@program_bp.route('/edit/<int:program_id>', methods=['GET', 'POST'])
def edit_program(program_id):
    # Form dan submit edit program"
    if 'logged_in' not in session or 'admin_id' not in session:
        flash("Anda harus login sebagai admin!")
        return redirect(url_for('auth.login'))
    admin_id = session['admin_id']
    program = readProgram_by_id(program_id)
    # Validasi program milik admin ini
    if not program or program[7] != admin_id:  # program[7] = admin_id
        flash("Program tidak ditemukan atau Anda tidak punya akses!")
        return redirect(url_for('program.list_program'))
    
    if request.method == "POST":
        # Ambil data dari form
        nama_program = request.form.get('nama_program', '').strip()
        if not nama_program:
            flash("Nama program harus diisi!")
            return redirect(url_for('program.edit_program', program_id=program_id))
        sektor_program = request.form.get('sektor_program', '')
        tujuan_program = request.form.get('tujuan_program', '')
        lokasi_program = request.form.get('lokasi_program', '')
        status_program = request.form.get('status_program', 'perencanaan')
        deskripsi_program = request.form.get('deskripsi_program', '')
        # Validasi status
        if status_program not in ALLOWED_STATUS:
            status_program = 'perencanaan'
        # Update database
        result = updateProgram_db(program_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program)
        # Validasi untuk memeriksa query dalam variabel result, apakah berhasil atau tidak
        if result:
            flash("Program berhasil diupdate!")
            return redirect(url_for('program.list_program'))
        else:
            flash("Gagal update program!")
            return redirect(url_for('program.edit_program', program_id=program_id))
    
    return render_template('admin/program/edit.html', program=program)


@program_bp.route('/delete/<int:program_id>', methods=['POST'])
def delete_program(program_id):
    # Hapus program"
    if 'logged_in' not in session or 'admin_id' not in session:
        flash("Anda harus login sebagai admin!")
        return redirect(url_for('auth.login'))
    admin_id = session['admin_id']
    program = readProgram_by_id(program_id)
    # Validasi program milik admin ini
    if not program or program[7] != admin_id:  # program[7] = admin_id
        flash("Program tidak ditemukan atau Anda tidak punya akses!")
        return redirect(url_for('program.list_program'))
    result = deleteProgram_db(program_id)
     # Validasi untuk memeriksa query dalam variabel result, apakah berhasil atau tidak
    if result:
        flash("Program berhasil dihapus!")
    else:
        flash("Gagal menghapus program!")
    
    return redirect(url_for('program.list_program'))


from flask import Blueprint, render_template, request, redirect, url_for, Response, flash, session
from greengrowth_project.models.lowongan import createLowongan_db, readLowongan_db, updateLowongan_db, readLowongan_by_id,deleteLowongan_db
from greengrowth_project.models.admin import get_all_programs_by_admin
lowongan_bp = Blueprint('lowongan', __name__, url_prefix='/lowongan')

ALLOWED_STATUS = {'dibuka', 'ditutup'}

@lowongan_bp.route('/create_lowongan', methods=['GET', 'POST'])
def create_lowongan():
    if request.method == "POST":
    # Memeriksa apakah session ada
        if 'logged_in' not in session:
            flash("Anda harus login sebagai admin!")
            return redirect(url_for('auth.login'))
        # Mengambil program_id dari form dropdown program
        try:
            program_id = request.form.get('program_id')
        except ValueError:
            flash("Program tidak valid!")
            return redirect(url_for('lowongan.create_lowongan'))
        # Mengambil data yang diinputkan pada form
        nama_lowongan = request.form.get('nama_lowongan', '')
        status_lowongan = request.form.get('status_lowongan', 'dibuka')
        if status_lowongan not in ALLOWED_STATUS:
            status_lowongan = "dibuka"
        # Validasi input angka
        min_umur = request.form.get('min_umur', 0)
        max_umur = request.form.get('max_umur', 0)
        kuota_pekerja = request.form.get('kuota_pekerja', 0)
        keahlian = request.form.get('keahlian', '')
        pengalaman = request.form.get('pengalaman', '')
        min_pendidikan = request.form.get('min_pendidikan', '')
        # Memanggil model create_lowongan
        createLowongan_db(program_id, nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja)
        return redirect(url_for('lowongan.read_lowongan', program_id=program_id))
    # GET request - tampil form, untuk menampilkan dropdown
    admin_id = session.get('admin_id') #Ambil ID admin yang sedang login dari session
    print(f"DEBUG create_lowongan GET: admin_id={admin_id}")
    programs = get_all_programs_by_admin(admin_id) # Ambil semua program milik admin dari database (untuk dropdown di form)
    print(f"DEBUG create_lowongan: programs={programs}")
    program_id = request.args.get('program_id', '') #A mbil program_id dari URL query parameter (jika ada)
    return render_template('admin/kelola_lowongan/create_lowongan.html', programs=programs, selected_program_id=program_id)

@lowongan_bp.route('/edit_lowongan/<int:lowongan_id>', methods=['GET', 'POST'])
def edit_lowongan(lowongan_id):
    if request.method == "POST":
        # Memeriksa apakah session ada
        if 'logged_in' not in session:
            flash("Anda harus login terlebih dahulu")
            return redirect(url_for('auth.login'))
        # Mengambil data yang diinputkan pada form
        program_id = request.form.get('program_id')
        nama_lowongan = request.form.get('judul_lowongan')
        status_lowongan = request.form.get('status_lowongan', 'dibuka')
        if status_lowongan not in ALLOWED_STATUS:
            status_lowongan = "dibuka"
        min_umur = request.form.get('min_umur', 0)
        max_umur = request.form.get('max_umur', 0)
        kuota_pekerja = request.form.get('kuota_pekerja', 0)
        keahlian = request.form.get('keahlian', '')
        pengalaman = request.form.get('pengalaman', '')
        min_pendidikan = request.form.get('min_pendidikan', '')
        # Memanggil fungsi query untuk update lowongan
        updateLowongan_db(lowongan_id, program_id, nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja)
        # Jika sudah selesai, alihkan ke read_lowongan
        return redirect(url_for('lowongan.read_lowongan', program_id=program_id))
     # GET request - tampil form, untuk menampilkan dropdown dan data lowongan
    admin_id = session.get('admin_id')
    programs = get_all_programs_by_admin(admin_id)
    lowongan = readLowongan_by_id(lowongan_id)
    return render_template('admin/kelola_lowongan/update_lowongan.html', 
                          programs=programs, 
                          lowongan_id=lowongan_id,
                          lowongan=lowongan)

@lowongan_bp.route('/read_lowongan', methods=['GET', 'POST'])
def read_lowongan():
    # Memeriksa apakah session ada
    if 'logged_in' not in session:
        flash("Anda harus login!")
        return redirect(url_for('auth.login'))
    admin_id = session.get('admin_id')
    print(f"DEBUG read_lowongan: admin_id={admin_id}")
    # Ambil semua program milik admin
    programs = get_all_programs_by_admin(admin_id)
    print(f"DEBUG read_lowongan: programs={programs}")
    # Ambil program_id dari request args atau session
    program_id = request.args.get('program_id') or session.get('program_id')
    # Validasi program_id ada di program milik admin
    program_ids = [str(p[0]) for p in programs]
    if str(program_id) not in program_ids and programs:
        program_id = str(programs[0][0])  # Gunakan program pertama
    else:
        program_id = str(program_id) if program_id else None
    
    lowongan_data = readLowongan_db(program_id)
    return render_template('admin/kelola_lowongan/read_lowongan.html', 
                         lowongan=lowongan_data, 
                         programs=programs, 
                         selected_program_id=program_id )

@lowongan_bp.route('/delete_lowongan/<int:lowongan_id>', methods=['POST'])
def delete_lowongan(lowongan_id):
    if 'logged_in' not in session:
        flash("Silahkan login terlebih dahulu")
        return redirect(url_for('auth.login'))
    admin_id =session.get('admin_id')
    lowongan = readLowongan_by_id(lowongan_id)
    # Validasi ketersediaan lowongan
    if not lowongan:
        return redirect(url_for('lowongan.read_lowongan'))
    program_id = lowongan[1] #Untuk mengambil program_id dari lowongan
    # Validasi apakah program benar-benar milik admin
    admin_program = get_all_programs_by_admin(admin_id)
    if not any(p[0]==program_id for p in admin_program):
        flash("Anda tidak mempunyai akses untuk menghapus lowongan ini")
        return redirect(url_for('lowongan.read_lowongan'))
    # Hapus lowongan
    deleteLowongan_db(lowongan_id)
    return redirect(url_for('lowongan.read_lowongan', program_id = program_id))
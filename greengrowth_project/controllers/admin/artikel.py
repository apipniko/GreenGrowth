from flask import Blueprint, render_template, request, redirect, url_for, Response, flash, session, abort, current_app
import os
import uuid
from werkzeug.utils import secure_filename
from greengrowth_project.models.artikel import (
    createArtikel_db,
    get_all_artikels,
    get_artikel_by_id,
    edit_artikel_by_id,
    delete_artikel_by_id,
)
from greengrowth_project.models.program import get_all_programs, get_program_by_id

artikel_bp = Blueprint('artikel', __name__, url_prefix='/admin/artikel')


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


@artikel_bp.route('/', methods=['GET'])
def index():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    artikels = get_all_artikels()
    return render_template('admin/artikel.html', artikels=artikels)


@artikel_bp.route('/create', methods=['GET', 'POST'])
def create():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    programs = get_all_programs()
    if request.method == 'POST':
        judul_artikel = request.form.get('judul_artikel')
        deskripsi = request.form.get('deskripsi')
        program_id = request.form.get('program_id')
        # validate program_id
        if not program_id or not get_program_by_id(program_id):
            flash('Program yang dipilih tidak valid.', 'error')
            return render_template('admin/artikel_admin.html', programs=programs, form=request.form)

        # handle upload
        file = request.files.get('foto_artikel')
        foto_rel = None
        if file and file.filename:
            foto_rel = save_upload(file)
            if foto_rel is None:
                flash('Format file tidak diizinkan.', 'error')
                return render_template('admin/artikel_admin.html', programs=programs, form=request.form)

        admin_id = session.get('admin_id') or None
        createArtikel_db(judul_artikel, deskripsi, foto_rel, program_id, admin_id)
        flash('Artikel berhasil dibuat.', 'success')
        return redirect(url_for('artikel.index'))
    return render_template('admin/artikel_admin.html', programs=programs)


@artikel_bp.route('/<int:artikel_id>')
def show(artikel_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    artikel = get_artikel_by_id(artikel_id)
    if not artikel:
        abort(404)
    return render_template('admin/artikel_show.html', artikel=artikel)


@artikel_bp.route('/<int:artikel_id>/edit', methods=['GET', 'POST'])
def edit(artikel_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    artikel = get_artikel_by_id(artikel_id)
    if not artikel:
        abort(404)
    programs = get_all_programs()
    if request.method == 'POST':
        try:
            new_judul = request.form.get('judul_artikel')
            new_deskripsi = request.form.get('deskripsi')
            program_id = request.form.get('program_id')
            
            # Convert program_id to int and validate
            if program_id:
                try:
                    program_id = int(program_id)
                except (ValueError, TypeError):
                    flash('Program ID tidak valid.', 'error')
                    return render_template('admin/artikel_edit.html', artikel=artikel, programs=programs)
                
                if not get_program_by_id(program_id):
                    flash('Program yang dipilih tidak ditemukan.', 'error')
                    return render_template('admin/artikel_edit.html', artikel=artikel, programs=programs)
            else:
                program_id = None

            # handle upload (optional)
            file = request.files.get('foto_artikel')
            new_foto_rel = None
            if file and file.filename:
                new_foto_rel = save_upload(file)
                if new_foto_rel is None:
                    flash('Format file tidak diizinkan.', 'error')
                    return render_template('admin/artikel_edit.html', artikel=artikel, programs=programs)
                # delete old file if exists
                if artikel.get('foto_artikel'):
                    old_full = os.path.join(current_app.root_path, 'static', artikel.get('foto_artikel'))
                    try:
                        if os.path.exists(old_full):
                            os.remove(old_full)
                    except Exception:
                        pass

            edit_artikel_by_id(artikel_id, new_judul, new_deskripsi, new_foto_rel or None, program_id)
            flash('Artikel diperbarui.', 'success')
            return redirect(url_for('artikel.show', artikel_id=artikel_id))
        except ValueError as ve:
            # Handle invalid program ID
            flash(f'Error: {str(ve)}', 'error')
            return render_template('admin/artikel_edit.html', artikel=artikel, programs=programs)
        except Exception as e:
            # Handle database/constraint errors
            flash('Gagal memperbarui artikel. Program mungkin sudah dihapus. Silakan pilih program lain.', 'error')
            return render_template('admin/artikel_edit.html', artikel=artikel, programs=programs)
    return render_template('admin/artikel_edit.html', artikel=artikel, programs=programs)


@artikel_bp.route('/<int:artikel_id>/delete', methods=['POST'])
def delete(artikel_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    artikel = get_artikel_by_id(artikel_id)
    if artikel and artikel.get('foto_artikel'):
        old_full = os.path.join(current_app.root_path, 'static', artikel.get('foto_artikel'))
        try:
            if os.path.exists(old_full):
                os.remove(old_full)
        except Exception:
            pass
    delete_artikel_by_id(artikel_id)
    flash('Artikel dihapus.', 'success')
    return redirect(url_for('artikel.index'))

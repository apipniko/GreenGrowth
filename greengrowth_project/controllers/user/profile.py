from flask import Blueprint, render_template, request, redirect, url_for, Response, flash, session, abort, current_app
from greengrowth_project.models.user import get_user_profile, edit_profile_by_id
import os
import uuid
from werkzeug.utils import secure_filename

profile_user_bp = Blueprint('profile_user', __name__, url_prefix='/user/profile')


def allowed_file(filename):
    if not filename:
        return False
    allowed = current_app.config.get('ALLOWED_EXTENSIONS', {'png','jpg','jpeg','gif'})
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed


def save_upload(file_storage):
    """Save uploaded file and return relative static path like 'uploads/xxx.jpg' or None if invalid"""
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
    rel = os.path.join('uploads', unique).replace('\\', '/')
    return rel

@profile_user_bp.route('/<int:user_id>', methods=['GET'])
def view_profile(user_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    profile = get_user_profile(user_id)
    if not profile:
        abort(404)
    back_url = url_for('user.dashboard')

    return render_template(
        'user/profile.html',
        profile=profile,
        back_url=back_url
    )

@profile_user_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    profile = get_user_profile(user_id)
    if not profile:
        abort(404)
    if request.method == 'POST':
        nama_user = request.form.get('nama_user')
        email_user = request.form.get('email_user')
        foto_file = request.files.get('foto_user')
        gender = request.form.get('gender')
        tanggal_lahir = request.form.get('tanggal_lahir')
        pendidikan_tertinggi = request.form.get('pendidikan_tertinggi')
        softskill = request.form.get('softskill')
        hardskill = request.form.get('hardskill')
        pengalaman = request.form.get('pengalaman')
        no_hp = request.form.get('no_hp')
        alamat = request.form.get('alamat')

        # handle file upload: save to static/uploads and store the static URL (keep existing if not replaced)
        foto_url = profile.get('foto_user')
        if foto_file and getattr(foto_file, 'filename', None):
            new_rel = save_upload(foto_file)
            if new_rel is None:
                flash('Format file tidak diizinkan atau tidak ada file yang dipilih.', 'error')
                return render_template('user/profile_edit.html', profile=profile)
            # Remove old local file if any
            try:
                old_rel = foto_url
                if old_rel:
                    if old_rel.startswith('/static/'):
                        old_rel = old_rel[len('/static/'):]
                    if old_rel.startswith('uploads/'):
                        old_path = os.path.join(current_app.root_path, 'static', old_rel.replace('/', os.path.sep))
                        if os.path.exists(old_path):
                            os.remove(old_path)
            except Exception:
                pass
            # store the static URL into DB so templates that use it directly work
            foto_url = url_for('static', filename=new_rel)
        edit_profile_by_id(user_id, nama_user, email_user, foto_url, gender, tanggal_lahir, pendidikan_tertinggi, softskill, hardskill, pengalaman, no_hp, alamat)
        flash('Profil berhasil diperbarui.', 'success')
        return redirect(url_for('profile_user.view_profile', user_id=user_id))
    return render_template('user/profile_edit.html', profile=profile)


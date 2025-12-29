from flask import Blueprint, render_template, request, redirect, url_for, Response, flash, session, abort, current_app
from greengrowth_project.models.user import get_user_profile, edit_profile_by_id
import os
import re
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

@profile_user_bp.route('/<int:user_id>', methods=['GET', 'POST'])
def view_profile(user_id):
    current_app.logger.info(f"view_profile called with path={request.path} args={dict(request.args)} method={request.method}")
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    profile = get_user_profile(user_id)
    if not profile:
        abort(404)

    raw_next = request.args.get('next') or request.form.get('next')
    next_url = raw_next if raw_next and raw_next.startswith('/') else None
    back_url = next_url or url_for('user.dashboard')
    errors = {}
    form_data = None

    if request.method == 'POST':
        form_data = request.form
        nama_user = request.form.get('nama_user', '').strip()
        email_user = request.form.get('email_user', '').strip()
        foto_file = request.files.get('foto_user')
        gender = request.form.get('gender', '').strip()
        tanggal_lahir = request.form.get('tanggal_lahir', '').strip()
        pendidikan_tertinggi = request.form.get('pendidikan_tertinggi', '').strip()
        softskill = request.form.get('softskill', '').strip()
        hardskill = request.form.get('hardskill', '').strip()
        pengalaman = request.form.get('pengalaman', '').strip()
        no_hp = request.form.get('no_hp', '').strip()
        alamat = request.form.get('alamat', '').strip()

        if not nama_user:
            errors['nama_user'] = 'Nama wajib diisi.'
        if not email_user or not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email_user):
            errors['email_user'] = 'Email tidak valid.'
        if gender and gender not in {'male', 'female'}:
            errors['gender'] = 'Pilihan jenis kelamin tidak valid.'
        if no_hp and not re.match(r'^[0-9+\-\s]{9,15}$', no_hp):
            errors['no_hp'] = 'No HP harus 9-15 digit dan hanya angka/tanda + - spasi.'

        foto_url = profile.get('foto_user')
        if foto_file and getattr(foto_file, 'filename', None):
            new_rel = save_upload(foto_file)
            if not new_rel:
                errors['foto_user'] = 'Format file foto tidak diizinkan (png/jpg/jpeg/gif).'
            else:
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
                foto_url = url_for('static', filename=new_rel)

        if errors:
            flash('Periksa kembali data yang belum valid.', 'error')
        else:
            # Map form values ('male'/'female') to DB enum values ('Laki-laki','Perempuan') or None
            db_gender = None
            if gender == 'male':
                db_gender = 'Laki-laki'
            elif gender == 'female':
                db_gender = 'Perempuan'

            edit_profile_by_id(
                user_id,
                nama_user,
                email_user,
                foto_url,
                db_gender,
                tanggal_lahir,
                pendidikan_tertinggi,
                softskill,
                hardskill,
                pengalaman,
                no_hp,
                alamat,
            )
            flash('Profil berhasil diperbarui.', 'success')
            if next_url:
                return redirect(next_url)
            profile = get_user_profile(user_id)
            # update session so navbar shows latest photo immediately
            session['profile_image'] = profile.get('foto_user')
            form_data = None

    return render_template(
        'user/profile.html',
        profile=profile,
        back_url=back_url,
        errors=errors,
        form_data=form_data,
        next_url=next_url,
    )


@profile_user_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_profile(user_id):
    current_app.logger.info(f"edit_profile called with path={request.path} args={dict(request.args)} method={request.method}")
    # Render a dedicated edit page on GET, and delegate POST to the existing view_profile handler
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    profile = get_user_profile(user_id)
    if not profile:
        abort(404)

    if request.method == 'POST':
        # reuse existing POST handling (validation + save) implemented in view_profile
        return view_profile(user_id)

    # GET: show the edit form
    return render_template('user/profile_edit.html', profile=profile, back_url=url_for('profile_user.view_profile', user_id=user_id))
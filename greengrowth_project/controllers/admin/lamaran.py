from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from greengrowth_project.models.lamaran import get_all_lamaran_by_admin, update_lamaran_status

lamaran_admin_bp = Blueprint('lamaran_admin', __name__, url_prefix='/admin/lamaran')


@lamaran_admin_bp.route('/list', methods=['GET'])
def list_lamaran():
    if 'logged_in' not in session or 'admin_id' not in session:
        flash('Anda harus login sebagai admin!')
        return redirect(url_for('auth.login'))

    admin_id = session['admin_id']
    lamaran_list = get_all_lamaran_by_admin(admin_id)
    return render_template('admin/monitoring_lamaran/lamaran.html', lamaran_list=lamaran_list)


@lamaran_admin_bp.route('/update_status/<int:lamaran_id>', methods=['POST'])
def update_status(lamaran_id):
    if 'logged_in' not in session or 'admin_id' not in session:
        flash('Anda harus login sebagai admin!')
        return redirect(url_for('auth.login'))

    new_status = request.form.get('status')
    if new_status not in {'diterima', 'ditolak', 'menunggu'}:
        flash('Status tidak valid.', 'error')
        return redirect(url_for('lamaran_admin.list_lamaran'))

    success = update_lamaran_status(lamaran_id, new_status)
    if success:
        flash('Status lamaran berhasil diupdate.', 'success')
    else:
        flash('Gagal mengupdate status lamaran.', 'error')

    return redirect(url_for('lamaran_admin.list_lamaran'))

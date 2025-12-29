from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from greengrowth_project.models.statistik import statistik_persentase_program_db, statistik_output_ekonomi_db
from greengrowth_project.models.program_admin import readProgram_by_id
from decimal import Decimal

statistik_bp = Blueprint('statistik', __name__, url_prefix='/statistik')


@statistik_bp.route('/program/<int:program_id>', methods=['GET'])
def statistik_persentase_program(program_id):
    # Memeriksa apakah session ada
    if 'logged_in' not in session:
        flash("Anda harus login!")
        return redirect(url_for('auth.login'))
    # Ambil data laporan untuk program tertentu
    statistik_list = statistik_persentase_program_db(program_id) or []
    # Siapkan labels dan data yang JSON-serializable
    labels = []
    data = []
    for row in statistik_list:
        # row expected: (program_id, nama_program, persentase, tanggal)
        try:
            t = row[3]
        except Exception:
            t = None
        try:
            v = row[2]
            # cast Decimal to float if necessary
            if isinstance(v, Decimal):
                v = float(v)
        except Exception:
            v = None
        labels.append(str(t) if t is not None else None)
        data.append(v)

    # Ambil info program (nama) jika ada
    program = None
    try:
        program = readProgram_by_id(program_id)
    except Exception:
        program = None
    return render_template('admin/statistik/statistik_program.html', statistik=statistik_list, program_id=program_id, labels=labels, data=data, program=program)


@statistik_bp.route('/program/output/<int:program_id>', methods=['GET'])
def statistik_output_ekonomi(program_id):
    # Memeriksa apakah session ada
    if 'logged_in' not in session:
        flash("Anda harus login!")
        return redirect(url_for('auth.login'))
    # Ambil data laporan output ekonomi untuk program tertentu
    statistik_list = statistik_output_ekonomi_db(program_id) or []
    # Siapkan labels dan data yang JSON-serializable (output ekonomi sebagai angka)
    labels = []
    data = []
    for row in statistik_list:
        # row expected: (program_id, nama_program, output_ekonomi, tanggal)
        try:
            t = row[3]
        except Exception:
            t = None
        try:
            v = row[2]
            if isinstance(v, Decimal):
                v = float(v)
        except Exception:
            v = None
        labels.append(str(t) if t is not None else None)
        data.append(v)
    # Ambil info program (nama) jika ada
    program = None
    try:
        program = readProgram_by_id(program_id)
    except Exception:
        program = None
    # Render using the ekonomi template (no chart removed there but table shown)
    return render_template('admin/statistik/statistik_output_ekonomi.html', statistik=statistik_list, program_id=program_id, labels=labels, data=data, program=program)


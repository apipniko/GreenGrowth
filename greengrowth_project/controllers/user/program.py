from flask import Blueprint, render_template, session, redirect, url_for, abort, request
from greengrowth_project.models.program import get_all_programs, get_program_by_id, get_all_program_sectors

program_user_bp = Blueprint('program_user', __name__, url_prefix='/user/program')

@program_user_bp.route('/', methods=['GET'])
def list_programs():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))

    selected_sector = request.args.get('sektor')
    q = request.args.get('q')
    if q is not None:
        q = q.strip() or None

    programs = get_all_programs(sektor=selected_sector, q=q)
    sectors = get_all_program_sectors()
    return render_template(
        'user/dashboard.html',
        programs=programs,
        sectors=sectors,
        selected_sector=selected_sector,
        q=q,
        result_count=len(programs),
    )

@program_user_bp.route('/<int:program_id>', methods=['GET'])
def show(program_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    program = get_program_by_id(program_id)
    if not program:
        abort(404)
    return render_template('user/program_show.html', program=program)
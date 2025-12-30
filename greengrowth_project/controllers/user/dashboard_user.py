from flask import Blueprint, render_template, session, redirect, url_for, request
from greengrowth_project.models.program import get_all_programs, get_all_program_sectors

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))

    selected_sector = request.args.get('sektor')

    q = request.args.get('q')
    if q is not None:
        q = q.strip() or None

    # Fetch programs from database
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
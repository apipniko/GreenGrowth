from flask import Blueprint, render_template, session, redirect, url_for, abort, request, jsonify
from greengrowth_project.models.lowongan import (
    readLowongan_db, 
    readLowongan_by_id, 
    get_all_lowongan_with_program,
    get_unique_locations,
    get_unique_education_levels
)

lowongan_user_bp = Blueprint('lowongan_user', __name__, url_prefix='/user/lowongan')

@lowongan_user_bp.route('/program/<int:program_id>', methods=['GET'])
def list_lowongan(program_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    lowongans = readLowongan_db(program_id)
    return render_template('user/lowongan.html', lowongans=lowongans, program_id=program_id) 

@lowongan_user_bp.route('/detail/<int:lowongan_id>', methods=['GET'])  
def show(lowongan_id):
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    lowongan = readLowongan_by_id(lowongan_id)
    if not lowongan:
        abort(404)
    return render_template('user/lowongan_show.html', lowongan=lowongan)

@lowongan_user_bp.route('/explore', methods=['GET', 'POST'])
def explore():
    """Explore page with filtering for lowongan"""
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    # Get filter options
    all_locations = get_unique_locations()
    all_education = get_unique_education_levels()
    
    # DEBUG: Print to console
    print(f"DEBUG - Locations: {all_locations}")
    print(f"DEBUG - Education: {all_education}")
    
    # Handle AJAX request for filtering
    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        lokasi_filter = data.get('lokasi', [])
        pendidikan_filter = data.get('pendidikan', [])
        
        # Get filtered lowongan
        lowongans = get_all_lowongan_with_program(
            lokasi_filter=lokasi_filter if lokasi_filter else None,
            pendidikan_filter=pendidikan_filter if pendidikan_filter else None
        )
        
        print(f"DEBUG - Filtered lowongans count: {len(lowongans)}")
        return jsonify({'lowongans': lowongans})
    
    # Initial page load
    lowongans = get_all_lowongan_with_program()
    print(f"DEBUG - Initial lowongans count: {len(lowongans)}")
    print(f"DEBUG - Lowongans data: {lowongans}")
    
    return render_template(
        'user/explore.html',
        lowongans=lowongans,
        all_locations=all_locations,
        all_education=all_education
    )
    
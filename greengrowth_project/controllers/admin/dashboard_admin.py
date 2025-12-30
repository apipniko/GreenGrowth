from flask import Blueprint, render_template, session, redirect, url_for

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'logged_in' not in session:
        return redirect(url_for('auth.login'))
    
    # Import mysql here to avoid circular import
    from greengrowth_project.app import mysql
    
    # Get statistics for dashboard
    stats = {
        'total_programs': 0,
        'active_vacancies': 0,
        'pending_applications': 0,
        'total_articles': 0
    }
    
    try:
        cursor = mysql.connection.cursor()
        
        # Get programs count
        cursor.execute("SELECT COUNT(*) as count FROM program")
        result = cursor.fetchone()
        stats['total_programs'] = result[0] if result else 0
        
        # Get active vacancies count
        cursor.execute("SELECT COUNT(*) as count FROM lowongan WHERE status = 'dibuka'")
        result = cursor.fetchone()
        stats['active_vacancies'] = result[0] if result else 0
        
        # Get pending applications count
        cursor.execute("SELECT COUNT(*) as count FROM lamaran WHERE status NOT IN ('diterima', 'ditolak')")
        result = cursor.fetchone()
        stats['pending_applications'] = result[0] if result else 0
        
        # Get total articles count
        cursor.execute("SELECT COUNT(*) as count FROM artikel")
        result = cursor.fetchone()
        stats['total_articles'] = result[0] if result else 0
        
        cursor.close()
    except Exception as e:
        print(f"Error fetching stats: {e}")
        # Use default values if there's an error
        pass
    
    return render_template('admin/dashboard.html', stats=stats)

  
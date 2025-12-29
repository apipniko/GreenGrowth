# Query untuk fitur Admin
def createLowongan_db(program_id,nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja):
    # Import MYSQL
    from greengrowth_project.app import mysql
    # Query untuk menambah data
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO lowongan(program_id, judul_lowongan, status_lowongan, lowongan_min_umur, lowongan_max_umur, lowongan_keahlian, lowongan_pengalaman, lowongan_min_pendidikan, kuota_pekerja) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)", (program_id, nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja,)
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error creating lowongan: {e}")
        return False
    
def readLowongan_db(program_id):
    # Import MySQL
    from greengrowth_project.app import mysql
    # Query untuk menampilkan seluruh data lowongan yang telah ditambah
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """SELECT 
                lowongan_id,
                program_id,
                judul_lowongan,
                status_lowongan,
                lowongan_min_umur,
                lowongan_max_umur,
                lowongan_keahlian,
                lowongan_pengalaman,
                lowongan_min_pendidikan,
                kuota_pekerja
            FROM lowongan 
            WHERE program_id=%s""", (program_id,)
        )
        rows = cur.fetchall()
        cur.close()
        
        # Convert to dictionary for easier template access
        lowongans = []
        for row in rows:
            lowongans.append({
                'id': row[0],
                'program_id': row[1],
                'judul': row[2],
                'status': row[3],
                'min_umur': row[4],
                'max_umur': row[5],
                'keahlian': row[6],
                'pengalaman': row[7],
                'min_pendidikan': row[8],
                'kuota': row[9]
            })
        return lowongans
    except Exception as e:
        print(f"Error reading lowongan: {e}")
        return []

def readLowongan_by_id(lowongan_id):
    # Get detail lowongan berdasarkan lowongan_id
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """SELECT 
                lowongan_id,
                program_id,
                judul_lowongan,
                status_lowongan,
                lowongan_min_umur,
                lowongan_max_umur,
                lowongan_keahlian,
                lowongan_pengalaman,
                lowongan_min_pendidikan,
                kuota_pekerja
            FROM lowongan 
            WHERE lowongan_id=%s""", (lowongan_id,)
        )
        row = cur.fetchone()
        cur.close()
        
        if not row:
            return None
            
        return {
            'id': row[0],
            'program_id': row[1],
            'judul': row[2],
            'status': row[3],
            'min_umur': row[4],
            'max_umur': row[5],
            'keahlian': row[6],
            'pengalaman': row[7],
            'min_pendidikan': row[8],
            'kuota': row[9]
        }
    except Exception as e:
        print(f"Error reading lowongan: {e}")
        return None

def updateLowongan_db(lowongan_id, program_id, nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja):
    # Update lowongan
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE lowongan SET 
            program_id=%s,
            judul_lowongan=%s,
            status_lowongan=%s,
            lowongan_min_umur=%s,
            lowongan_max_umur=%s,
            lowongan_keahlian=%s,
            lowongan_pengalaman=%s,
            lowongan_min_pendidikan=%s,
            kuota_pekerja=%s
            WHERE lowongan_id=%s
            """,
            (program_id, nama_lowongan, status_lowongan, min_umur, max_umur, keahlian, pengalaman, min_pendidikan, kuota_pekerja, lowongan_id)
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error updating lowongan: {e}")
        return False

def deleteLowongan_db(lowongan_id):
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            DELETE FROM lowongan WHERE lowongan_id=%s
            """,(lowongan_id,)
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error deleting lowongan {e}")
        return False


def get_all_lowongan_with_program(lokasi_filter=None, pendidikan_filter=None):
    """
    Get all lowongan with program info.
    Optionally filter by lokasi_program and lowongan_min_pendidikan.
    Returns list of lowongan with program details.
    """
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        
        # Base query with JOIN
        query = """
            SELECT 
                l.lowongan_id,
                l.program_id,
                l.judul_lowongan,
                l.status_lowongan,
                l.lowongan_min_umur,
                l.lowongan_max_umur,
                l.lowongan_keahlian,
                l.lowongan_pengalaman,
                l.lowongan_min_pendidikan,
                l.kuota_pekerja,
                p.nama_program,
                p.lokasi_program,
                p.sektor_program,
                p.deskripsi_program
            FROM lowongan l
            JOIN program p ON l.program_id = p.program_id
            WHERE l.status_lowongan = 'dibuka'
        """
        
        params = []
        
        # Add filters if provided
        if lokasi_filter:
            query += " AND p.lokasi_program IN (%s)" % ','.join(['%s'] * len(lokasi_filter))
            params.extend(lokasi_filter)
            
        if pendidikan_filter:
            query += " AND l.lowongan_min_pendidikan IN (%s)" % ','.join(['%s'] * len(pendidikan_filter))
            params.extend(pendidikan_filter)
        
        query += " ORDER BY l.lowongan_id DESC"
        
        if params:
            cur.execute(query, tuple(params))
        else:
            cur.execute(query)
            
        rows = cur.fetchall()
        cur.close()
        
        lowongans = []
        for row in rows:
            lowongans.append({
                'id': row[0],
                'program_id': row[1],
                'judul': row[2],
                'status': row[3],
                'min_umur': row[4],
                'max_umur': row[5],
                'keahlian': row[6],
                'pengalaman': row[7],
                'min_pendidikan': row[8],
                'kuota': row[9],
                'nama_program': row[10],
                'lokasi_program': row[11],
                'sektor_program': row[12],
                'deskripsi_program': row[13]
            })
        return lowongans
    except Exception as e:
        print(f"Error getting all lowongan with program: {e}")
        return []


def get_unique_locations():
    """Get all unique locations from program table"""
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT lokasi_program FROM program WHERE lokasi_program IS NOT NULL ORDER BY lokasi_program")
        rows = cur.fetchall()
        cur.close()
        return [row[0] for row in rows if row[0]]
    except Exception as e:
        print(f"Error getting unique locations: {e}")
        return []


def get_unique_education_levels():
    """Get all unique education levels from lowongan table"""
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT DISTINCT lowongan_min_pendidikan FROM lowongan WHERE lowongan_min_pendidikan IS NOT NULL ORDER BY lowongan_min_pendidikan")
        rows = cur.fetchall()
        cur.close()
        return [row[0] for row in rows if row[0]]
    except Exception as e:
        print(f"Error getting unique education levels: {e}")
        return []
    
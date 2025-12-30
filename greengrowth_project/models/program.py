def createProgram_db(admin_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program):
    """Insert a program into the DB. Import `mysql` lazily to avoid circular imports."""
    from greengrowth_project.app import mysql

    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "INSERT INTO program(nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id) VALUES(%s, %s, %s, %s, %s, %s, %s)",
            (nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id),
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error creating program: {e}")
        return False


def readProgram_by_admin(admin_id):
    # Get semua program milik admin
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT program_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id FROM program WHERE admin_id = %s", (admin_id,))
        programs = cur.fetchall()
        cur.close()
        return programs
    except Exception as e:
        print(f"Error reading programs: {e}")
        return []


def readProgram_by_id(program_id):
    # Get detail program berdasarkan ID - return: (program_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id)
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT program_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, admin_id FROM program WHERE program_id = %s", (program_id,))
        program = cur.fetchone()
        cur.close()
        return program
    except Exception as e:
        print(f"Error reading program: {e}")
        return None


def updateProgram_db(program_id, nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program):
    # Update program
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            "UPDATE program SET nama_program=%s, sektor_program=%s, tujuan_program=%s, lokasi_program=%s, status_program=%s, deskripsi_program=%s WHERE program_id=%s",
            (nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program, program_id),
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error updating program: {e}")
        return False


def deleteProgram_db(program_id):
    # Hapus program
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM program WHERE program_id = %s", (program_id,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error deleting program: {e}")
        return False


def get_all_programs(sektor=None, q=None):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()

    where_clauses = []
    params = []

    if sektor:
        where_clauses.append("sektor_program = %s")
        params.append(sektor)

    if q:
        like = f"%{q}%"
        where_clauses.append("(nama_program LIKE %s OR deskripsi_program LIKE %s OR lokasi_program LIKE %s)")
        params.extend([like, like, like])

    where_sql = ""
    if where_clauses:
        where_sql = " WHERE " + " AND ".join(where_clauses)

    cur.execute(
        f"""
        SELECT 
            program_id,
            nama_program,
            lokasi_program,
            deskripsi_program
        FROM program
        {where_sql}
        ORDER BY nama_program ASC
        """,
        tuple(params),
    )
    rows = cur.fetchall()
    cur.close()

    programs = []
    for r in rows:
        programs.append({
            'id': r[0],
            'nama': r[1],
            'lokasi': r[2],
            'deskripsi': r[3]
        })
    return programs



def get_program_by_id(program_id):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 
            program_id,
            nama_program,
            sektor_program,
            tujuan_program,
            lokasi_program,
            deskripsi_program
        FROM program
        WHERE program_id = %s
    """, (program_id,))
    r = cur.fetchone()
    cur.close()

    if not r:
        return None

    return {
        'id': r[0],
        'nama': r[1],
        'sektor': r[2],
        'tujuan': r[3],
        'lokasi': r[4],
        'deskripsi': r[5]
    }


def get_all_program_sectors():
    """Return unique program sectors suitable for UI filters."""
    from greengrowth_project.app import mysql

    cur = mysql.connection.cursor()
    cur.execute(
        """
        SELECT DISTINCT sektor_program
        FROM program
        WHERE sektor_program IS NOT NULL AND sektor_program <> ''
        ORDER BY sektor_program ASC
        """
    )
    rows = cur.fetchall()
    cur.close()

    return [{'nama': r[0]} for r in rows]


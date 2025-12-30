def createArtikel_db(judul_artikel, deskripsi, foto_artikel, program_id, admin_id):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO artikel(judul_artikel, deskripsi, foto_artikel, program_id, admin_id) VALUES(%s, %s, %s, %s, %s)",
        (judul_artikel, deskripsi, foto_artikel, program_id, admin_id),
    )
    mysql.connection.commit()
    cur.close()


def get_all_artikels():
    """Return list of artikels as dicts ordered by newest first, include program name if available"""
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT a.artikel_id, a.judul_artikel, a.deskripsi, a.foto_artikel, a.program_id, p.nama_program, a.created_at, a.updated_at "
        "FROM artikel a LEFT JOIN program p ON a.program_id = p.program_id "
        "ORDER BY a.created_at DESC"
    )
    rows = cur.fetchall()
    cur.close()

    artikels = []
    for r in rows:
        artikels.append({
            'artikel_id': r[0],
            'judul_artikel': r[1],
            'deskripsi': r[2],
            'foto_artikel': r[3],
            'program_id': r[4],
            'program_name': r[5],
            'created_at': r[6],
            'updated_at': r[7]
        })
    return artikels


def edit_artikel_by_id(artikel_id, new_judul, new_deskripsi, new_foto, program_id=None):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    try:
        if program_id is not None:
            # Validate program exists before updating
            cur.execute("SELECT program_id FROM program WHERE program_id=%s", (program_id,))
            if not cur.fetchone():
                raise ValueError(f"Program dengan ID {program_id} tidak ditemukan")
            
            cur.execute(
                "UPDATE artikel SET judul_artikel=%s, deskripsi=%s, foto_artikel=%s, program_id=%s WHERE artikel_id=%s",
                (new_judul, new_deskripsi, new_foto, program_id, artikel_id),
            )
        else:
            cur.execute(
                "UPDATE artikel SET judul_artikel=%s, deskripsi=%s, foto_artikel=%s WHERE artikel_id=%s",
                (new_judul, new_deskripsi, new_foto, artikel_id),
            )
        mysql.connection.commit()
    except Exception as e:
        mysql.connection.rollback()
        raise e
    finally:
        cur.close()


def delete_artikel_by_id(artikel_id):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute(
        "DELETE FROM artikel WHERE artikel_id=%s",
        (artikel_id,),
    )
    mysql.connection.commit()
    cur.close()


def get_artikel_by_id(artikel_id):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT a.artikel_id, a.judul_artikel, a.deskripsi, a.foto_artikel, a.program_id, p.nama_program, a.created_at, a.updated_at "
        "FROM artikel a LEFT JOIN program p ON a.program_id = p.program_id WHERE a.artikel_id=%s",
        (artikel_id,),
    )
    r = cur.fetchone()
    cur.close()
    if not r:
        return None
    return {
        'artikel_id': r[0],
        'judul_artikel': r[1],
        'deskripsi': r[2],
        'foto_artikel': r[3],
        'program_id': r[4],
        'program_name': r[5],
        'created_at': r[6],
        'updated_at': r[7]
    }
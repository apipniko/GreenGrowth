def createLaporan_db(program_id,foto_laporan,laporan_tanggal,laporan_persentase_progres,laporan_output_ekonomi):
    from greengrowth_project.app import mysql
    # Query untuk menambahkan laporan
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
                    INSERT INTO laporan (program_id,foto_laporan,laporan_tanggal,laporan_persentase_progres,laporan_output_ekonomi) VALUES(%s, %s, %s, %s, %s)
                    """,(program_id,foto_laporan,laporan_tanggal,laporan_persentase_progres,laporan_output_ekonomi,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error createing laporan: {e}")
        return False
    
def readLaporan_db():
    # Import MySQL
    from greengrowth_project.app import mysql
    # Query untuk menampilkan seluruh data laporan yang telah ditambah
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT laporan.laporan_id, program.nama_program, laporan.foto_laporan,laporan.laporan_tanggal, laporan.laporan_persentase_progres,laporan.laporan_output_ekonomi FROM laporan
            JOIN program
            ON laporan.program_id = program.program_id
            ORDER BY laporan_tanggal
            """
        )
        result = cur.fetchall()
        cur.close()
        return result
    except Exception as e:
        return []

def readLaporan_by_id(laporan_id):
    # Import MySQL
    from greengrowth_project.app import mysql
    # Query untuk menampilkan seluruh data laporan yang telah ditambah
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT laporan.laporan_id, program.nama_program, laporan.foto_laporan, laporan.laporan_tanggal, laporan.laporan_persentase_progres, laporan.laporan_output_ekonomi
            FROM laporan
            JOIN program ON laporan.program_id = program.program_id
            WHERE laporan_id = %s
            ORDER BY laporan_tanggal
            """, (laporan_id,)
        )
        result = cur.fetchone()
        cur.close()
        return result
    except Exception as e:
        return None

def updateLaporan_db(program_id, foto_laporan, laporan_tanggal, laporan_persentase_progres, laporan_output_ekonomi, laporan_id):
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            UPDATE laporan SET
              program_id=%s,
              foto_laporan=%s,
              laporan_tanggal=%s,
              laporan_persentase_progres=%s,
              laporan_output_ekonomi=%s
            WHERE laporan_id=%s
            """,
            (program_id, foto_laporan, laporan_tanggal, laporan_persentase_progres, laporan_output_ekonomi, laporan_id),
        )
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error updating laporan: {e}")
        return False

def deleteLaporan_db(laporan_id):
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM laporan WHERE laporan_id = %s", (laporan_id,))
        mysql.connection.commit()
        cur.close()
        return True
    except Exception as e:
        print(f"Error deleting laporan: {e}")
        return False
    
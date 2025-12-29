def statistik_persentase_program_db(program_id):
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT laporan.program_id, program.nama_program, laporan.laporan_persentase_progres, laporan.laporan_tanggal FROM laporan 
            JOIN program ON laporan.program_id = program.program_id
            WHERE laporan.program_id = %s
            ORDER BY laporan.laporan_tanggal;
            """,(program_id,)
        )
        result = cur.fetchall()
        cur.close()
        return result
    except Exception as e:
        print("[statistik_persentase_program_db] Error:", e)
        return []
    
def statistik_output_ekonomi_db(program_id):
    from greengrowth_project.app import mysql
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            """
            SELECT laporan.program_id, program.nama_program, laporan.laporan_output_ekonomi, laporan.laporan_tanggal FROM laporan 
            JOIN program ON laporan.program_id = program.program_id
            WHERE laporan.program_id = %s;
            """,(program_id,)
        )
        result = cur.fetchall()
        cur.close()
        return result
    except Exception as e:
        print("[statistik_output_ekonomi_db] Error:", e)
        return []
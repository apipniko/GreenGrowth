def createProgram_db(nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program):
    """Insert a program into the DB. Import `mysql` lazily to avoid circular imports."""
    from greengrowth_project.app import mysql

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO programs(nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program) VALUES(%s, %s, %s, %s, %s, %s)",
        (nama_program, sektor_program, tujuan_program, lokasi_program, status_program, deskripsi_program),
    )
    mysql.connection.commit()
    cur.close()




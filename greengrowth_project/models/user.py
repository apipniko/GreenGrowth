from werkzeug.security import generate_password_hash


def get_account_user(email):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email_user = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user

def add_account_user(nama_user, email_user, password_user):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users(nama_user, email_user, password_user) VALUES(%s, %s, %s)", (nama_user, email_user, generate_password_hash(password_user)))
    mysql.connection.commit()
    cur.close()

def get_user_profile(user_id):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT user_id, nama_user, email_user, foto_user, gender, tanggal_lahir, pendidikan_tertinggi, softskill, hardskill, pengalaman, no_hp, alamat FROM users WHERE user_id = %s", (user_id, ))
    profile = cur.fetchone()
    cur.close()
    if not profile:
        return None
    return {
        'user_id': profile[0],
        'nama_user': profile[1],
        'email_user': profile[2],
        'foto_user': profile[3],
        'gender': profile[4],
        'tanggal_lahir': profile[5],
        'pendidikan_tertinggi': profile[6],
        'softskill': profile[7],
        'hardskill': profile[8],
        'pengalaman': profile[9],
        'no_hp': profile[10],
        'alamat': profile[11]
    }

def edit_profile_by_id(user_id, nama_user, email_user, foto_user=None, gender=None, tanggal_lahir=None, pendidikan_tertinggi=None, softskill=None, hardskill=None, pengalaman=None, no_hp=None, alamat=None):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE users
        SET nama_user = %s,
            email_user = %s,
            foto_user = %s,
            gender = %s,
            tanggal_lahir = %s,
            pendidikan_tertinggi = %s,
            softskill = %s,
            hardskill = %s,
            pengalaman = %s,
            no_hp = %s,
            alamat = %s
        WHERE user_id = %s
    """, (nama_user, email_user, foto_user, gender, tanggal_lahir, pendidikan_tertinggi, softskill, hardskill, pengalaman, no_hp, alamat, user_id))
    mysql.connection.commit()
    cur.close()
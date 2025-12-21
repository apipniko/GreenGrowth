from werkzeug.security import generate_password_hash


def get_account_admin(email):
    from greengrowth_project.app import mysql
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin_pemerintah WHERE email_admin = %s", (email,))
    user = cur.fetchone()
    cur.close()
    return user
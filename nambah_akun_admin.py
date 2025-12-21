from werkzeug.security import generate_password_hash
from greengrowth_project.app import app, mysql

def add_account_admin():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO admin_pemerintah(nama_admin, email_admin, password_admin,foto_admin,instansi) VALUES(%s, %s, %s, %s, %s)", ('sleman', 'SlemanCity@gmail.com', generate_password_hash('sleman'), './static/images/image.png', 'DP3 Sleman'))
        mysql.connection.commit()
        cur.close()
        print("Admin account added successfully!")

add_account_admin()
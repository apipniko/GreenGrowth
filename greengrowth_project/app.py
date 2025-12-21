import os
from flask import Flask, render_template, request, redirect, url_for, session, flash 
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from .controllers.auth.routes import auth_bp
from .controllers.user.dashboard import user_bp
from .controllers.admin.dashboard import admin_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")
app.config["MYSQL_HOST"] = "localhost"
app.config['MYSQL_PORT'] = 3306
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "greengrowth"
mysql = MySQL(app)

# Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(admin_bp)

@app.route('/')
def welcome():
    return render_template('welcome.html')
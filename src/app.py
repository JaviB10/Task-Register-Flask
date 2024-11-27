from flask import Flask, request, render_template, redirect, url_for
from sqlite3 import connect
import sqlite3
from .models import initialize_database
from .services.project_service import ProjectService
from .services.user_service import UserService
from .routes.project_routes import project_bp
from .routes.user_routes import user_bp

app = Flask(__name__)

app.register_blueprint(project_bp, url_prefix='/projects')
app.register_blueprint(user_bp, url_prefix='/users')

def get_db_connection():
    conn = connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    db = get_db_connection()
    project_service = ProjectService(db)
    projects = project_service.get_all_projects()
    user_service = UserService(db)
    users = user_service.get_all_users()
    db.close()

    return render_template('home.html', page='home', projects=projects, users=users)

@app.route('/users')
def list_users():
    db = get_db_connection()
    user_service = UserService(db)
    users = user_service.get_all_users()
    db.close()
    return render_template('home.html', page='users', users=users)

@app.route('/projects_user/<int:user_id>')
def list_projects_user(user_id):
    db = get_db_connection()
    project_service = ProjectService(db)
    projects = project_service.get_projects_by_user(user_id)
    db.close()
    return render_template('home.html', page='projects_user', projects=projects)

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
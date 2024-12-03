from flask import Flask, request, render_template, redirect, url_for
from sqlite3 import connect
import sqlite3
from .models import initialize_database
from .services.project_service import ProjectService
from .services.user_service import UserService
from .services.project_collaborators_service import ProjectCollaboratorsService
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

    email = "admin@example.com"

    project_service = ProjectService(db)
    user_service = UserService(db)
    projects_collaborators_service = ProjectCollaboratorsService(db)

    users = user_service.get_all_users()
    user = user_service.get_user_by_email(email)

    projects = [dict(row) for row in project_service.get_projects_by_user(user['id'])]

    collaborator_rows = projects_collaborators_service.get_projects_collaborators_by_user(user['id'])
    project_collaborator_id = [row["project_id"] for row in collaborator_rows]

    # Si el usuario tiene colaboraciones, buscar los proyectos completos
    projects_collaborator = []
    if project_collaborator_id:
        projects_collaborator = [dict(row) for row in project_service.get_projects_by_id(project_collaborator_id)]

    # Unificar ambas listas sin duplicados
    all_projects = list({project["id"]: project for project in (projects + projects_collaborator)}.values())

    # Obtener todos los colaboradores de proyectos
    projects_collaborators = projects_collaborators_service.get_all_projects_collaborators()

    # Enriquecer proyectos con colaboradores
    all_projects = projects_collaborators_service.map_project_collaborators(all_projects, projects_collaborators)
    
    db.close()

    return render_template('home.html', page='home', all_projects=all_projects, users=users, user=user)

@app.route('/users')
def list_users():
    db = get_db_connection()
    email = "admin@example.com"
    user_service = UserService(db)
    users = user_service.get_all_users()
    user = user_service.get_user_by_email(email)
    db.close()

    return render_template('home.html', page='users', users=users, user=user)

@app.route('/projects_user/<int:user_id>')
def list_projects_user(user_id):
    db = get_db_connection()
    
    email = "admin@example.com"
    user_service = UserService(db)
    user = user_service.get_user_by_email(email)

    project_service = ProjectService(db)
    projects = [dict(row) for row in project_service.get_projects_by_user(user_id)]

    projects_collaborators_service = ProjectCollaboratorsService(db)
    collaborator_rows = projects_collaborators_service.get_projects_collaborators_by_user(user_id)
    project_collaborator_id = [row["project_id"] for row in collaborator_rows]

    # Si el usuario tiene colaboraciones, buscar los proyectos completos
    projects_collaborator = []
    if project_collaborator_id:
        projects_collaborator = [dict(row) for row in project_service.get_projects_by_id(project_collaborator_id)]

    # Unificar ambas listas sin duplicados
    all_projects = list({project["id"]: project for project in (projects + projects_collaborator)}.values())

    # Obtener todos los colaboradores de proyectos
    projects_collaborators = projects_collaborators_service.get_all_projects_collaborators()

    # Enriquecer proyectos con colaboradores
    all_projects = projects_collaborators_service.map_project_collaborators(all_projects, projects_collaborators)

    user_service = UserService(db)
    user_profile = user_service.get_user_by_id(user_id)
    users = user_service.get_all_users()
    db.close()

    return render_template('home.html', page='projects_user', all_projects=all_projects, user_profile=user_profile, user=user, users=users)

@app.route('/assigned_projects/<int:user_id>')
def assigned_projects(user_id):
    db = get_db_connection()

    project_service = ProjectService(db)
    projects = project_service.get_assigned_projects_by_user(user_id)
    user_service = UserService(db)
    users = user_service.get_all_users()
    user = user_service.get_user_by_id(user_id)

    db.close()

    return render_template('home.html', page='assigned_projects', projects=projects, users=users, user=user)


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
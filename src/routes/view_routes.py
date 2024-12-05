from flask import Blueprint, render_template
from ..database import get_db_connection
from .auth_routes import token_required, role_required
from ..services.project_service import ProjectService
from ..services.user_service import UserService
from ..services.project_collaborators_service import ProjectCollaboratorsService

view_bp = Blueprint('view', __name__)

@view_bp.route('/')
@token_required
def home(user_row):

    db = get_db_connection()

    project_service = ProjectService(db)
    user_service = UserService(db)

    # Obtener información del usuario
    user = user_service.get_user_by_email(user_row['email'])
    users = user_service.get_all_users()

    # Obtener proyectos del usuario
    all_projects = project_service.get_user_projects(user['id'], user['role'])

    db.close()

    return render_template('home.html', page='home', all_projects=all_projects, users=users, user=user)

@view_bp.route('/users')
@token_required
@role_required(0)
def list_users(user_row):

    db = get_db_connection()

    user_service = UserService(db)

    users = user_service.get_all_users()
    user = user_service.get_user_by_email(user_row['email'])

    db.close()

    return render_template('home.html', page='users', users=users, user=user)

@view_bp.route('/assigned_projects')
@token_required
def assigned_projects(user_row, **kwargs):

    db = get_db_connection()

    project_service = ProjectService(db)
    user_service = UserService(db)

    projects = project_service.get_assigned_projects_by_user(user_row['id'])
    
    users = user_service.get_all_users()
    user = user_service.get_user_by_id(user_row['id'])

    db.close()

    return render_template('home.html', page='assigned_projects', projects=projects, users=users, user=user)

@view_bp.route('/projects_user/<int:user_id>')
@token_required
def list_projects_user(user_id, user_row):
    db = get_db_connection()
    
    email = user_row['email']

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
from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from ..services.project_service import ProjectService
from sqlite3 import connect
import sqlite3

project_bp = Blueprint('projects', __name__)

def get_db_connection():
    conn = connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@project_bp.route('/', methods=['GET'])
def get_all_projects():
    db = get_db_connection()
    project_service = ProjectService(db)
    projects = project_service.get_all_projects()
    db.close()
    return render_template('table-projects.html', projects=projects)

@project_bp.route('/create_project', methods=['GET', 'POST'])
def create_project():
    db = get_db_connection()
    project_service = ProjectService(db)

    try:
        if request.method == 'POST':
            project_name = request.form.get('project_name')
            comments = request.form.get('comments')
            worked_hours = request.form.get('worked_hours', 0)
            to_do_list = request.form.get('to_do_list')

            collaborators_raw = request.form.get('collaborators', '')
            collaborators = [int(c.strip()) for c in collaborators_raw.split(',') if c.strip().isdigit()]

            # Crear el proyecto
            success = project_service.create_project(project_name, comments, worked_hours, to_do_list, collaborators = collaborators)

            if success:
                return redirect(request.referrer)  # Redirigir después de la actualización
            else:
                return "Error al crear el proyecto", 500
    except Exception as e:
        return jsonify({'error': 'Ocurrió un error al crear el proyecto', 'details': str(e)}), 500

@project_bp.route('/delete_project', methods=['GET', 'POST'])    
def delete_project():
    db = get_db_connection()
    project_service = ProjectService(db)

    if request.method == 'POST':
        project_id = request.form.get('projectId')

        # Actualizar el proyecto en la base de datos
        success = project_service.delete_project(project_id)

        if success:
            return redirect(request.referrer)  # Redirigir después de la actualización
        else:
            return "Error al eliminar el proyecto", 500

@project_bp.route('/update_project', methods=['GET', 'POST'])
def update_project():
    db = get_db_connection()
    project_service = ProjectService(db)

    if request.method == 'POST':
        project_id = request.form.get('project_id')
        project_name = request.form['project_name']
        comments = request.form['comments']
        to_do_list = request.form['to_do_list']
        worked_hours = request.form['worked_hours']
        status = int(request.form['status_project'])

        project = project_service.get_project_by_id(project_id)
        if not project:
            return "Proyecto no encontrado", 404

        success = project_service.update_project(project_id, project_name, comments, to_do_list, worked_hours, status)

        if success:
            return redirect(request.referrer)  # Redirigir después de la actualización
        else:
            return "Error al actualizar el proyecto", 500
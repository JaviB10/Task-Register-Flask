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
        project_name = request.form.get('project_name')
        comments = request.form.get('comments')
        worked_hours = request.form.get('worked_hours', 0)
        to_do_list = request.form.get('to_do_list')

        collaborators_raw = request.form.get('collaborators', '')
        collaborators = [int(c.strip()) for c in collaborators_raw.split(',') if c.strip().isdigit()]

        # Crear el proyecto
        project_id = project_service.create_project(project_name, comments, worked_hours, to_do_list, collaborators = collaborators)

        return jsonify({'message': 'Proyecto creado con éxito', 'project_id': project_id}), 201

    except Exception as e:
        return jsonify({'error': 'Ocurrió un error al crear el proyecto', 'details': str(e)}), 500

@project_bp.route('/delete_project', methods=['GET', 'POST'])    
def delete_project():
    db = get_db_connection()
    project_service = ProjectService(db)
    project_id = request.form.get('projectId')
    print(project_id)
    project_service.delete_project(project_id)

    return redirect(url_for('projects.get_all_projects'))
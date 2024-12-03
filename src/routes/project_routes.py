from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from ..services.project_service import ProjectService
from sqlite3 import connect
import sqlite3

project_bp = Blueprint('projects', __name__)

def get_db_connection():
    conn = connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@project_bp.route('/create_project', methods=['GET', 'POST'])
def create_project():
    db = get_db_connection()

    project_service = ProjectService(db)

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        project_name = request.form['project_name']
        comments = request.form['comments']
        worked_hours = request.form['worked_hours']
        worked_minutes = request.form['worked_minutes']
        to_do_list = request.form['to_do_list']

        # Recibir lista de IDs de colaboradores
        collaborators = request.form.getlist('collaborators')
        assigned_project = request.form.get('is_part_of_project') == "on"

        response = project_service.create_project(user_id, project_name, comments, worked_hours, worked_minutes, to_do_list, assigned_project, collaborators)

        return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]

@project_bp.route('/delete_project/<int:project_id>', methods=['GET', 'POST'])    
def delete_project(project_id):
    db = get_db_connection()

    project_service = ProjectService(db)

    response = project_service.delete_project(project_id)

    return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]

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
        worked_minutes = request.form['worked_minutes']
        status = int(request.form['status_project'])
        role_user = int(request.form['role_user'])

        # Recibir lista de IDs de colaboradores
        collaborators = request.form.getlist('collaborators')
        assigned_project = request.form.get('defaultCheck2') == "on"
        
        response = project_service.update_project(project_id, project_name, comments, to_do_list, worked_hours, worked_minutes, status, role_user, assigned_project, collaborators)

        return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]
        
@project_bp.route('/update_assigned_project/<int:project_id>', methods=['GET', 'POST'])
def update_assigned_project(project_id):
    db = get_db_connection()

    project_service = ProjectService(db)

    if request.method == 'POST':
        user_id = request.form['user_id']

        response = project_service.update_assigned_project(project_id, user_id)

        return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]
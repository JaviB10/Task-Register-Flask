from flask import Blueprint, request, jsonify
from ..database import get_db_connection
from ..services.project_service import ProjectService

project_bp = Blueprint('projects', __name__)

@project_bp.route('/create_project', methods=['GET', 'POST'])
def create_project():
    db = get_db_connection()
    try:
        project_service = ProjectService(db)

        if request.method == 'POST':
            user_id = request.form.get('user_id')
            project_name = request.form['project_name']
            comments = request.form['comments']
            worked_hours = request.form['worked_hours']
            worked_minutes = request.form['worked_minutes']
            to_do_list = request.form['to_do_list']
            assigned_project = request.form.get('is_part_of_project') == "on"

            # Recibir lista de IDs de colaboradores
            collaborators = request.form.getlist('collaborators')

            response = project_service.create_project(user_id, project_name, comments, worked_hours, worked_minutes, to_do_list, assigned_project, collaborators)

            return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]
    except Exception as e:
        db.rollback()
        return {"status": 500, "message": f"Unexpected error: {str(e)}"}
    
    finally:
        db.close()

@project_bp.route('/update_project/<int:project_id>', methods=['GET', 'POST'])
def update_project(project_id):
    db = get_db_connection()
    try:
        project_service = ProjectService(db)

        if request.method == 'POST':
            project_name = request.form['project_name']
            comments = request.form['comments']
            to_do_list = request.form['to_do_list']
            worked_hours = request.form['worked_hours']
            worked_minutes = request.form['worked_minutes']
            status = int(request.form['status_project'])
            user_id = request.form.get('userID')
            role_user = int(request.form['role_user_update'])
            assigned_project = request.form.get('defaultCheck2') == "on"

            # Recibir lista de IDs de colaboradores
            collaborators = request.form.getlist('collaborators')
            
            response = project_service.update_project(project_id, project_name, comments, to_do_list, worked_hours, worked_minutes, status, user_id, role_user, assigned_project, collaborators)
            
            return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]
    except Exception as e:
        db.rollback()
        return {"status": 500, "message": f"Unexpected error: {str(e)}"}
    
    finally:
        db.close()

@project_bp.route('/delete_project/<int:project_id>', methods=['GET', 'POST'])    
def delete_project(project_id):
    db = get_db_connection()
    try:
        project_service = ProjectService(db)

        if request.method == 'POST':
            user_id = request.form.get('user_id_delete')

        response = project_service.delete_project(project_id, user_id)

        return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]
    except Exception as e:
        db.rollback()
        return {"status": 500, "message": f"Unexpected error: {str(e)}"}
    
    finally:
        db.close()

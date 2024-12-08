from flask import Blueprint, request, jsonify
from ..database import get_db_connection
from .auth_routes import token_required
from ..services.user_service import UserService

user_bp = Blueprint('users', __name__)

@user_bp.route('/create_user', methods=['GET', 'POST'])
def create_user():

    db = get_db_connection()
    try:
        user_service = UserService(db)

        if request.method == 'POST':
            name = request.form.get('name')
            last_name = request.form.get('last_name')
            position = request.form.get('position')
            email = request.form.get('email')
            role = int(request.form['role_user'])

        response = user_service.create_user(name, last_name, position, email, role)

        return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]
    except Exception as e:
            db.rollback()
            return {"status": 500, "message": f"Unexpected error: {str(e)}"}
        
    finally:
        db.close()
        
@user_bp.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    db = get_db_connection()
    try:
        user_service = UserService(db)

        if request.method == 'POST':
            name = request.form['first_name']
            last_name = request.form['last_name']
            position = request.form['position_user']
            email = request.form['email_user']
            role = int(request.form['roleUser'])
        
            response = user_service.update_user(user_id, name, last_name, position, email, role)

            return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]
    except Exception as e:
        db.rollback()
        return {"status": 500, "message": f"Unexpected error: {str(e)}"}
    
    finally:
        db.close()

@user_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])    
def delete_user(user_id):
    db = get_db_connection()
    try:
        user_service = UserService(db)

        response = user_service.delete_user(user_id)

        return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]
    except Exception as e:
        db.rollback()
        return {"status": 500, "message": f"Unexpected error: {str(e)}"}
    
    finally:
        db.close()

        
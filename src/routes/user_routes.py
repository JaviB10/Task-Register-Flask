from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from ..services.user_service import UserService
from sqlite3 import connect
import sqlite3

user_bp = Blueprint('users', __name__)

def get_db_connection():
    conn = connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@user_bp.route('/', methods=['GET'])
def get_all_users():
    db = get_db_connection()
    user_service = UserService(db)
    users = user_service.get_all_users()
    db.close()
    return render_template('table-users.html', users=users)

@user_bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        position = request.form.get('position')
        email = request.form.get('email')

    db = get_db_connection()
    user_service = UserService(db)

    user_service.create_user(name, last_name, position, email, role="user")

    return redirect(url_for('users.get_all_users'))

@user_bp.route('/delete_user', methods=['GET', 'POST'])    
def delete_user():
    db = get_db_connection()
    user_service = UserService(db)
    user_id = request.form.get('userId')
    print(user_id)
    user_service.delete_user(user_id)

    return redirect(url_for('users.get_all_users'))
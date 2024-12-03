from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from ..services.user_service import UserService
from sqlite3 import connect
import sqlite3

user_bp = Blueprint('users', __name__)

def get_db_connection():
    conn = connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@user_bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    db = get_db_connection()

    user_service = UserService(db)

    if request.method == 'POST':
        name = request.form.get('name')
        last_name = request.form.get('last_name')
        position = request.form.get('position')
        email = request.form.get('email')

    response = user_service.create_user(name, last_name, position, email)

    return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]

@user_bp.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    db = get_db_connection()

    user_service = UserService(db)

    if request.method == 'POST':
        name = request.form['first_name']
        last_name = request.form['last_name']
        position = request.form['position_user']
        email = request.form['email_user']
    
        response = user_service.update_user(user_id, name, last_name, position, email)

        return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]

@user_bp.route('/delete_user/<int:user_id>', methods=['GET', 'POST'])    
def delete_user(user_id):
    db = get_db_connection()

    user_service = UserService(db)

    response = user_service.delete_user(user_id)

    return jsonify({'status': response["status"], 'message': response["message"]}), response["status"]

        
from flask import Blueprint, request, jsonify, render_template
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
    return render_template('index.html', projects=projects)
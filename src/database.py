import os
from dotenv import load_dotenv
import sqlite3
from .models.users import User
from .models.projects import Project
from .models.project_collaborators import ProjectCollaborator
from .models.recycle_projects import RecycleProjects

load_dotenv()

DATABASE = os.getenv("DATABASE")

def get_db_connection():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    conn.execute('PRAGMA journal_mode=WAL;')

    # Crear tablas
    User.create_table(cursor)
    Project.create_table(cursor)
    ProjectCollaborator.create_table(cursor)
    RecycleProjects.create_table(cursor)

    conn.commit()
    conn.close()
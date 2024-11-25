import sqlite3
from .users import User
from .projects import Project
from .project_collaborators import ProjectCollaborator

def initialize_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    User.create_table(cursor)
    Project.create_table(cursor)
    ProjectCollaborator.create_table(cursor)

    conn.commit()
    conn.close()
from sqlite3 import Connection

class ProjectCollaboratorsService:
    def __init__(self, db: Connection):
        self.db = db

    def get_all_projects_collaborators(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM project_collaborators')
        return cursor.fetchall()
    
    def get_projects_collaborators_by_user(self, user_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM project_collaborators WHERE collaborator_id = ?', (user_id,))
        return cursor.fetchall()
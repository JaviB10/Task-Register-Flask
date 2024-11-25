from sqlite3 import Connection
from datetime import datetime

class ProjectService:
    def __init__(self, db: Connection):
        self.db = db

    def get_all_projects(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM projects')
        return cursor.fetchall()
    
    def get_project_by_id(self, project_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id))
        return cursor.fetchone()
    
    def create_project(self, project_name, comments, worked_hours, to_do_list, collaborators = []):
        cursor = self.db.cursor()
        
        start = datetime.now().strftime('%Y-%m-%d')
        finish = None 
        status = 'In progress'
        user_id = 1

        cursor.execute('''
            INSERT INTO projects (project_name, comments, start, finish, status, worked_hours, to_do_list, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (project_name, comments, start, finish, status, worked_hours, to_do_list, user_id))
        
        project_id = cursor.lastrowid

        for user_id in collaborators:
            cursor.execute('''
                INSERT INTO project_collaborators(project_id, user_id)
                VALUES (?, ?)
            ''', (project_id, user_id))

        self.db.commit()
        return project_id
    
    def delete_project(self, project_id):
        cursor = self.db.cursor()
        
        cursor.execute('''
            DELETE FROM project_collaborators WHERE project_id = ?
        ''', (project_id,))
        
        cursor.execute('''
            DELETE FROM projects WHERE id = ?
        ''', (project_id,))
        
        self.db.commit()

        if cursor.rowcount == 0:
            return False
        return True
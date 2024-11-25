from sqlite3 import Connection

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
    
    def create_project(self, project, collaborators = []):
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO projects (project_name, comments, start, finish, status, worked_hours, to_do_list, user_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (
                project['project_name'],
                project['comments'],
                project['start'],
                project['finish'],
                project['status'],
                project['worked_hours'],
                project['to_do_list'],
                project['user_id'],
            ))
        
        project_id = cursor.lastrowid

        for user_id in collaborators:
            cursor.execute('''
                INSERT INTO project_collaborators(project_id, user_id)
                VALUES (?, ?)
            ''', (project_id, user_id))

        self.db.commit()
        return project_id
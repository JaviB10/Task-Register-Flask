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
        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        return cursor.fetchone()
    
    def get_projects_by_id(self, project_ids):
        cursor = self.db.cursor()
        if not project_ids:
            return []  # Retornar lista vacía si no hay IDs

        placeholders = ','.join('?' for _ in project_ids)
        query = f'SELECT * FROM projects WHERE id IN ({placeholders})'

        cursor = self.db.cursor()
        cursor.execute(query, project_ids)
        return cursor.fetchall()
    
    def get_projects_by_user(self, user_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM projects WHERE creator_id = ?', (user_id,))
        return cursor.fetchall()
    
    def get_assigned_projects_by_user(self, user_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM projects WHERE creator_id = ? AND assigned_user_id IS NOT NULL', (user_id,))
        return cursor.fetchall()
    
    def create_project(self, user_id, project_name, comments, worked_hours, worked_minutes, to_do_list, collaborators):
        cursor = self.db.cursor()
        
        creator_id = user_id
        start = datetime.now().strftime('%d-%m-%Y')
        finish = None 
        status = True

        if worked_hours == "":
            worked_hours = 0
        
        if worked_minutes == "":
            worked_minutes = 0

        cursor.execute('''
            INSERT INTO projects (project_name, comments, start, finish, status, worked_hours, worked_minutes, to_do_list, creator_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (project_name, comments, start, finish, status, worked_hours, worked_minutes, to_do_list, creator_id))
        
        project_id = cursor.lastrowid  # Obtener el ID del proyecto recién creado

        # Insertar colaboradores en la tabla `project_collaborators`
        if collaborators:
            for collaborator_id in collaborators:
                cursor.execute('''
                    INSERT INTO project_collaborators (project_id, collaborator_id)
                    VALUES (?, ?)
                ''', (project_id, collaborator_id))

        self.db.commit()
        
        return {"status": 200, "message": "Project created successfully."}
    
    def delete_project(self, project_id):
        cursor = self.db.cursor()

        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = cursor.fetchone()

        if not project:
            return {"status": 404, "message": "Project not found."}
        
        if project['status'] == 1:
            return {"status": 400, "message": "The project is in progress, so it cannot be deleted."}
        
        cursor.execute('DELETE FROM project_collaborators WHERE project_id = ?', (project_id,))
        
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        
        self.db.commit()

        return {"status": 200, "message": "Project deleted successfully."}
    
    def update_project(self, project_id, project_name, comments, to_do_list, worked_hours, worked_minutes, status, collaborators):
        try:
            cursor = self.db.cursor()

            cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
            project = cursor.fetchone()

            if not project:
                return {"status": 404, "message": "Project not found."}

            if status == 0:  # Finished
                finish = datetime.now().strftime('%d-%m-%Y')
            else:  # In Progress
                finish = None

            if worked_hours == "":
                worked_hours = 0
            
            if worked_minutes == "":
                worked_minutes = 0
            
            cursor.execute('''
                UPDATE projects 
                SET project_name = ?, comments = ?, to_do_list = ?, worked_hours = ?, worked_minutes = ?, status = ?, finish = ?
                WHERE id = ?
            ''', (project_name, comments, to_do_list, worked_hours, worked_minutes, status, finish, project_id))

            creator_id = project["creator_id"]
            print(creator_id)
            if collaborators:
                collaborators = [int(collaborator) for collaborator in collaborators]
                print(collaborators)
                if creator_id in collaborators:
                    return {"status": 400, "message": "The creator of the project cannot be a collaborator."}

                cursor.execute('DELETE FROM project_collaborators WHERE project_id = ?', (project_id,))
                
                for collaborator_id in collaborators:
                    cursor.execute('''
                        INSERT INTO project_collaborators (project_id, collaborator_id)
                        VALUES (?, ?)
                    ''', (project_id, collaborator_id))
            
            self.db.commit()

            return {"status": 200, "message": "Project updated successfully."}
            
        except Exception as e:
            print(f"Error al actualizar el proyecto: {e}")
            return False
        
    def update_assigned_project(self, project_id, user_id):
        try:
            cursor = self.db.cursor()

            cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
            project = cursor.fetchone()

            if not project:
                return {"status": 404, "message": "Project not found."}
            
            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()

            if not user:
                return {"status": 404, "message": "User not found."}

            if int(user_id) != 0:
                cursor.execute('UPDATE projects SET assigned_user_id = ? WHERE id = ?', (user_id, project_id))

                self.db.commit()

                return {"status": 200, "message": "Project updated successfully."}

        except Exception as e:
            print(f"Error al asignar el proyecto a un usuario: {e}")
            return False
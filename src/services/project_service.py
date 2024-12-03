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
        cursor.execute('SELECT * FROM projects WHERE creator_id = ? AND assigned_id != 0', (user_id,))
        projects = [dict(row) for row in cursor.fetchall()]

        # Obtener los IDs de los proyectos donde el usuario es colaborador
        cursor.execute('''
            SELECT project_id 
            FROM project_collaborators 
            WHERE collaborator_id = ?
        ''', (user_id,))
        collaborator_rows = cursor.fetchall()
        project_collaborator_ids = [row["project_id"] for row in collaborator_rows]

        # Si el usuario tiene colaboraciones, buscar los proyectos completos
        projects_collaborator = []
        if project_collaborator_ids:
            cursor.execute('SELECT * FROM projects WHERE id IN ({})'.format(
                ','.join('?' * len(project_collaborator_ids))
            ), project_collaborator_ids)
            projects_collaborator = [dict(row) for row in cursor.fetchall()]

        # Unificar ambas listas sin duplicados
        all_projects = list({project["id"]: project for project in (projects + projects_collaborator)}.values())

        # Obtener todos los colaboradores de proyectos
        cursor.execute('SELECT * FROM project_collaborators')
        projects_collaborators = cursor.fetchall()

        # Mapear colaboradores a proyectos
        project_collaborators_map = {}
        for collaborator in projects_collaborators:
            project_id = collaborator["project_id"]
            collaborator_id = collaborator["collaborator_id"]
            if project_id not in project_collaborators_map:
                project_collaborators_map[project_id] = []
            project_collaborators_map[project_id].append(collaborator_id)

        # Enriquecer los proyectos con los colaboradores
        for project in all_projects:
            project_id = project["id"]
            project["collaborators"] = project_collaborators_map.get(project_id, [])

        return all_projects
    
    def create_project(self, user_id, project_name, comments, worked_hours, worked_minutes, to_do_list, assigned_project, collaborators):
        cursor = self.db.cursor()
        
        creator_id = user_id
        start = datetime.now().strftime('%d-%m-%Y')
        finish = None 
        status = True

        if worked_hours == "":
            worked_hours = 0
        
        if worked_minutes == "":
            worked_minutes = 0
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if user['role'] != 1:
            if assigned_project is False:
                    assigned_project = collaborators[0] if collaborators else None
            else:
                assigned_project = 0

        cursor.execute('''
            INSERT INTO projects (project_name, comments, start, finish, status, worked_hours, worked_minutes, to_do_list, creator_id, assigned_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (project_name, comments, start, finish, status, worked_hours, worked_minutes, to_do_list, creator_id, assigned_project))
        
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
    
    def update_project(self, project_id, project_name, comments, to_do_list, worked_hours, worked_minutes, status, role_user, assigned_project, collaborators):
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
            
            print(assigned_project)

            if role_user != 1:
                if assigned_project is False:
                    assigned_project = collaborators[0] if collaborators else None
                else:
                    assigned_project = 0

            cursor.execute('''
                UPDATE projects 
                SET project_name = ?, comments = ?, to_do_list = ?, worked_hours = ?, worked_minutes = ?, status = ?, finish = ?, assigned_id = ?
                WHERE id = ?
            ''', (project_name, comments, to_do_list, worked_hours, worked_minutes, status, finish, assigned_project, project_id))

            creator_id = project["creator_id"]
          
            collaborators = [int(collaborator) for collaborator in collaborators]

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
            self.db.rollback()  # Revertir cambios en caso de error
            return {"status": 500, "message": f"An error occurred: {str(e)}"}
        
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
from sqlite3 import Connection
from datetime import datetime
from .project_collaborators_service import ProjectCollaboratorsService

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
    
    def get_projects_assigned_to_user(self, user_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM projects WHERE creator_id = ? AND assigned_id != ?', (user_id, user_id))
        return cursor.fetchall()

    def get_assigned_projects_by_user(self, user_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM projects WHERE creator_id = ? AND assigned_id != ?', (user_id, user_id))
        projects = [dict(row) for row in cursor.fetchall()]

        # Obtener los colaboradores asociados a estos proyectos
        cursor.execute(
            'SELECT project_id, collaborator_id FROM project_collaborators WHERE project_id IN ({})'.format(
                ','.join('?' * len(projects))
            ),
            [project["id"] for project in projects]
        )
        collaborator_rows = cursor.fetchall()

        # Mapear los colaboradores a sus respectivos proyectos
        project_collaborators_map = {}
        for row in collaborator_rows:
            project_id = row["project_id"]
            collaborator_id = row["collaborator_id"]
            if project_id not in project_collaborators_map:
                project_collaborators_map[project_id] = []
            project_collaborators_map[project_id].append(collaborator_id)

        # Enriquecer los proyectos con los colaboradores
        for project in projects:
            project_id = project["id"]
            project["collaborators"] = project_collaborators_map.get(project_id, [])

        return projects
    
    def create_project(self, user_id, project_name, comments, worked_hours, worked_minutes, to_do_list, assigned_project, collaborators):
        cursor = self.db.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if user['role'] == 0:
            if assigned_project == False and collaborators == []:
                return {"status": 400, "message": "The project must have at least one collaborator or include you as a participant."}

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
                assigned_project = user_id
        else:
            assigned_project = user_id

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
    
    def delete_project(self, project_id, user_id):
        cursor = self.db.cursor()

        cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        project = cursor.fetchone()
        print(project)
        if not project:
            return {"status": 404, "message": "Project not found."}
        
        if project['status'] == 1:
            return {"status": 400, "message": "The project is in progress, so it cannot be deleted."}

        cursor.execute('''
            INSERT INTO recycle_projects (
                original_project_id, project_name, comments, start, finish, 
                status, worked_hours, worked_minutes, to_do_list, 
                creator_id, assigned_id, deleted_at, deleted_by
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_DATE, ?)
        ''', (
            project['id'], project['project_name'], project['comments'], project['start'], project['finish'],
            project['status'], project['worked_hours'], project['worked_minutes'], project['to_do_list'],
            project['creator_id'], project['assigned_id'], user_id
        ))

        cursor.execute('DELETE FROM project_collaborators WHERE project_id = ?', (project_id,))
        
        cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        
        self.db.commit()

        return {"status": 200, "message": "Project deleted successfully."}
    
    def update_project(self, project_id, project_name, comments, to_do_list, worked_hours, worked_minutes, status, user_id, role_user, assigned_project, collaborators):
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

            cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            user = cursor.fetchone()    

            if role_user != 1:  # Si el rol no es 'user'
                if assigned_project is False:
                    if collaborators:
                        # Si no hay asignado, se asigna al primer colaborador
                        assigned_project = collaborators[0]
                    else:
                        assigned_project = project['creator_id']
                else:
                    # Si ya está asignado, verificar si el usuario es el creador
                    if user['id'] != project['creator_id']:
                        return {"status": 400, "message": "You are not the creator of the project, so you cannot assign yourself to it. If you wish to participate, you must do so as a collaborator."}
                    else:
                        assigned_project = user['id']
            else:  # Si el rol es 'user'
                if collaborators:
                    # Si hay colaboradores, asignar el proyecto al primer colaborador
                    assigned_project = collaborators[0]
                else:
                    # Si no hay colaboradores, asignar el proyecto al creador (admin)
                    assigned_project = project['creator_id']

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
        
    def get_user_projects(self, user_id, role):
        # Proyectos creados por el usuario
        projects_created = [dict(row) for row in self.get_projects_by_user(user_id)]
        print('Proyecto creado',projects_created)
        # Proyectos donde el usuario es colaborador
        projects_collaborators_service = ProjectCollaboratorsService(self.db)
        collaborator_rows = projects_collaborators_service.get_projects_collaborators_by_user(user_id)
        projects_collaborator_ids = [row["project_id"] for row in collaborator_rows]
        print('projects_collaborator_ids',projects_collaborator_ids)
        projects_as_collaborator = []
        if projects_collaborator_ids:
            projects_as_collaborator = [dict(row) for row in self.get_projects_by_id(projects_collaborator_ids)]
        print('projects_as_collaborator',projects_as_collaborator)
        # Proyectos asignados al usuario
        projects_assigned = [dict(row) for row in self.get_projects_assigned_to_user(user_id)]
        print('projects_assigned',projects_assigned)
        # Filtrar y combinar según el rol del usuario
        if role == 1:
            # Usuario regular: incluir creados, colaboraciones y asignados
            all_projects = list({
                project["id"]: project
                for project in (projects_created + projects_as_collaborator + projects_assigned)
            }.values())
        elif role == 0:
            print('Entrar como admin')
            # Administrador: incluir creados y colaboraciones, excluir asignados
            filtered_projects_created = [
                project for project in projects_created
                if project["assigned_id"] == user_id
            ]
            print('filtered_projects_created', filtered_projects_created)

            # Combinar proyectos creados filtrados y colaboraciones
            all_projects = list({
                project["id"]: project
                for project in (filtered_projects_created + projects_as_collaborator)
            }.values())
            print('all_projects', all_projects)
        # Mapear colaboradores a proyectos
        projects_collaborators = projects_collaborators_service.get_all_projects_collaborators()
        all_projects = self.map_project_collaborators(all_projects, projects_collaborators)

        return all_projects

    def map_project_collaborators(self, projects, projects_collaborators):
        project_collaborators_map = {}
        for pc in projects_collaborators:
            project_id = pc['project_id']
            collaborator_id = pc['collaborator_id']
            if project_id not in project_collaborators_map:
                project_collaborators_map[project_id] = []
            project_collaborators_map[project_id].append(collaborator_id)

        for project in projects:
            project['collaborators'] = project_collaborators_map.get(project['id'], [])

        return projects
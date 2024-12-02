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
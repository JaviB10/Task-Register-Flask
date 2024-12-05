class ProjectCollaborator:
    def __init__(self, project_id, collaborator_id):
        self.project_id = project_id
        self.collaborator_id = collaborator_id

    @staticmethod
    def create_table(cursor):
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_collaborators(
                project_id INTEGER NOT NULL,
                collaborator_id INTEGER NOT NULL,
                PRIMARY KEY (project_id, collaborator_id),
                FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
                FOREIGN KEY(collaborator_id) REFERENCES users(id) ON DELETE CASCADE
            )
        ''')
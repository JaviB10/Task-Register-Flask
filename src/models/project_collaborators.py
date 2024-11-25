class ProjectCollaborator:
    def __init__(self, id, project_id, user_id):
        self.id = id
        self.project_id = project_id
        self.user_id = user_id

    @staticmethod
    def create_table(cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS project_collaborators(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   project_id INTEGER NOT NULL,
                   user_id INTEGER NOT NULL,
                   FOREIGN KEY(project_id) REFERENCES projects(id) ON DELETE CASCADE,
                   FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
    ''')
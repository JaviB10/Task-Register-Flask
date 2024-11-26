class Project:
    def __init__(self, id, project_name, comments, start, finish, status, collaborators, worked_hours, to_do_list, user_id ):
        self.id = id
        self.project_name = project_name
        self.comments = comments
        self.start = start
        self.finish = finish
        self.status = status
        self.collaborators = collaborators
        self.worked_hours = worked_hours
        self.to_do_list = to_do_list
        self.user_id = user_id

    @staticmethod
    def create_table(cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   project_name TEXT NOT NULL,
                   comments TEXT,
                   start DATE NOT NULL DEFAULT CURRENT_DATE,
                   finish DATE DEFAULT NULL,
                   status BOOLEAN DEFAULT 1,  -- 1 means In Progress, 0 means Finished,
                   worked_hours INTEGER DEFAULT 0,
                   to_do_list TEXT,
                   user_id INTEGER,
                   FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE SET NULL
            )
    ''')
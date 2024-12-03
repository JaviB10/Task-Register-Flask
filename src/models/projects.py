class Project:
    def __init__(self, id, project_name, comments, start, finish, status, worked_hours, worked_minutes, to_do_list, creator_id, assigned_id):
        self.id = id
        self.project_name = project_name
        self.comments = comments
        self.start = start
        self.finish = finish
        self.status = status
        self.worked_hours = worked_hours
        self.worked_minutes = worked_minutes
        self.to_do_list = to_do_list
        self.creator_id = creator_id
        self.assigned_id = assigned_id

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
                worked_minutes INTEGER DEFAULT 0,
                to_do_list TEXT,
                creator_id INTEGER NOT NULL,
                assigned_id INTEGER DEFAULT NULL,
                FOREIGN KEY(creator_id) REFERENCES users(id) ON DELETE CASCADE
            )
    ''')
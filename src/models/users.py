class User:
    def __init__(self, id, name, last_name, position, email, role, profile_picture = None):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.position = position
        self.email = email
        self.role = role
        self.profile_picture = profile_picture

    @staticmethod
    def create_table(cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    role TEXT CHECK(role IN ('admin', 'user')) DEFAULT 'user',
                    profile_picture TEXT
        )
    ''')
from werkzeug.security import check_password_hash, generate_password_hash

class User:
    def __init__(self, id, name, last_name, position, email, password, role, profile_picture = None):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.position = position
        self.email = email
        self.password = password
        self.role = role
        self.profile_picture = profile_picture

    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)

    @staticmethod
    def create_table(cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    role TEXT CHECK(role IN ('admin', 'user')) DEFAULT 'user',
                    profile_picture TEXT
        )
    ''')
from sqlite3 import Connection

class UserService:
    def __init__(self, db: Connection):
        self.db = db

    def get_all_users(self):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM users')
        return cursor.fetchall()
    
    def get_user_by_id(self, user_id):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id))
        return cursor.fetchone()
    
    def create_user(self, name, last_name, position, email, role):
        cursor = self.db.cursor()
        cursor.execute('''
            INSERT INTO users (name, last_name, position, email, role)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, last_name, position, email, role))
        self.db.commit()
        return cursor.lastrowid
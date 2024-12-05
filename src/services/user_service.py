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
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        return cursor.fetchone()
    
    def get_user_by_email(self, email):
        cursor = self.db.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return cursor.fetchone()
    
    def create_user(self, name, last_name, position, email, role):
        cursor = self.db.cursor()

        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user:
            return {"status": 400, "message": "The email has already been taken."}

        cursor.execute('''
            INSERT INTO users (name, last_name, position, email, role)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, last_name, position, email, role))

        self.db.commit()

        return {"status": 200, "message": "User created successfully."}
    
    def update_user(self, user_id, name, last_name, position, email, role):
        cursor = self.db.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            return {"status": 404, "message": "User not found."}
        
        if email != user['email']:
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            
            if user:
                return {"status": 400, "message": "The email has already been taken."}
        
        cursor.execute('UPDATE users SET name = ?, last_name = ?, position = ?, email = ?, role = ? WHERE id = ?', (name, last_name, position, email, role, user_id))
        
        self.db.commit()

        return {"status": 200, "message": "User updated successfully."}
        
    
    def delete_user(self, user_id):
        cursor = self.db.cursor()

        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            return {"status": 404, "message": "User not found."}
        
        cursor.execute('SELECT * FROM projects WHERE creator_id = ?', (user_id,))
        projects = cursor.fetchall()

        if projects:
            for project in projects:
                if project['status'] == 1:
                    return {"status": 400, "message": "The user cannot be deleted because they have unfinished projects."}
        
        # Intentar eliminar el usuario
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))

        self.db.commit()
        
        return {"status": 200, "message": "User updated successfully."}
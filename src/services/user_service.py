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
        cursor.execute('''
            INSERT INTO users (name, last_name, position, email, role)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, last_name, position, email, role))
        self.db.commit()
        return cursor.lastrowid
    
    def delete_user(self, user_id):
        cursor = self.db.cursor()
        print(user_id)
        # Comprobar si el usuario existe
        cursor.execute('''
            SELECT * FROM users WHERE id = ?
        ''', (user_id,))
        user = cursor.fetchone()
        if not user:
            print(f"El usuario con id {user_id} no existe.")
            return False
        
        # Intentar eliminar el usuario
        cursor.execute('''
            DELETE FROM users WHERE id = ?
        ''', (user_id,))
        self.db.commit()
        
        if cursor.rowcount == 0:
            print(f"No se pudo eliminar el usuario con id {user_id}.")
            return False
        
        print(f"Usuario con id {user_id} eliminado correctamente.")
        return True
    
    def update_user(self, user_id, name, last_name, position, email, current_email):
        try:
            cursor = self.db.cursor()
            
            if email != current_email:
                cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
                user = cursor.fetchone()
                
                if user:
                    if cursor.rowcount > 0:
                        return True
                    else:
                        return False
            
            cursor.execute('''
                UPDATE users 
                SET name = ?, last_name = ?, position = ?, email = ?
                WHERE id = ?
            ''', (name, last_name, position, email, user_id))
            
            self.db.commit()

            if cursor.rowcount > 0:
                return True
            else:
                return False
            
        except Exception as e:
            print(f"Error al actualizar el usuario: {e}")
            return False
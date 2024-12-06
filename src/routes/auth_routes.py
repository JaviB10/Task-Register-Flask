from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session
from functools import wraps
from ..database import get_db_connection
from ..services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'jwt' in request.cookies:
            token = request.cookies.get('jwt')
        elif 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return redirect(url_for('auth.login_page'))
        
        db = get_db_connection()
        auth_service = AuthService(db)
        data = auth_service.decode_token(token)

        if not data:
            return redirect(url_for('auth.login_page'))
        
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (int(data['user_id']),))
        user_row = cursor.fetchone()
        if not user_row:
            return jsonify({'message': 'User not found!'}), 401
        
        session['current_user'] = { 
            'id': user_row['id'], 
            'email': user_row['email'], 
            'role': user_row['role'] 
        }
        
        db.close()
        
        return f(user_row, *args, **kwargs)
    return decorated

def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'current_user' not in session  or session['current_user'].get('role') != required_role:
                return jsonify({'message': 'You do not have permission to access this resource!'}), 403
            return f(*args, **kwargs)
        return decorated
    return decorator

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')

    if not email:
        return jsonify({'message': 'Email and password are required!'}), 400
    
    # Obtener la conexión a la base de datos
    db = get_db_connection()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user_row = cursor.fetchone()


    if not user_row:
        return jsonify({'message': 'Invalid email or password!'}), 401
    
    auth_service = AuthService(db)
    token = auth_service.generate_token(user_row['id'], user_row['email'], user_row['role'])

    response = jsonify({'message': 'Logged in successfully!'})
    response.set_cookie('jwt', token, httponly=True)

    db.close()

    return response

@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_bp.route('/logout', methods=['GET'])
def logout():
    # Eliminar el token de las cookies
    response = redirect(url_for('auth.login_page'))

    # Eliminar el token de las cookies (seteamos el valor a None y max_age a 0 para eliminarlo)
    response.set_cookie('jwt', '', expires=0)
    
    # Limpiar la información de la sesión
    session.pop('current_user', None)  # Eliminar el 'current_user' de la sesión

    return response
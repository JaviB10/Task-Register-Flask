from dotenv import load_dotenv
from flask import Flask
import os
from .database import initialize_database
from .routes.project_routes import project_bp
from .routes.user_routes import user_bp
from .routes.auth_routes import auth_bp
from .routes.view_routes import view_bp

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

app.register_blueprint(project_bp, url_prefix='/projects')
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(view_bp, url_prefix='/')

with app.app_context():
    initialize_database()

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template
from .models import initialize_database
from .routes.project_routes import project_bp
from .routes.user_routes import user_bp

app = Flask(__name__)

app.register_blueprint(project_bp, url_prefix='/')
app.register_blueprint(user_bp, url_prefix='/')

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
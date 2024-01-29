from flask import abort, Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# db variable initialization
DB = 'database.db'
db = SQLAlchemy()


#csrf protection for forms
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'osff-management-app'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB}'
    csrf.init_app(app)
    db.init_app(app)

    from .home import home
    from .auth import auth
    from .user import user
    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')

    # Create database with models
    from .models import User, Role, Department
    with app.app_context():
        db.create_all()


    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    return app
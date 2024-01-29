from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

class User(UserMixin, db.Model):
    """
    Create User table
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        """
        Set password to a hash value
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Verify password against password hash
        """
        return check_password_hash(self.password_hash, password)



class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='department',
                                lazy='dynamic')

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role',
                                lazy='dynamic')
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

DB = 'rentride.db'

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'rent-ride'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB}'

db.init_app(app)

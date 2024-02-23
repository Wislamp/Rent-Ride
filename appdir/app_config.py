from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def init_db():
    db = SQLAlchemy()
    return db


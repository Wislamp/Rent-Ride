from flask import render_template
from .app_config import app

@app.route('/')
def index():
    return render_template('home.html')
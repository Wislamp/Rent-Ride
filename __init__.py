from .app_config import db, app
from .models import Car, Rental, Customer

# Create database
with app.app_context():
    db.create_all()
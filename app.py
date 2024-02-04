from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# db variable initialization
DB = 'database.db'
db = SQLAlchemy()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rent-ride'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB}'
db.init_app(app)

# from .home import home
# app.register_blueprint(home, url_prefix='/')

# Database  models
class Car(db.Model):
    """
    Create a Car table
    """

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    color = db.Column(db.String(20))
    plate = db.Column(db.String(15), unique=True)
    rate_per_hour = db.Column(db.Float)
    status = db.Column(db.String(20))

    # Relationships
    rentals = db.relationship('Rental', backref='car', lazy='dynamic')


class Rental(db.Model):
    """
    Create a Rental table
    """

    __tablename__ = 'rentals'

    id = db.Column(db.Integer, primary_key=True)
    pickup_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)
    total_cost = db.Column(db.Float)

    # Foreign Keys
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))


class Customer(db.Model):
    """
    Create a Customer table
    """

    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(60), unique=True)
    phone = db.Column(db.String(15))
    address = db.Column(db.String(200))

    # Relationships
    rentals = db.relationship('Rental', backref='customer', lazy='dynamic')

# Create database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('hello.html')
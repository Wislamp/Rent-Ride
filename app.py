from flask import Flask, render_template
import app_config 

DB = 'rentride.db'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'rent-ride'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB}'

db = app_config.init_db()
db.init_app(app)

"""
Import Database Models
"""
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
    rate_per_hour = db.Column(db.Float)
    status = db.Column(db.String(20))
    category = db.Column(db.String(50))

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

"""
End Import
"""

# Create Database Tables
with app.app_context():
    db.create_all()



@app.route('/')
def index():
    return render_template('home.html')

@app.route('/cars/1')
def show_car_details():
    return render_template('car-details.html')

@app.route('/rent-form')
def rent_form():
    return render_template('rent-form.html')
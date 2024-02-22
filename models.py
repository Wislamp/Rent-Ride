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
    duration = db.Column(db.Integer)

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
    city = db.Column(db.String(100))

    # Relationships
    region = db.Relationship('Region', backref='region', lazy='dynamic')
    rentals = db.relationship('Rental', backref='customer', lazy='dynamic')

class Region(db.Model):
    """
    Create a Region table
    """"

    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


def db_create(app):
    with app.app_context():
        db.create_all()
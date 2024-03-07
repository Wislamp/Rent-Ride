import os
from flask import Flask, render_template, request, redirect


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='rent-ride',
        DATABASE=os.path.join(app.instance_path, 'rentride.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        print('instance dir exists or an error occured while creating it..')




    """
    ---ROUTES---
    """
    @app.route('/')
    def index():
        query = 'SELECT * from cars WHERE category=?'
        cursor = db.get_db().execute(query, ['Popular'])
        cars = cursor.fetchall()
        if cars is None:
            cars = 'No available cars'
        else:
            cars = list(cars)
        return render_template('home.html', available_cars = cars)

    @app.route('/cars/<car_id>')
    def show_car_details(car_id):
        query = 'SELECT * from cars WHERE id=?'
        cursor = db.get_db().execute(query, [car_id])
        car = cursor.fetchone()
        images = car['images'].split(',')
        return render_template('car-details.html', car = car, images = images)

    @app.route('/cars/reservation/<car_id>')
    def reservation_form(car_id):
        query = 'SELECT * from regions'
        cursor = db.get_db().execute(query, [])
        regions = cursor.fetchall()
        regions = list(regions)

        return render_template('reservation-form.html', regions=regions, car = car_id)


    @app.post('/reservations/submit/<car_id>')
    def submit_reservation(car_id):
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        phone = request.form['contact']
        residence_address = request.form['address']
        city = request.form['city']
        region = request.form['region']
        duration = request.form['duration']

        # TODO 1:
        # first make sure the customer id is there! (email)
        # if the custmer is there, get his id and insert it with rental info below
        # if not, create a customer and get their id 
        query = 'SELECT id from customers WHERE email=?'
        cursor = db.get_db().execute(query, [email])
        customer_id = cursor.fetchone()
        if customer_id is not None:
            # Insert into rentals table
            query = 'INSERT INTO rentals (car_id, customer_id, duration) VALUES (?,?,?)'
            cursor = db.get_db().cursor()
            cursor.execute(query, [car_id, customer_id[0], duration])
            db.get_db().commit()
        
        else:
            query = 'SELECT id from regions WHERE region=?'
            cursor = db.get_db().execute(query, [region])
            region_id = cursor.fetchone()[0]

            query = 'INSERT INTO customers (first_name, last_name, email, phone, residence_address, city, region_id) VALUES (?,?,?,?,?,?,?)'
            cursor = db.get_db().execute(query, [first_name, last_name, email, phone, residence_address, city, region_id])
            customer_id = cursor.lastrowid
            db.get_db().commit()

            query = 'INSERT INTO rentals (car_id, customer_id, duration) VALUES (?,?,?)'
            cursor = db.get_db().cursor()
            cursor.execute(query, [car_id, customer_id, duration])
            db.get_db().commit()
        
        # phase 1 : redirect user to the home page TODO 2
        return redirect('/')
        # phase 2 : create reservation-confirmation.html and direct the user there , passing the rental id.
        #           this rental id will be used in that page to retrive and display reservation info
        #           in parallel, send an email to the user
        return 
    ## TODO 3 : create reservations.html page in which we can list all reservations
    ## TODO 4 : create add-cars.html page 
    ## TODO 5 fix validation in reservation and adding cars
    ## TODO 6: add reservation-sattus in the rentals table and add cancel-reservation feature
    
    from . import db
    db.init_app(app)

    return app
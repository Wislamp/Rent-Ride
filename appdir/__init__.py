import os
from flask import Flask, render_template


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

    from . import db
    db.init_app(app)


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
        return render_template('reservation-form.html')

    return app
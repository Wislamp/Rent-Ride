DROP TABLE IF EXISTS cars;
DROP TABLE IF EXISTS rentals;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS regions;

CREATE TABLE cars (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  model TEXT NOT NULL,
  model_year INTEGER NOT NULL,
  color TEXT NOT NULL,
  rate FLOAT NOT NULL,
  rent_status TEXT NOT NULL,
  category TEXT NOT NULL
);

CREATE TABLE rentals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  car_id INTEGER NOT NULL,
  customer_id INTEGER NOT NULL,
  duration INTEGER NOT NULL,
  FOREIGN KEY (car_id) REFERENCES cars (id),
  FOREIGN KEY (customer_id) REFERENCES customers (id)
);

CREATE TABLE customers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  region_id INTEGER NOT NULL,
  rental_id INTEGER NOT NULL,
  email TEXT UNIQUE NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  phone TEXT NOT NULL,
  residence_address TEXT NOT NULL,
  city TEXT NOT NULL,
  FOREIGN KEY (region_id) REFERENCES regions (id),
  FOREIGN KEY (rental_id) REFERENCES rentals (id)
);

CREATE TABLE regions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  region TEXT NOT NULL,
);
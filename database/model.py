# model.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Cake(db.Model):
    __tablename__ = 'cake'
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    frosting = db.Column(db.String(100), nullable=False)
    decoration = db.Column(db.String(100), nullable=False)
  
class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='customer')
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='employee')
    orders = db.relationship('Order', backref='employee', lazy='dynamic')

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    cake_id = db.Column(db.Integer, db.ForeignKey('cakes.id'))
    status = db.Column(db.String(64), nullable=False)
    cancel_fee = db.Column(db.Float)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'db'
db = SQLAlchemy(app)

class Cake(db.model):
    """
    Represents the 'cake' table in the database.

    attributes:
        - id: The primary key for the cake.
        - flavor: The flavor of the cake.
        - size: The size of the cake.
        - frosting: The frosting of the cake.
        - decoration: The decoration of the cake.
    """
    __tablename__ = 'cake'
    id = db.Column(db.Integer, primary_key=True)
    flavor = db.Column(db.String(100), nullable=False)
    size = db.Column(db.String(20), nullable=False)
    frosting = db.Column(db.String(100), nullable=False)
    decoration = db.Column(db.String(100), nullable=False)
  
class Customer(db.model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='customer')
    orders = db.relationship('Order', backref='customer', lazy='dynamic')

class Employee(db.model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='employee')
    orders = db.relationship('Order', backref='employee', lazy='dynamic')

class Order(db.model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    cake_id = db.Column(db.Integer, db.ForeignKey('cakes.id'))
    status = db.Column(db.String(64), nullable=False)
    cancel_fee = db.Column(db.Float)


if __name__ == '__main__':
    app.run()
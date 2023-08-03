#!/usr/bin/env python3

from authentication.auth_tools import login_pipeline, update_passwords, hash_password
from database.db import Database
from flask import Flask, render_template, request, redirect, url_for, session
from core.session import Sessions

app = Flask(__name__)
HOST, PORT = 'localhost', 8080
global username, products, db, sessions
CUSTOMIZATION_COST = 0
username = 'default'
db = Database('database/store_records.db')
products = db.get_full_inventory()
sessions = Sessions()
sessions.add_new_session(username, db)
owners =[]

@app.route('/')
def index_page():
    """
    Renders the index page when the user is at the `/` endpoint, passing along default flask variables.

    args:
        - None

    returns:
        - None
    """
    return render_template('index.html', username=username, products=products, sessions=sessions)


@app.route('/login')
def login_page():
    """
    Renders the login page when the user is at the `/login` endpoint.

    args:
        - None

    returns:
        - None
    """
    return render_template('login.html')

@app.route('/home', methods=['POST'])
def login():
    """
    Renders the home page when the user is at the `/home` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - sessions: adds a new session to the sessions object

    """
    username = request.form['username']
    password = request.form['password']
    if login_pipeline(username, password):
        sessions.add_new_session(username, db)
        return render_template('home.html', products=products, sessions=sessions)
    else:
        password_incorrect = True
        print(f"Incorrect username ({username}) or password ({password}).")
        return render_template('login.html', password_incorrect=password_incorrect)

@app.route('/owner_login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST':
        owner_username = request.form['username']
        owner_password = request.form['password']
        if owner_username == 'owner' and owner_password == 'password':
            session['is_owner'] = True
            return redirect(url_for('owner_dashboard'))
    
    return render_template('owner_login.html')

@app.route('/owner-dashboard')
def owner_dashboard():
    if not session.get('is_owner'):
        return redirect(url_for('owner_login'))
    sales_data = []
    order_data = []

    return render_template('owner_dashboard.html', sales=sales_data, orders=order_data)

@app.route('/register')
def register_page():
    """
    Renders the register page when the user is at the `/register` endpoint.

    args:
        - None

    returns:
        - None
    """
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    """
    Renders the index page when the user is at the `/register` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - passwords.txt: adds a new username and password combination to the file
        - database/store_records.db: adds a new user to the database
    """
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    salt, key = hash_password(password)
    update_passwords(username, key, salt)
    db.insert_user(username, key, email, first_name, last_name)
    return render_template('index.html')

@app.route('/owner_register', methods=['GET', 'POST'])
def owner_register():
    if request.method == 'POST':
        owner_username = request.form['username']
        owner_password = request.form['password']
        owners.append({'username': owner_username, 'password': owner_password})
        return redirect(url_for('owner_dashboard'))

    return render_template('owner_register.html')

@app.route('/owner-dashboard')
def owner_dashboard():
    if not session.get('is_owner'):
        return redirect(url_for('owner_login'))
    
    # Fetch owner-specific data (e.g., sales, orders) from the database
    # Replace the example data with your actual data fetching logic
    sales_data = []
    order_data = []

    return render_template('owner_dashboard.html', sales=sales_data, orders=order_data)

@app.route('/shopping_cart', methods=['POST'])
def add_product_to_cart():
    order = {}
    user_session = sessions.get_session(username)
    for item in products:
     if request.form.get(str(item['id'])):
        count = int(request.form[str(item['id'])])
        if count > 0:
            cost = count * item['price']
            flavor, toppings, fillings = None, None, None
            customization_cost_flavor = None
            customization_cost_toppings = None
            customization_cost_fillings = None
            if(request.form.get("flavor-" + str(item['id']))):
                customization_cost_flavor = 0
                flavor = request.form.get("flavor-" + str(item['id']))
                if(flavor != "Vanilla"):
                    customization_cost_flavor = 10
                customization_cost_flavor *= count
                cost += customization_cost_flavor * count
            if(request.form.get("toppings-" + str(item['id']))):
                customization_cost_toppings= 0
                toppings = request.form.get("toppings-" + str(item['id']))
                if(toppings != "Sprinkles"):
                    customization_cost_toppings = 5
                customization_cost_toppings *= count
                cost += customization_cost_toppings * count
            if(request.form.get("fillings-" + str(item['id']))):
                customization_cost_fillings = 0
                fillings = request.form.get("fillings-" + str(item['id']))
                if(fillings == "Strawberry Jam"):
                    customization_cost_fillings = 20
                if(fillings == "Chocolate Ganache"):
                    customization_cost_fillings = 20 
                if(fillings == "Cream Cheese"):
                    customization_cost_fillings = 20
                customization_cost_fillings *= count
                cost += customization_cost_fillings * count
            order[item['item_name']] = {'count': count, 'cost': round(cost,2), 'image_url': item['image_url'],
                                        "flavor": flavor, "toppings":toppings, "fillings":fillings, 
                                        "customization_cost_flavor": customization_cost_flavor,
                                        "customization_cost_toppings": customization_cost_toppings,
                                        "customization_cost_fillings": customization_cost_fillings}
            user_session.add_new_item(
                item['id'], item['item_name'], round(cost,2), count)
        else:
            order.pop(item['item_name'], None)
            user_session.remove_item(item['id'])
            user_session.add_new_item(item['id'], item['item_name'], 0, 0)

    user_session.submit_cart()

    return render_template('shopping_cart.html', order=order, sessions=sessions, total_cost=user_session.total_cost)


@app.route('/checkout', methods=['POST'])
def checkout():
    """
    Renders the checkout page when the user is at the `/checkout` endpoint with a POST request.

    args:
        - None

    returns:
        - None

    modifies:
        - sessions: adds items to the user's cart
    """
    user_session = sessions.get_session(username)
    return render_template('checkout.html', total_cost=user_session.total_cost)

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)

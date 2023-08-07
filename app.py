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
order = {}
customer_info ={}

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

@app.route('/logout')
def logout_page():
    """
    Renders the login page when the user is at the `/logout` endpoint.

    args:
        - None

    returns:
        - None
    """
    return render_template('index.html', products=products)

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

@app.route('/owner_login')
def owner_login_page():
    """
    Renders the login page when the user is at the `/login` endpoint.

    args:
        - None

    returns:
        - None
    """
    return render_template('owner_login.html')

@app.route('/owner_login', methods=['GET', 'POST'])
def owner_login():
    username = request.form['username']
    password = request.form['password']
    security_code = request.form['security_code']
    error_message= None
    if login_pipeline(username, password):
        if security_code == 'ITSC3155':
            sessions.add_new_session(username, db)
            return render_template('owner_dashboard.html', products=products, sessions=sessions)
        else:
            error_message = "Sorry, wrong security code. You can't login as an owner."
            return render_template('owner_login.html', error_message=error_message)
    else:
        password_incorrect = True
        print(f"Incorrect username ({username}) or password ({password}).")
        if security_code != 'ITSC3155': 
            error_message = "Sorry, wrong security code. You can't login as an owner."
        return render_template('owner_login.html', password_incorrect=password_incorrect, error_message=error_message)

@app.route('/owner-dashboard')
def owner_dashboard():
    if not session.get('is_owner'):
        return redirect(url_for('owner_login'))
    sales_data = db.get_full_sales_information()
    order_data = db.get_orders()

    return render_template('owner_dashboard.html', sales=sales_data, orders=order_data)

@app.route('/add_to_order', methods=['POST'])
def add_to_order():
    if not session.get('is_owner'):
        return redirect(url_for('owner_login'))
    
    if request.method == 'POST':
        order_id = request.form['order_id']
        product_id = request.form['product_id']
        quantity = int(request.form['quantity'])
        db.add_product_to_order(order_id, product_id, quantity)

    # Fetch the updated order from the user session
    user_session = sessions.get_session(username)
    order = user_session.cart

    # Calculate the discounted price for each item in the order
    for item_name, item_details in order.items():
        item_cost = item_details['cost']
        if user_session.discount_applied:
            item_discounted_cost = item_cost * 0.85  # 15% discount applied
            order[item_name]['discounted_cost'] = round(item_discounted_cost, 2)
        else:
            order[item_name]['discounted_cost'] = item_cost

    
    return redirect(url_for('owner_dashboard'))

# customer registration
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
    return render_template('index.html',  products=products)

# # owner registation
# @app.route('/owner_register')
# def owner_register_page():
#     """
#     Renders the register page when the user is at the `/register` endpoint.

#     args:
#         - None

#     returns:
#         - None
#     """
#     return render_template('owner_register.html')

# @app.route('/owner_register', methods=['POST'])
# def owner_register():
#     error_message = None  # Initialize error_message
#     if request.method == 'POST':
#         owner_username = request.form['username']
#         owner_password = request.form['password']
#         security_code = request.form['security_code']

#         if security_code != 'ITSC3155': 
#             error_message = "Sorry, wrong security code. You can't register as an owner."
#         else:
#             email = request.form['email']
#             first_name = request.form['first_name']
#             last_name = request.form['last_name']
#             salt, key = hash_password(owner_password)
#             update_passwords(username, key, salt)
#             db.insert_user(username, key, email, first_name, last_name)

#             return redirect(url_for('owner_login'))

#     return render_template('owner_register.html', error_message=error_message)


@app.route('/shopping_cart', methods=['POST'])
def add_product_to_cart():
    # order = {}

    for item_name in order.keys():
        order[item_name]['image_url'] = get_image_url_for_item(item_name)

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
                cost += customization_cost_flavor
            if(request.form.get("toppings-" + str(item['id']))):
                customization_cost_toppings= 0
                toppings = request.form.get("toppings-" + str(item['id']))
                if(toppings != "Sprinkles"):
                    customization_cost_toppings = 5
                customization_cost_toppings *= count
                cost += customization_cost_toppings
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
                cost += customization_cost_fillings
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

@app.route('/confirmation_details', methods=['POST'])
def confirmation_details():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    shipping_address = request.form.get('shipping_address')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    card_number = request.form.get('card_number')
    expiration = request.form.get('expiration')
    name_on_card = request.form.get('name_on_card')
    cvv = request.form.get('cvv')

    customer_info = {
            'first_name': first_name,
            'last_name': last_name,
            'shipping_address': shipping_address,
            'email': email,
            'phone_number': phone_number,
            'card_number': card_number,
            'expiration': expiration,
            'name_on_card': name_on_card,
            'cvv': cvv,
        }
    # Fetch the discounted total from the session and round it to two decimal places
    user_session = sessions.get_session(username)
    discounted_total = round(user_session.get_discounted_total(), 2)
    
    return render_template('confirmation_details.html', order=order, customer_info=customer_info, sessions=sessions, total_cost=user_session.total_cost, discounted_total=discounted_total)

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
    # Fetch the discounted total from the user session
    user_session = sessions.get_session(username)
    total_cost = user_session.total_cost  # Get the original total cost
    discount_applied = user_session.discount_applied

    # Check if the discount is applied and adjust the total cost accordingly
    if user_session.discount_applied:
        discounted_total = total_cost * 0.85  # 15% discount
    else:
        discounted_total = total_cost

    return render_template('checkout.html', total_cost=total_cost, discount_applied=discount_applied, discounted_total=discounted_total)

def get_image_url_for_item(item_name):
    for item in products:
        if item['item_name'] == item_name:
            return item['image_url']
    return None  # Return None if the item name is not found

@app.route('/apply_discount', methods=['POST'])
def apply_discount():
    discount_code = request.form.get('discount_code')
    user_session = sessions.get_session(username)

    if discount_code == '15percent' and not user_session.discount_applied:
        user_session.apply_discount(0.15)  # 15% discount applied
        user_session.discount_applied = True

    # If the discount code is not valid or already used, render the shopping cart as it is
    total_cost = user_session.total_cost
    return render_template('shopping_cart.html', order=user_session.cart, total_cost=total_cost, sessions=sessions)


if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)

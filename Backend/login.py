from flask import Flask, request, redirect, render_template, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import fetchusers  # Import the fetchusers.py module for PDF generation

app = Flask(__name__)
app.secret_key = '12345'

# MongoDB config
app.config['MONGO_URI'] = 'mongodb://localhost:27017/role_portal'
mongo = PyMongo(app)

# Collection mapping
collections = {
    'admin': mongo.db.admins,
    'buyer': mongo.db.buyers,
    'seller': mongo.db.sellers
}

# Home route
@app.route('/')
def index():
    return render_template('login.html')  # This file must be inside 'templates' folder

# Login route
@app.route('/login', methods=['POST'])
def login():
    role = request.form.get('role')
    username = request.form.get('username')
    password = request.form.get('password')

    if role in collections:
        user = collections[role].find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['role'] = role
            flash(f'Welcome back, {username}!', 'success')
            return redirect(f'/{role}_dashboard')
    flash('Invalid credentials for selected role.', 'error')
    return redirect('/')

# Signup route
@app.route('/signup', methods=['POST'])
def signup():
    role = request.form.get('role')
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('new_password')
    confirm = request.form.get('confirm_password')

    if password != confirm:
        flash('Passwords do not match.', 'error')
        return redirect('/')

    if role in collections:
        if collections[role].find_one({'username': username}):
            flash('Username already exists.', 'error')
            return redirect('/')
        hashed_password = generate_password_hash(password)
        collections[role].insert_one({
            'email': email,
            'username': username,
            'password': hashed_password
        })
        flash('Account created successfully! Please log in.', 'success')

        # Call the function to regenerate the PDF after signup
        fetchusers.fetch_and_generate_pdf()  # Regenerate the report

    else:
        flash('Invalid role.', 'error')

    return redirect('/')

# Dashboard routes
@app.route('/admin_dashboard')
def admin_dashboard():
    return f"Hello Admin: {session.get('username')}"

@app.route('/buyer_dashboard')
def buyer_dashboard():
    return f"Hello Buyer: {session.get('username')}"

@app.route('/seller_dashboard')
def seller_dashboard():
    return f"Hello Seller: {session.get('username')}"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

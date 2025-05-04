from flask import Flask, request, redirect, render_template, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import fetchusers  # Make sure this module is in the same folder

app = Flask(__name__)
app.secret_key = '12345'

# MongoDB config
app.config['MONGO_URI'] = 'mongodb://localhost:27017/role_portal'
mongo = PyMongo(app)

# Collection mapping
collections = {
    'admin': mongo.db.admins,
    'buyer': mongo.db.buyers,
    'producers': mongo.db.producers
}

# Home route (Login Page)
@app.route('/')
def index():
    return render_template('buyer_templates/login.html')

# Login POST route
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
        fetchusers.fetch_and_generate_pdf()
    else:
        flash('Invalid role.', 'error')

    return redirect('/home')

# Home Page after login
@app.route('/home')
def home():
    if 'username' in session:
        return render_template('buyer_templates/home.html', username=session['username'], role=session['role'])
    flash('Please log in first.', 'error')
    return redirect('/')

# Dashboards
@app.route('/admin_dashboard')
def admin_dashboard():
    if 'username' in session:
        return render_template('buyer_templates/home.html', username=session['username'])
    return redirect('/')

@app.route('/buyer_dashboard')
def buyer_dashboard():
    if 'username' in session:
        return render_template('buyer_templates/home.html', username=session['username'])
    return redirect('/')

@app.route('/seller_dashboard')
def seller_dashboard():
    if 'username' in session:
        return render_template('buyer_templates/home.html', username=session['username'])
    return redirect('/')

# Marketplace Page
@app.route('/marketplace')
def marketplace():
    if 'username' in session:
        return render_template('buyer_templates/marketplace.html', username=session['username'])
    flash('Please log in first.', 'error')
    return redirect('/')

# Visual Page
@app.route('/visual')
def visual():
    if 'username' in session:
        return render_template('buyer_templates/visual.html', username=session['username'])
    flash('Please log in first.', 'error')
    return redirect('/')

# TN Visualization
@app.route('/tn_visualization')
def tn_visualization():
    return render_template('buyer_templates/TN_visualization.html')

# Separate login GET (in case needed)
@app.route('/login')
def login_():
    return render_template('buyer_templates/login.html')

# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)

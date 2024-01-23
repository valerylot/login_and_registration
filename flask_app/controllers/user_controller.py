from flask_app import app
from flask import Flask, render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_bcrypt import Bcrypt 
bcrypt = Bcrypt(app)

# THIS IS THE HOME PAGE THAT DISPLAYS THE LOGIN AND REGISTRATION FORMS
@app.route('/')
def index():
    return render_template('index.html')


# THIS IS TO CREATE A USER 
@app.route('/users/registration', methods=['POST'])
def registration():
    if not User.validate_user(request.form):
        return redirect('/')


# THIS IS THE BCRYPT PART
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    new_user = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : pw_hash
    }

    user_id = User.create_user(new_user)
    session['user_id'] = user_id

    return redirect('/dashboard ')

# THIS SAVES THE DATA, IF EVERYTHING GOES THRU
    # User.save(request.form)
    # return redirect('/registration')


# THIS REDIRECTS US TO DASHBOARD.HTML
@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user_id = session['user_id']

        data = {
            'user_id' : user_id
        }
        current_user = User.get_user_by_id(data)
        return render_template('dashboard.html', current_user = current_user)
# BECAUSE WE SAVED IT AS CURRENT_USER, NOW WE CAN USE IT IN JINJA
    else:
        return redirect('/')

# NOW TO VALIDATE, WE NEED A STATICMETHOD CALLED validate_user in our model
    
# NEED A ROUTE TO VALIDATE THE LOGIN FORM SEPARATELY
@app.route('/users/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email']
    }

    user_in_db = User.read_one_user_by_email(data)

    if not user_in_db:
        flash("Invalid email or password.", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid email or password.", "login")
        return redirect('/')
    
    session['user_id'] = user_in_db.id

    return redirect('/dashboard')

# THIS DESTROYS A SESSION
@app.route('/logout')
def destroy_session():
    session.clear()
    return redirect ('/')
from flask import Blueprint, render_template, request,redirect,url_for,flash,session
from flask_login import login_required, current_user,logout_user,login_user
from .model import User
from . import db
import os

auth = Blueprint('auth', __name__)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')

        username_exists = User.query.filter_by(username=username).first()

        if username_exists:
            flash('Username already exists. Please choose a different one.',category='error')
            return redirect(url_for('auth.signup'))
        else:
            new_user = User(name=name,username=username,password=password,role=1)

            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html')
    
# request {
# method: 'POST',
# form:{
#     'name': 'John Doe',
#     'username': 'johndoe',
#     'password': 'securepassword'
# }
# }

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            if user.password == password:
                if user.role == 0:
                    print('admin logged in successfully')
                    login_user(user)
                    return redirect('/admin_dashboard')
                else:
                    print('customer logged in successfully')
                    login_user(user)
                    return redirect('/customer_dashboard')
            else:
                flash('Incorrect password. Please try again.', category='error')
                return redirect(url_for('auth.login'))
        else:
            flash('Username does not exist. Please sign up.', category='error')
            return redirect(url_for('auth.signup'))
    else:
        return render_template('login.html')
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
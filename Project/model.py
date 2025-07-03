from flask_login import UserMixin
from . import db
from flask import current_app
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.Numeric())
    # admin role = 0, customer = 1

    @staticmethod
    def create_admin_user():
        with current_app.app_context():
            if User.query.filter_by(username='admin').first() is None:
                admin_user = User(username='admin',password='admin',name='Admin',role=0)
                db.session.add(admin_user)
                db.session.commit()

                print("Admin user created successfully.")
            else:
                print("Admin user already exists.")

class Cateogories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Numeric(), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('cateogories.id'), nullable=False)
    category = db.relationship('Cateogories', backref=db.backref('products', lazy=True))                
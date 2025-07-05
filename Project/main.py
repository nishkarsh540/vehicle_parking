from flask import Blueprint, render_template, request, redirect, url_for,flash,abort
from . import db
from .model import User, Cateogories
from flask_login import login_required,current_user

main = Blueprint('main',__name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/admin/manage_cat',methods=['GET','POST'])
@login_required
def manage_cat():
    if request.method == 'POST':
        if 'create_category' in request.form:
            category_name = request.form.get('create_category')

            existing_category = Cateogories.query.filter_by(name=category_name).first()

            if existing_category:
                flash('Category already exists.', category='error')
            else:
                new_category = Cateogories(name= category_name)
                db.session.add(new_category)
                db.session.commit()
                flash('Category created successfully!', category='success')
        elif 'remove_category' in request.form:
            category_id = request.form.get('category_id')
            category = Cateogories.query.get(category_id)

            if category:
                db.session.delete(category)
                db.session.commit()
                flash('Category removed successfully!', category='success')
            else:
                flash('Category not found.', category='error')
        elif 'update_category' in request.form:
            category_id = request.form.get('category_id')
            new_category_name = request.form.get('new_category_name')
            category = Cateogories.query.get(category_id)

            if category:
                category.name = new_category_name
                db.session.commit()
                flash('Category updated successfully!', category='success')
            else:
                flash('Category not found.', category='error')
        return redirect(url_for('main.manage_cat'))
    if not current_user.role == 0:
        abort(403)

    categories = Cateogories.query.all()

    return render_template('manage_cat.html', categories= categories)
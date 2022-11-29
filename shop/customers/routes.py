from flask import render_template,session, request,redirect,url_for,flash,current_app,make_response
from flask_login import login_required, current_user, logout_user, login_user
from flask_babel import _
from shop import app,db,search,bcrypt,login_manager
from .forms import CustomerRegisterForm, CustomerLoginFrom
from shop.products.models import Category, Addproduct, Register
import secrets
import os
import json

def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories


@app.route('/customer/register', methods=['GET','POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(name=form.name.data, password=hash_password, contact=form.contact.data)
        db.session.add(register)
        db.session.commit()
        return redirect(url_for('customerLogin'))
    return render_template('customer/register.html', form=form, categories=categories())


@app.route('/customer/login', methods=['GET','POST'])
def customerLogin():
    form = CustomerLoginFrom()
    if form.validate_on_submit():
        user = Register.query.filter_by(contact=form.contact.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash(_('Nädogry telefon ýada açar söz'))
        return redirect(url_for('customerLogin'))

    return render_template('customer/login.html', form=form, categories=categories())


@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/customer/<name>', methods=['GET', 'POST'])
@login_required
def aboutCustomer(name):
    user = Register.query.filter_by(name=name).first_or_404()
    return render_template('customer/aboutcustomer.html', user=user, categories=categories())


def updateshoppingcart():
    for key, shopping in session['Shoppingcart'].items():
        session.modified = True
        del shopping['image']
    return updateshoppingcart


@app.route('/language/<language>')
def set_language(language=None):
	session['language'] = language
	if language == 'tk':
		language == 'tk'
	else:
		language == 'ru'
	return redirect(request.referrer)


@app.route('/admin/customers', methods=['GET'])
def get_customers():
    clients = Register.query.all()
    return render_template('customer/customers.html', clients=clients, categories=categories())


@app.route('/admin/customer/<int:id>', methods=['GET','POST'])
def deletecustomer(id):
    customer = Register.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(customer)
        db.session.commit()
        return redirect(url_for('get_customers'))
    return redirect(url_for('admin'))

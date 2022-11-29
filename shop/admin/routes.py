from flask import render_template,session, request,redirect,url_for,flash
from shop import app,db,bcrypt
from .forms import RegistrationForm,LoginForm
from .models import User
from shop.products.models import Addproduct,Category,Image, Subcategory


@app.route('/admin/')
def admin():
    if 'email' not in session:
        flash(f'Ilkinji içeri giriň','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.order_by(Addproduct.approved).all()
    images = Image.query.all()
    return render_template('admin/index.html', title='Admin page',products=products, images=images)


@app.route('/admin/approveimages/<int:id>', methods=['GET'])
def get_images(id):
    if 'email' not in session:
        flash(f'Ilkinji içeri giriň','danger')
        return redirect(url_for('login'))
    products = Addproduct.query.get_or_404(id)
    return render_template('admin/approve_images.html', products=products)


@app.route('/admin/categories')
def categories():
    if 'email' not in session:
        flash(f'Ilkinji içeri giriň','danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='categories',categories=categories)


@app.route('/admin/registernewuser', methods=['GET', 'POST'])
def register():
    # if 'email' not in session:
    #     flash(f'Please firstly login','danger')
    #     return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name=form.name.data,username=form.username.data, email=form.email.data,
                    password=hash_password)
        db.session.add(user)
        flash(f'Hoş geldiňiz {form.name.data} Registrasiýa bolanynyň üçin minnetdar','success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('admin/register.html',title='Register user', form=form)


@app.route('/admin/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Hoş geldiňiz {form.email.data} içeri girdiňiz','success')
            return redirect(url_for('admin'))
        else:
            flash(f'Nädogry email ýada parol', 'success')
            return redirect(url_for('login'))
    return render_template('admin/login.html',title='Login page',form=form)


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/admin/admins', methods=['GET'])
def admins():
    admins = User.query.all()
    return render_template('admin/admins.html', admins=admins)


@app.route('/admin/banners', methods=['GET', 'POST'])
def banners():
    banners = Banner.query.all()
    return render_template('admin/banners.html', banners=banners)

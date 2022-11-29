from flask import render_template,session, request,redirect,url_for,flash,current_app
from shop import app,db,search
from .models import Category,Addproduct,Register, Image, Subcategory
from .forms import Addproducts
import secrets
import os
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
import urllib.request


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories

def subcategories():
    subcategories = Subcategory.query.join(Addproduct,(Subcategory.id == Addproduct.subcategory_id)).all()
    return subcategories


@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page',1, type=int)
    products = Addproduct.query.order_by(Addproduct.price.desc()).paginate(page=page, per_page=28)
    return render_template('products/index.html', products=products, categories=categories(), subcategories=subcategories())


@app.route('/result')
def result():
    searchword = request.args.get('q')
    products = Addproduct.query.msearch(searchword, fields=['name'] , limit=28)
    return render_template('products/result.html',products=products, categories=categories())


@app.route('/product/<int:id>')
def single_page(id):
    product = Addproduct.query.get_or_404(id)
    return render_template('products/single_page.html',product=product, categories=categories())


@app.route('/categories/<int:id>')
def get_category(id):
    page = request.args.get('page',1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = Addproduct.query.filter_by(category=get_cat).paginate(page=page, per_page=28)
    return render_template('products/index.html',get_cat_prod=get_cat_prod,categories=categories(),get_cat=get_cat)


@app.route('/addcat',methods=['GET','POST'])
def addcat():
    if 'email' not in session:
        flash('Birinji ulgama giriň','danger')
        return redirect(url_for('login'))
    if request.method =="POST":
        getcat = request.form.get('category')
        category = Category(name=getcat)
        db.session.add(category)
        db.session.commit()
        return redirect(url_for('addsubcat'))
    return render_template('products/addbrand.html', title='Add category')


@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Birinji ulgama giriň','danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method =="POST":
        updatecat.name = category
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('products/addbrand.html', title='Update category',categories='categories',updatecat=updatecat)



@app.route('/addsubcat', methods=['GET', 'POST'])
def addsubcat():
    if 'email' not in session:
        return redirect(url_for('login'))
    categories = Category.query.all()
    if request.method == 'POST':
        addsubcategory = request.form.get('addsubcategory')
        category = request.form.get('category')
        subcategories = Subcategory(names=addsubcategory, category_id=category)
        db.session.add(subcategories)
        db.session.commit()
        return redirect(url_for('addsubcat'))
    return render_template('products/addsubcategory.html', categories=categories)


    
@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    if 'email' not in session:
        flash('Birinji ulgama giriň','danger')
        return redirect(url_for('login'))
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('admin'))

    
# ADDING PRODUCT ROUTE
@app.route('/addproduct', methods=['GET','POST'])
@login_required
def addproduct():
    form = Addproducts(request.form)
    categories = Category.query.all()
    subcategories = Subcategory.query.all()
    if request.method=="POST":
        files = request.files.getlist('files[]')
        file_names = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_names.append(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                print('Success')
                img = Image(img=file.read(), name=filename)
                db.session.add(img)
                db.session.commit()
        name = form.name.data
        price = form.price.data
        desc = form.description.data
        category = request.form.get('category')
        subcategory = request.form.get('subcategory')
        addproduct = Addproduct(name=name,price=price,desc=desc,category_id=category,subcategory_id=subcategory,author=current_user)
        db.session.add(addproduct)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('products/addproduct.html', form=form, title='Add a Product', categories=categories, subcategories=subcategories)


@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    if 'email' not in session:
        flash('Birinji ulgama giriň','danger')
        return redirect(url_for('login'))
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.desc = form.description.data
        product.category_id = category
        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('home'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.description.data = product.desc
    category = product.category.name
    return render_template('products/addproduct.html', form=form, title='Update Product',getproduct=product,categories=categories)


@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            print(e)
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('admin'))
    flash(f'Maglumaty pozmak mümkinçiligi ýok','success')
    return redirect(url_for('admin'))


@app.route('/myproducts/<name>', methods=['GET'])
def myproducts(name):
    user = Register.query.filter_by(name=name).first_or_404()
    posts = user.posts.order_by(Addproduct.price.desc())
    return render_template('products/myproducts.html', posts=posts, user=user)


@app.route('/approved/<int:id>', methods=['GET', 'POST'])
def approved_product(id):
    if 'email' not in session:
        flash('Birinji ulgama giriň','danger')
        return redirect(url_for('login'))
    product = Addproduct.query.get_or_404(id)
    product.approved = True
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/cancel/<int:id>', methods=['GET', 'POST'])
def approved_cancel(id):
    if 'email' not in session:
        flash('Birinji ulgama giriň','danger')
        return redirect(url_for('login'))
    product = Addproduct.query.get_or_404(id)
    product.approved = False
    db.session.commit()
    return redirect(url_for('admin'))


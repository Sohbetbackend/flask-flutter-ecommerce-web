from shop import db, login_manager, ma
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)


#USERS ADDING PRODUCT 
class Addproduct(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)
    register_id = db.Column(db.Integer, db.ForeignKey('register.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'),nullable=False)
    subcategory = db.relationship('Subcategory',backref=db.backref('subcategories', lazy=True))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))

    def __repr__(self):
        return '<Addproduct %r>' % self.name


# UPLOADING IMAGES
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    img = db.Column(db.Text)
    addproduct = db.relationship('Addproduct', backref=db.backref('addproducts', lazy=True))
    


#Kategoriya table
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)


    def __repr__(self):
        return '<Category %r>' % self.name


# SUBCATEGORY TABLE
class Subcategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(64))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categoriess', lazy=True))



#Ulanyjy registrasiya table
class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    password = db.Column(db.String(200), unique= False)
    contact = db.Column(db.String(50), unique= False)
    posts = db.relationship('Addproduct', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<Register %r>' % self.name




db.create_all()


from shop import db, login_manager, ma
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)


#Towar goshmak uchin table
class Addproduct(db.Model):
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    discount = db.Column(db.Integer, default=0)
    desc = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    approved = db.Column(db.Boolean, default=False)
    register_id = db.Column(db.Integer, db.ForeignKey('register.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),nullable=False)
    category = db.relationship('Category',backref=db.backref('categories', lazy=True))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'),nullable=False)
    brand = db.relationship('Brand',backref=db.backref('brands', lazy=True))

    image_1 = db.Column(db.String(260), default='image1.jpg')
    image_2 = db.Column(db.String(150), default='image2.jpg')
    image_3 = db.Column(db.String(150), default='image3.jpg')


    def __repr__(self):
        return '<Addproduct %r>' % self.name


#Brend table
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __repr__(self):
        return '<Brand %r>' % self.name


#Kategoriya table
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    image_category = db.Column(db.String(100))


    def __repr__(self):
        return '<Category %r>' % self.name




#Ulanyjy registrasiya table
class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50), unique= False)
    password = db.Column(db.String(200), unique= False)
    contact = db.Column(db.String(50), unique= False)
    posts = db.relationship('Addproduct', backref='author', lazy='dynamic')


    def __repr__(self):
        return '<Register %r>' % self.name

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text)

    def __repr__(self):
        return '<Banner %r>' % self.image




db.create_all()


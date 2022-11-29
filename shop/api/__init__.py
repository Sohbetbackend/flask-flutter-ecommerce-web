from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from shop import db, app, api, ma
from shop.products.models import Addproduct, Category, Register


class AddproductSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "desc", "category_id", "brand_id", "register_id", "approved")
        model = Addproduct


product_schema = AddproductSchema()
products_schema = AddproductSchema(many=True)


class ProductListResource(Resource):
    def get(self):
        products = Addproduct.query.all()
        return products_schema.dump(products)


class ProductResource(Resource):
    def get(self, product_id):
        product = Addproduct.query.get_or_404(product_id)
        return product_schema.dump(product)


class CategorySchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "image_category")
        model = Category

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)


class CategoryListResource(Resource):
    def get(self):
        categories = Category.query.all()
        return categories_schema.dump(categories)


class CategoryResource(Resource):
    def get(self, category_id):
        category = Category.query.get_or_404(category_id)
        return category_schema.dump(category)

    
class RegisterSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "contact")
        model = Register
    
register_schema = RegisterSchema()
registers_schema = RegisterSchema(many=True)

class RegisterListResource(Resource):
    def get(self):
        registers = Register.query.all()
        return registers_schema.dump(registers)
    
class RegisterResource(Resource):
    def get(self, register_id):
        register = Register.query.get_or_404(register_id)
        return register_schema.dump(register)


api.add_resource(ProductListResource, '/api/products')
api.add_resource(ProductResource, '/api/products/<int:product_id>')
api.add_resource(CategoryListResource, '/api/categories')
api.add_resource(CategoryResource, '/api/categories/<int:category_id>')
api.add_resource(RegisterListResource, '/api/users')
api.add_resource(RegisterResource, '/api/users/<int:register_id>')

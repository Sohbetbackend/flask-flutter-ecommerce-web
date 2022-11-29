from flask import Flask, request, json, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from shop import db, app, api, ma
from shop.products.models import Addproduct, Category, Register


@app.route('/api/register', methods=['GET', 'POST'])
def api_register():
    d={}
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        phone = request.form['phone']

        phone = Register.query.filter_by(phone=phone).first()

        if phone is None:
            register = Register(name=name, password=password, phone=phone)

            db.session.add(register)
            db.session.commit()

            return jsonify(["Register success"])
        else:

            return jsonify(["User already exists!"])


@app.route('/api/login', methods=['GET', 'POST'])
def api_login():
    d = {}
    if request.method == "POST":
        phone = request.form['phone']
        password = request.form['password']

        login = Register.query.filter_by(phone=phone, password=password).first()

        if login is None:

            return jsonify(["Wrong Credentials"])
        else:

            return jsonify(["Success"]) 

import unittest 
from datetime import datetime, timedelta
from shop import app, db
from shop.products.models import Addproduct, Brand, Category, Register


class Test():
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class RegisterModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(Test)
        self.app_context = self.shop.app_context
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register(self):
        r = Register(name='john', contact='64545533')

    def test_post(self):
        a = Addproduct(name="alma", price="12", phone="6666", desc="yasyl alma")

    
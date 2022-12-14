from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
import os
from flask_msearch import Search
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from flask_moment import Moment
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/productsimage')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/ecommerce'
app.config['SECRET_KEY']='hfouewhfoiwefoquw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['LANGUAGES'] = ['tk', 'ru']


db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
search = Search()
babel = Babel(app)
moment = Moment(app)
search.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view='customerLogin'
login_manager.needs_refresh_message_category='danger'
login_manager.login_message = _l(u"Please login first")


@babel.localeselector
def get_locale():
    try:
        language = session['language']
    except KeyError:
        language = None
    if language:
        return language
    return 'tk'


from shop.products import routes, errors
from shop.admin import routes
from shop.customers import routes
from shop.api import routes


@app.context_processor
def inject_conf_var():
    return dict(
        AVAILABLE_LANGUAGE=app.config['LANGUAGES'],
        CURRENT_LANGUAGE=session.get('language', 'tk')
    )


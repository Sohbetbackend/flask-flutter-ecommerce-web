from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed
from flask_babel import lazy_gettext as _l

class Addproducts(Form):
    name = StringField(_l('Ady'), [validators.DataRequired()])
    price = FloatField(_l('Bahasy'), [validators.DataRequired()])
    discount = IntegerField(_l('Arzanladyş'), default=0)
    description = TextAreaField(_l('Giňişleýin'), [validators.DataRequired()])


class Banner(Form):
    name = StringField('Bannerin ady', [validators.DataRequired()])
    image = FileField('Image', validators=[FileAllowed(['jpg','png','gif','jpeg']), 'Haýyş edýäs diňeje surat'])
    
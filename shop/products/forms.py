from wtforms import Form, SubmitField,IntegerField,FloatField,StringField,TextAreaField,validators
from flask_wtf.file import FileField,FileRequired,FileAllowed
from flask_babel import lazy_gettext as _l

class Addproducts(Form):
    name = StringField(_l('Ady'), [validators.DataRequired()])
    price = FloatField(_l('Bahasy'), [validators.DataRequired()])
    phone = IntegerField(_l('Telefon'), [validators.DataRequired(), validators.Length(min=8)])
    discount = IntegerField(_l('Arzanladyş'), default=0)
    description = TextAreaField(_l('Giňişleýin'), [validators.DataRequired()])

    image_1 = FileField(_l('Surat 1'), validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg']), 'Haýyş edýäs diňeje surat'])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg','png','gif','jpeg']), 'Haýyş edýäs diňeje surat'])
    # image_3 = FileField('Image 3', validators=[FileAllowed(['jpg','png','gif','jpeg']), 'Haýys edýäs diňeje surat'])


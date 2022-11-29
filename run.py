from shop import app, db
from shop.products.models import Addproduct, Category, Register
from shop.admin.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Addproduct': Addproduct, 'Category': Category, 'Register': Register, 'User': User}


if __name__ =="__main__":
    app.run(debug='True', host='0.0.0.0', port=5000)

from shop import app, db
from shop.products.models import Addproduct, Brand, Category, Register
from shop.admin.models import User


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Addproduct': Addproduct, 'Brand': Brand, 'Category': Category, 'Register': Register, 'User': User}


if __name__ =="__main__":
    app.run(debug=True)

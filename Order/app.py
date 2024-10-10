from flask import Flask
from routes import order_blueprint
from models import db, init_app

app = Flask(__name__)
#app.config['SECRET_KEY']='6f31f270fbe1f48b075e518eb11d19fa3d9f5a49ba4f67d31e851bca257df839'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root89%40@localhost/order_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

app.register_blueprint(order_blueprint)
init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=5003)
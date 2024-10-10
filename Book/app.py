from flask import Flask
from routes import book_blueprint
import models
from flask_login import LoginManager

app = Flask(__name__)
#app.config['SECRET_KEY']='6f31f270fbe1f48b075e518eb11d19fa3d9f5a49ba4f67d31e851bca257df839'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root89%40@localhost/books_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
models.init_app(app)
app.register_blueprint(book_blueprint)
login_manager=LoginManager(app)



if __name__ == '__main__':
    app.run(debug=True)
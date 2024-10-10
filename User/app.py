#User/app.py

#Library
import mysql.connector
import pymysql
from flask import Flask
from flask import Flask
from flask.sessions import SecureCookieSessionInterface
from flask_migrate import Migrate
from flask_login import LoginManager
import models
from routes import user_blueprint

#Connection with MySQL
app=Flask(__name__)
app.config['SECRET_KEY']='6f31f270fbe1f48b075e518eb11d19fa3d9f5a49ba4f67d31e851bca257df839'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root89%40@localhost/new_users-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources

models.init_app(app)
app.register_blueprint(user_blueprint)
login_manager=LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.filter_by(id=user_id).first()

@login_manager.request_loader
def load_user_from_request(request):
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        user = models.User.query.filter_by(api_key=api_key).first()
        if user:
            return user

    return None


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, **kwargs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from flask_mail import Mail
import flask_whooshalchemy as wa 
from Main.config import config 
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view= 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
def create_app():
	app = Flask(__name__)
	with app.app_context():
		app.config.from_object(config)
		db.init_app(app)
		db.create_all()
		bcrypt.init_app(app)
		login_manager.init_app(app)
		mail.init_app(app)
		from Main.users.routes import users
		from Main.posts.routes import posts
		from Main.index.routes import index
		from Main.errors.handlers import errors
		app.register_blueprint(users)
		app.register_blueprint(posts)
		app.register_blueprint(index)
		app.register_blueprint(errors)
	return app
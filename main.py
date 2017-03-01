import os
from flask import Flask
from shared_objects import db
from constants import Constants
from shared_objects import mail
from shared_objects import passlib
from shared_objects import swagger_app
from flask_restful import Api as FlaskApi

from user_resource import UserResource
from login_resource import LoginResource
from group_resource import GroupResource
from expense_resource import ExpenseResource
from category_resource import CategoryResource
from user_update_resource import UserUpdateResource
from group_update_resource import GroupUpdateResource
from budget_limit_resource import BudgetLimitResource
from category_limit_resource import CategoryLimitResource
from expense_update_resource import ExpenseUpdateResource
from category_update_resource import CategoryUpdateResource
from registration_email_resource import RegistrationEmailResource
from budget_limit_update_resource import BudgetLimitUpdateResource
from category_limit_update_resource import CategoryLimitUpdateResource
from send_registration_email_resource import SendRegistrationEmailResource

from flask_passlib import LazyCryptContext
from flask_passlib.context import werkzeug_salted_md5
from flask_passlib.context import werkzeug_salted_sha1
from flask_passlib.context import werkzeug_salted_sha256
from flask_passlib.context import werkzeug_salted_sha512


def add_resource(obj, path):
    swagger_app.add_resource(obj, path)
    flask_resource_api.add_resource(obj, path)

os.environ.setdefault('DATABASE_URL', 'postgresql://localhost/postgres')

flask_app = Flask(__name__)
flask_app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
flask_app.config['BUNDLE_ERRORS'] = True
flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
flask_app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False,
    MAIL_USERNAME=Constants.project_email,
    MAIL_PASSWORD='ShareBudgetTS',
))

flask_resource_api = FlaskApi(flask_app)

db.init_app(flask_app)
with flask_app.app_context():
    # Extensions like Flask-SQLAlchemy now know what the "current" app
    db.create_all()

swagger_app.init_app(flask_app)

passlib.init_app(flask_app, context=LazyCryptContext(
    schemes=[
        werkzeug_salted_md5,
        werkzeug_salted_sha1,
        werkzeug_salted_sha256,
        werkzeug_salted_sha512,
    ],
    default='werkzeug_salted_sha512',))

mail.init_app(flask_app)

add_resource(UserResource, '/user')
add_resource(LoginResource, '/login')
add_resource(GroupResource, '/group')
add_resource(ExpenseResource, '/expense')
add_resource(CategoryResource, '/category')
add_resource(UserUpdateResource, '/user/updates')
add_resource(BudgetLimitResource, '/group/limit')
add_resource(GroupUpdateResource, '/group/updates')
add_resource(CategoryLimitResource, '/category/limit')
add_resource(ExpenseUpdateResource, '/expense/updates')
add_resource(CategoryUpdateResource, '/category/updates')
add_resource(BudgetLimitUpdateResource, '/group/limit/updates')
add_resource(CategoryLimitUpdateResource, '/category/limit/updates')
add_resource(SendRegistrationEmailResource, '/registration/sendemail')
add_resource(RegistrationEmailResource, Constants.k_registration_resource_path)

if __name__ == '__main__':
    flask_app.run(debug=True)
from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from utils.db import init_db
from apis.user_api import user_ns, get_user_by_id
from apis.expense_api import expense_ns

def create_app(config_object='config.DevelopmentConfig'): # Default configuration

  app = Flask(__name__)
  jwt = JWTManager(app)
  api = Api(app, version = '1.0', title = 'BBHMM API', description = 'A Splitwise clone API')

  app.config.from_object(config_object)

  # Initialize the postgreSQL database
  with app.app_context():
    init_db()

  # Register namespaces
  api.add_namespace(user_ns, path = '/users')
  api.add_namespace(expense_ns, path = '/expenses')

  @jwt.user_identity_loader
  def user_identity_lookup(user):
    return user['id']

  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return get_user_by_id(identity)
  
  return app

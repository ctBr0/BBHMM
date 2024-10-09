from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from utils.db import init_db
from resources.user_resource import user_ns
from resources.expense_resource import expense_ns

app = Flask(__name__)
jwt = JWTManager(app)
api = Api(app, version = '1.0', title = 'BBHMM API', description = 'A Splitwise clone API')

app.config.from_object('config.DevelopmentConfig')

# Initialize the postgreSQL database
with app.app_context():
  init_db()

# Register namespaces
api.add_namespace(user_ns, path = '/users')
api.add_namespace(expense_ns, path = '/group-expenses')

if __name__ == '__main__':
  app.run()
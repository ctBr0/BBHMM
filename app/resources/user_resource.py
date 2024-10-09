from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token
from utils.bcrypt_helper import hash_password, check_password
from utils.db import get_db

user_ns = Namespace('users', description="User operations")

user_model = user_ns.model('user', {
  'name': fields.String,
  'email': fields.String,
  'password': fields.String
})

@user_ns.route('/register')
class UserRegister(Resource):

  @user_ns.expect(user_model)
  def post(self):
    data = user_ns.payload
    hashed_password = hash_password(data['password'])
    
    with get_db() as conn:
      with conn.cursor() as cur:
        cur.execute("""
          INSERT INTO "user" (name, email, hashed_password) 
          VALUES (%s, %s, %s) 
          RETURNING id;
        """, (data['name'], data['email'], hashed_password))
        user_id = cur.fetchone()[0]
        conn.commit()
            
    return {'message': 'User created', 'user_id': user_id}, 201

"""

@user_ns.route('/login')
class UserLogin(Resource):

  @user_ns.expect(user_model)
  def post(self):
    data = user_ns.payload

    with get_db() as conn:
      with conn.cursor() as cur:
        cur.execute
          SELECT * FROM \"user\" WHERE email = %s;     
        , (data['email'],))
        user = cur.fetchone()

    if user and check_password(data['password'], user['password']):
      access_token = create_access_token(identity=user['id'])
      return {'access_token': access_token}, 200
    return {'message': 'Invalid credentials'}, 401
  
"""

"""
  @user_ns.route('logout')
  class UserLogout(Resource):

    def post(self):
"""


  
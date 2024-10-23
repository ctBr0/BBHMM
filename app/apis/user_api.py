from flask_restx import Resource, Namespace, fields
from flask_jwt_extended import create_access_token
from utils.bcrypt_helper import hash_password, check_password
from utils.db import get_db, close_db
from psycopg.rows import dict_row
from psycopg import errors

user_ns = Namespace('users', description="User operations")

user_model = user_ns.model('user_model', {
  'name': fields.String,
  'email': fields.String,
  'password': fields.String
})

login_model = user_ns.model('login_model', {
  'email': fields.String,
  'password': fields.String
})

def get_user_by_id(user_id):

  with get_db() as conn:
    with conn.cursor(row_factory=dict_row) as cur:
      cur.execute(
        """
        SELECT * 
        FROM \"user\" 
        WHERE id = %s;
        """,
        (user_id,))
      user = cur.fetchone()
    
  # required for jwt_required
  close_db() 
  
  return user

@user_ns.route('/register')
class UserRegister(Resource):

  @user_ns.doc(description = "Create a user account.")
  @user_ns.expect(user_model)
  def post(self):
      
    try:
      data = user_ns.payload
      hashed_password = hash_password(data['password'])
      
      with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
          cur.execute(
            """
            INSERT INTO \"user\" (name, email, hashed_password) 
            VALUES (%s, %s, %s);
            """,
            (data['name'], data['email'], hashed_password,))
          conn.commit()
              
      return {"message": "User successfully registered!"}, 201
    
    except errors.UniqueViolation as e:
      return {"message": "Email already exists!", "error": str(e)}, 409
    
    except errors.DatabaseError as e:
      # Handle general database errors
      return {"message": "Database error occurred!", "error": str(e)}, 500

    except Exception as e:
      # Handle any other exceptions
      return {"message": "An error occurred!", "error": str(e)}, 500

@user_ns.route('/login')
class UserLogin(Resource):

  @user_ns.doc(description = "Log in to account.")
  @user_ns.expect(login_model)
  def post(self):

    try:
      data = user_ns.payload

      with get_db() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
          cur.execute(
            """
            SELECT * FROM \"user\"
            WHERE email = %s;     
            """,
            (data['email'],))
          user = cur.fetchone()
          conn.commit()

      if not user:
        return {"message": "User does not exist!"}, 401
      
      else:
        if check_password(data['password'], user['hashed_password']):
          access_token = create_access_token(user)
          return {"message": "Successfully logged in!", "access_token": access_token}, 200
        
        else:
          return {"message": "Incorrect password!"}, 401
    
    except errors.DatabaseError as e:
      # Handle general database errors
      return {"message": "Database error occurred!", "error": str(e)}, 500

    except Exception as e:
      # Handle any other exceptions
      return {"message": "An error occurred!", "error": str(e)}, 500
      
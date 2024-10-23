import pytest
from psycopg.rows import dict_row
from mock_data import *

# Using relative path
from utils.db import get_db # type: ignore

# Test successful registration
@pytest.mark.integration
def test_register_success(client, app):

  # Send the POST request to the register endpoint
  response = client.post('/users/register', json = mock_user_data_1)
  
  with app.app_context():
    # Assert response status code and message
    assert response.status_code == 201
    assert response.json['message'] == "User successfully registered!"
  
  with app.app_context():
    # Verify that the user was inserted into the database
    with get_db() as conn:
      with conn.cursor(row_factory = dict_row) as cur:
        cur.execute(
          """
            SELECT * 
            FROM \"user\" 
            WHERE email = %s;
          """,
          (mock_user_data_1['email'],))
        user = cur.fetchone()
        assert user is not None
        assert user['name'] == mock_user_data_1['name']
        assert user['email'] == mock_user_data_1['email']

# Test registration with an existing email (unique constraint violation)
@pytest.mark.integration
def test_register_duplicate_email(client, app):

  # Register a new user
  client.post('/users/register', json = mock_user_data_1)

  # Try to register the same email again
  response = client.post('/users/register', json = mock_user_data_1)

  with app.app_context():
    assert response.status_code == 409
    assert response.json['message'] == "Email already exists!"

# Test multiple sucessful registrations
@pytest.mark.integration
def test_multiple_register_success(client, app):

  response = client.post('/users/register', json = mock_user_data_1)
  
  with app.app_context():
    assert response.status_code == 201
    assert response.json['message'] == "User successfully registered!"

  response = client.post('/users/register', json = mock_user_data_2)
  
  with app.app_context():
    assert response.status_code == 201
    assert response.json['message'] == "User successfully registered!"

  response = client.post('/users/register', json = mock_user_data_3)
  
  with app.app_context():
    assert response.status_code == 201
    assert response.json['message'] == "User successfully registered!"

# Test successful login to an existing account
@pytest.mark.integration
def test_login_success(client, app):

  # Register a new user
  client.post('/users/register', json = mock_user_data_1)

  # Try to log in to account
  response = client.post('/users/login', json = mock_login_data_1)

  with app.app_context():
    assert response.status_code == 200
    assert response.json['message'] == "Successfully logged in!"

# Test login to account that does not exist
@pytest.mark.integration
def test_login_not_exist(client, app):

  # Register a new user
  client.post('/users/register', json = mock_user_data_1)

  # Try to log in to an account that does not exist
  response = client.post('/users/login', json = mock_login_data_2)

  with app.app_context():
    assert response.status_code == 401
    assert response.json['message'] == "User does not exist!"

# Test login to account with an incorrect password
@pytest.mark.integration
def test_login_wrong_password(client, app):

  # Register a new user
  client.post('/users/register', json = mock_user_data_1)

  # Try to log in to account with an incorrect password
  response = client.post('/users/login', json = mock_login_data_3)

  with app.app_context():
    assert response.status_code == 401
    assert response.json['message'] == "Incorrect password!"
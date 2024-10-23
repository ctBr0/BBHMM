import pytest
from psycopg.rows import dict_row
from mock_data import *

# Using relative path
from utils.db import get_db # type: ignore

# Test successful expense creation
@pytest.mark.integration
def test_create_expense_success(client, app):

  client.post('/users/register', json = mock_user_data_1)
  client.post('/users/register', json = mock_user_data_2)

  response = client.post('/users/login', json = mock_login_data_1)
  token = response.json['access_token']

  with app.app_context():

    with get_db() as conn:
      with conn.cursor(row_factory = dict_row) as cur:
        cur.execute(
          """
            SELECT id
            FROM \"user\";
          """)
        user_ids = cur.fetchall()

  print(user_ids)

  response = client.post(
    '/expenses/non-group-expenses',
    headers = {
      'Authorization': f'Bearer {token}'
    },
    json = {
        'description': "Expense 1",
        'amount': 30,
        'payor_id': user_ids[0]['id'],
        'payee_id': user_ids[1]['id']
  })

  with app.app_context():
    assert response.status_code == 201
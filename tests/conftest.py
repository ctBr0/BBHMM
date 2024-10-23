import pytest
from app import create_app

# Using relative path
from utils.db import get_db # type: ignore

@pytest.fixture()
def app():
  # Create the Flask app with the testing configuration
  app = create_app('config.TestingConfig')

  yield app

  # Clean up the database after each test
  with app.app_context():
    with get_db() as conn:
      with conn.cursor() as cur:
        cur.execute("""DELETE FROM \"non_group_expense\";""")
        cur.execute("""DELETE FROM \"user\";""")
        conn.commit()

@pytest.fixture()
def client(app):
  return app.test_client()

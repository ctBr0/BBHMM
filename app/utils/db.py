import psycopg
from flask import current_app, g

def get_db():
  if 'db' not in g:
    g.db = psycopg.connect(current_app.config['DATABASE_URI'])
  return g.db

def close_db():
  db = g.pop('db', None)
  if db is not None:
    db.close()

def init_db():

  conn = get_db()

  # Open the schema.sql file and read the content to create the tables
  with open('schema.sql', 'r') as f:
    schema = f.read()

  with conn.cursor() as cursor:
    cursor.execute(schema)

  # Commit the changes and close the connection
  conn.commit()
  conn.close()
  print("Database initialized with schema.sql")

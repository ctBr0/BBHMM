import os
from dotenv import load_dotenv

load_dotenv()

class Config:
  SECRET_KEY = os.getenv('SECRET_KEY')
  JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
  TESTING = False

class DevelopmentConfig(Config):
  DATABASE_URI = os.getenv('DATABASE_DEV_URL') # Local PostgreSQL database

class TestingConfig(Config):
  TESTING = True
  DATABASE_URI = os.getenv('DATABASE_TEST_URL') # Local PostgreSQL database

class ProductionConfig(Config):
  DATABASE_URI = os.getenv('DATABASE_PROD_URL') # AWS RDS PostgreSQL database

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', '6353877251')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost/cryptawallx')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
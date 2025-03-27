import os

class Config:
    # In production, use a secure environment variable for SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    # Using SQLite for simplicity; update for other databases as needed
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

# Настройки Flask
SECRET_KEY = os.urandom(24)

# Настройки базы данных
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/Flowers store'
SQLALCHEMY_TRACK_MODIFICATIONS = False

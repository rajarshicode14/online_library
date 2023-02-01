from os import environ, getcwd, path
from dotenv import load_dotenv

load_dotenv(path.join(getcwd(), '.env'))

SECRET_KEY = environ.get('SECRET_KEY')
DB_URI = environ.get('DB_URI')



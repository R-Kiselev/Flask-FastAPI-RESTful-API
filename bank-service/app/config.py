import os

from dotenv import load_dotenv

load_dotenv()

FLASK_RUN_CERT = os.getenv("FLASK_CERT")
ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == 'development'
SECRET_KEY = os.getenv("SECRET_KEY")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")

SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False

LOG_SERVICE_URL = os.getenv("LOG_SERVICE_URL")
CALLBACK_QUEUE = os.getenv("CALLBACK_QUEUE")
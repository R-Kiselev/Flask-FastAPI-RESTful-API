from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from passlib.context import CryptContext

from app.message_queue import MessageQueue


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

message_queue_client = MessageQueue()
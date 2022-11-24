from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# creates a flask app
app = Flask(__name__)

# Loading .env file to access env variables
load_dotenv()

# Configuration of app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.getenv("DB_NAME")}.db'
app.config['SQLALCHEMY_TRACK_MODIFICATON'] = False

# creates an DB instance
db = SQLAlchemy(app)

# Creates an instane to encrypt passwords
bcrypt = Bcrypt(app)

# Creates an instance to handle authentication
jwt = JWTManager(app)

from src.api.auth import routes
from src.api.blog import routes
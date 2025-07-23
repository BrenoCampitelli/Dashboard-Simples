from dash import Dash
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


app = Dash(__name__)
server = app.server
app.config.supress_callback_exceptions = True

server.config.update(
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bancodedados.db',
    SECRET_KEY = 'kdbfvhyuhg87f9fhrnb875hafvbhrfh387f',
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)

database = SQLAlchemy(server)
bcrypt = Bcrypt(server)
login_manager = LoginManager(server)
login_manager.login_view = '/login'


from dashapp import views

